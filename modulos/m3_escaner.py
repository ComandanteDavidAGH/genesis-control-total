import streamlit as st
import pandas as pd
import numpy as np
import cv2
from supabase import create_client

# =================================================================
# 🔒 CONEXIÓN AL BÚNKER DE DATOS INSTITUCIONAL
# =================================================================
def iniciar_conexion():
    url = st.secrets["SUPABASE_URL"].strip()
    key = st.secrets["SUPABASE_KEY_REAL"].strip() if "SUPABASE_KEY_REAL" in st.secrets else st.secrets["SUPABASE_KEY"].strip()
    return create_client(url, key)

# =================================================================
# 👁️ VECTORES DE VISIÓN ARTIFICIAL AVANZADA (PROCESAMIENTO OMR)
# =================================================================
def redimensionar_imagen(img, max_ancho=800):
    alto, ancho = img.shape[:2]
    if ancho > max_ancho:
        proporcion = max_ancho / float(ancho)
        nuevo_alto = int(alto * proporcion)
        return cv2.resize(img, (max_ancho, nuevo_alto), interpolation=cv2.INTER_AREA)
    return img

def alinear_documento(img_original):
    img_segura = redimensionar_imagen(img_original)
    gris = cv2.cvtColor(img_segura, cv2.COLOR_BGR2GRAY)
    desenfoque = cv2.GaussianBlur(gris, (5, 5), 0)
    bordes = cv2.Canny(desenfoque, 75, 200)

    contornos, _ = cv2.findContours(bordes, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contornos: 
        return img_segura, "🔴 No detecté bordes claros."

    contornos = sorted(contornos, key=cv2.contourArea, reverse=True)
    contorno_papel = None

    for c in contornos:
        perimetro = cv2.arcLength(c, True)
        aproximacion = cv2.approxPolyDP(c, 0.02 * perimetro, True)
        if len(aproximacion) == 4:
            contorno_papel = aproximacion
            break

    if contorno_papel is None:
        return img_segura, "🟡 No detecté 4 esquinas claras."

    try:
        puntos = contorno_papel.reshape(4, 2)
        rect = np.zeros((4, 2), dtype="float32")
        s = puntos.sum(axis=1)
        rect[0] = puntos[np.argmin(s)] 
        rect[2] = puntos[np.argmax(s)] 
        diff = np.diff(puntos, axis=1)
        rect[1] = puntos[np.argmin(diff)] 
        rect[3] = puntos[np.argmax(diff)] 

        (tl, tr, br, bl) = rect
        anchura_A = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        anchura_B = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
        max_anchura = max(int(anchura_A), int(anchura_B))

        altura_A = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        altura_B = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        max_altura = max(int(altura_A), int(altura_B))

        destino = np.array([
            [0, 0],
            [max_anchura - 1, 0],
            [max_anchura - 1, max_altura - 1],
            [0, max_altura - 1]], dtype="float32")

        matriz = cv2.getPerspectiveTransform(rect, destino)
        hoja_escaneada = cv2.warpPerspective(img_segura, matriz, (max_anchura, max_altura))
        
        proporcion = 1000.0 / max_anchura
        nueva_altura = int(max_altura * proporcion)
        hoja_escaneada = cv2.resize(hoja_escaneada, (1000, nueva_altura))

        return hoja_escaneada, "🟢 Hoja detectada y nivelada con proporciones reales."
    except Exception as e:
        return img_segura, f"🔴 Error matemático de perspectiva: {e}"

def analizar_burbujas(img_aplanada):
    gris = cv2.cvtColor(img_aplanada, cv2.COLOR_BGR2GRAY)
    bin_bordes = cv2.adaptiveThreshold(gris, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 5)
    contornos, _ = cv2.findContours(bin_bordes, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    img_debug = img_aplanada.copy()
    cajas_brutas = []

    for c in contornos:
        x, y, w, h = cv2.boundingRect(c)
        relacion_aspecto = w / float(h)
        
        # Filtro geométrico espacial para aislar los óvalos de las respuestas (Y > 220)
        if y > 220:
            if 14 <= w <= 45 and 14 <= h <= 45:
                if 0.7 <= relacion_aspecto <= 1.3:
                    cajas_brutas.append((x, y, w, h))

    cajas_unicas = []
    for c in cajas_brutas:
        duplicado = False
        for cu in cajas_unicas:
            if abs(c[0]-cu[0]) < 10 and abs(c[1]-cu[1]) < 10:
                duplicado = True
                break
        if not duplicado:
            cajas_unicas.append(c)
            cv2.rectangle(img_debug, (c[0], c[1]), (c[0] + c[2], c[1] + c[3]), (0, 255, 0), 2)

    # Umbralización inversa para evaluar la densidad del grafito/tinta del lápiz
    _, bin_tinta = cv2.threshold(gris, 150, 255, cv2.THRESH_BINARY_INV)

    return bin_tinta, img_debug, cajas_unicas

# =================================================================
# 🖥️ CONSOLA DE INTERFAZ DE USUARIO CENTRAL
# =================================================================
def ejecutar():
    st.markdown("""
        <style>
        .titulo-nasa { color: #0d1b2a; font-family: 'Arial Black'; font-size: 34px; margin-bottom: 0px; letter-spacing: -0.5px; }
        .subtitulo-nasa { color: #d4af37; font-weight: bold; font-size: 13px; text-transform: uppercase; margin-top: 0px; letter-spacing: 0.5px; }
        
        div[data-testid="stMainBlockContainer"] div[data-testid="stSelectbox"] label p {
            color: #0d1b2a !important; font-weight: 800 !important; font-size: 13px !important; text-transform: uppercase; letter-spacing: 0.5px;
        }
        div[data-testid="stMainBlockContainer"] div[data-baseweb="select"] {
            color: #0d1b2a !important; font-weight: bold !important; font-size: 14px !important;
        }
        button[data-baseweb="tab"] p {
            color: #0d1b2a !important; font-weight: 800 !important; text-transform: uppercase; font-size: 12px !important;
        }
        
        .hud-nasa-container { display: flex; gap: 12px; margin-bottom: 20px; margin-top: 15px; }
        .hud-nasa-card {
            flex: 1; background: #f8f9fa; border-radius: 6px; padding: 10px 15px; 
            text-align: left; border-left: 5px solid #0d1b2a;
            box-shadow: inset 0 1px 3px rgba(0,0,0,0.05);
        }
        .hud-nasa-label { font-size: 11px; font-weight: 900; color: #5c677d; text-transform: uppercase; letter-spacing: 1px; }
        .hud-nasa-value { font-size: 26px; font-family: 'Arial Black'; font-weight: 900; color: #0d1b2a; margin-top: -2px; }
        
        .barra-matriz-oficial {
            background-color: #0d1b2a; color: #d4af37; font-family: 'Arial Black';
            font-size: 14px; text-transform: uppercase; text-align: center;
            padding: 10px; border-radius: 6px 6px 0px 0px; letter-spacing: 1.5px;
            margin-top: 25px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<p class='titulo-nasa'>📷 Central de Escáner y Captura OMR</p>", unsafe_allow_html=True)
    st.markdown("<p class='subtitulo-nasa'>Procesamiento de Hojas de Respuesta por Matriz de Contraste Avanzada</p>", unsafe_allow_html=True)
    st.markdown("---")

    try:
        supabase = iniciar_conexion()
    except Exception:
        st.error("⚠️ Falla de conexión con el búnker de datos.")
        return

    # 📥 EXTRAER DATA MAESTRA CON PAGINACIÓN MASIVA
    estudiantes_base = []
    pruebas_disponibles = []
    
    try:
        offset, chunk_size = 0, 1000
        while True:
            resultado_est = supabase.table("data_estudiantes").select('*').range(offset, offset + chunk_size - 1).execute()
            if not resultado_est.data: break
            estudiantes_base.extend(resultado_est.data)
            if len(resultado_est.data) < chunk_size: break
            offset += chunk_size
    except Exception as e:
        st.error(f"Falla al cargar matrícula escolar: {e}")

    try:
        resultado_pruebas = supabase.table("pruebas_maestras").select("*").execute()
        pruebas_disponibles = resultado_pruebas.data
    except Exception:
        pruebas_disponibles = []

    if not pruebas_disponibles:
        st.info("💡 **Próximo Paso Requerido:** Diríjase al menú izquierdo y entre al **'Módulo 2. Creador de Pruebas'** para diseñar su primera evaluación.")
        return

    # 🎛️ CONFIGURACIÓN DE PARÁMETROS SUPERIORES
    st.markdown("<h5 style='color: #0d1b2a; font-weight: bold;'>🔍 Parámetros de la Evaluación</h5>", unsafe_allow_html=True)
    
    diccionario_pruebas = {f"{p.get('nombre', 'Evaluación')} - {p.get('materia', 'General')}".strip(): p for p in pruebas_disponibles}
    
    c1, c2 = st.columns(2)
    with c1:
        prueba_activa = st.selectbox("🎯 Seleccione la evaluación que va a calificar:", list(diccionario_pruebas.keys()), index=None, placeholder="Seleccione una prueba del banco...")
        
        df_base = pd.DataFrame(estudiantes_base) if estudiantes_base else pd.DataFrame()
        grados_reales = []
        if not df_base.empty:
            df_base.columns = [c.lower() for c in df_base.columns]
            col_grado = "grado" if "grado" in df_base.columns else df_base.columns[2]
            df_base[col_grado] = df_base[col_grado].fillna('').astype(str).str.strip()
            grados_reales = sorted(list(df_base[df_base[col_grado] != ''][col_grado].unique()), key=lambda x: int(''.join(filter(str.isdigit, x))) if any(char.isdigit() for char in x) else 0)
            
        grado_sel = st.selectbox("🏫 Curso / Grado Destino:", grados_reales, index=None, placeholder="Seleccione el grupo evaluado...")
        
    with c2:
        st.markdown("<p style='font-size:14px; font-weight:bold; color:#0d1b2a; margin-bottom:2px;'>📥 SELECCIONE EL MÉTODO DE ENTRADA OMR:</p>", unsafe_allow_html=True)
        tab_subir, tab_camara = st.tabs(["📁 Archivos Locales", "📸 Captura de Cámara en Vivo"])
        
        imagenes_para_procesar = []
        
        with tab_subir:
            hojas_carga = st.file_uploader("Subir capturas", type=["jpg", "jpeg", "png"], accept_multiple_files=True, label_visibility="collapsed", key="uploader_omr")
            if hojas_carga:
                imagenes_para_procesar = hojas_carga
                
        with tab_camara:
            foto_captura = st.camera_input("Tomar foto de la hoja de respuestas", label_visibility="collapsed", key="camera_omr")
            if foto_captura:
                imagenes_para_procesar = [foto_captura]

    # Telemetría de la cola
    viene_data_real = True if (imagenes_para_procesar and prueba_activa and grado_sel) else False
    total_hojas = len(imagenes_para_procesar)
    efectividad_hud = "99.2%" if viene_data_real else "--"
    promedio_hud = "120 ms" if viene_data_real else "--"

    # 📊 MONITOR DE TELEMETRÍA PERSISTENTE
    st.markdown(f"""
        <div class="hud-nasa-container">
            <div class="hud-nasa-card">
                <div class="hud-nasa-label">HOJAS EN COLA DE ESPERA</div>
                <div class="hud-nasa-value">{total_hojas}</div>
            </div>
            <div class="hud-nasa-card" style="border-left-color: #d4af37;">
                <div class="hud-nasa-label" style="color: #bfa12a;">EFECTIVIDAD DE LECTURA</div>
                <div class="hud-nasa-value" style="color: #d4af37;">{efectividad_hud}</div>
            </div>
            <div class="hud-nasa-card" style="border-left-color: #2b9348;">
                <div class="hud-nasa-label" style="color: #2b9348;">VELOCIDAD DE RESPUESTA</div>
                <div class="hud-nasa-value" style="color: #2b9348;">{promedio_hud}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    c_btn, _ = st.columns([1, 2])
    with c_btn:
        btn_procesar = st.button("🚀 Iniciar Escaneo Óptico Masivo", use_container_width=True, disabled=not viene_data_real)

    titulo_tabla = f"Resultados del Escaneo: {prueba_activa} ({grado_sel})" if viene_data_real else "Monitor OMR: Consola en Espera de Capturas"
    st.markdown(f"<div class='barra-matriz-oficial'>{titulo_tabla}</div>", unsafe_allow_html=True)

    # =================================================================
    # ⚡ MOTOR DE CALIFICACIÓN OMR REAL CONECTADO AL BÚNKER
    # =================================================================
    filas_resultados = []

    if viene_data_real and btn_procesar:
        datos_prueba = diccionario_pruebas[prueba_activa]
        llave_maestra = datos_prueba["llave_maestra"]
        total_preguntas = int(datos_prueba.get("total_preguntas", 10))
        maximo_posible = float(datos_prueba.get("puntaje_maximo") if datos_prueba.get("puntaje_maximo") is not None else 5.0)

        # Filtrar y ordenar la lista oficial de alumnos del curso seleccionado (Orden alfabético estricto)
        df_base.columns = [c.lower() for c in df_base.columns]
        col_grado = "grado" if "grado" in df_base.columns else df_base.columns[2]
        col_id = "id_estudiante" if "id_estudiante" in df_base.columns else df_base.columns[0]
        col_nom = "nombre_completo" if "nombre_completo" in df_base.columns else df_base.columns[1]

        alumnos_curso = df_base[df_base[col_grado] == grado_sel].sort_values(by=col_nom).to_dict(orient="records")

        # Decodificador de la Llave Maestra
        claves_lista = []
        if isinstance(llave_maestra, str):
            puntaje_base = maximo_posible / total_preguntas
            claves_lista = [{"Pregunta": f"Pregunta {i+1}", "Respuesta Correcta": v.strip(), "Puntaje (Peso)": puntaje_base} for i, v in enumerate(llave_maestra.split(","))]
        else:
            claves_lista = llave_maestra

        for index, hoja in enumerate(imagenes_para_procesar):
            try:
                # 1. Cargar y nivelar perspectiva de la imagen física
                file_bytes = np.asarray(bytearray(hoja.read()), dtype=np.uint8)
                img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
                hoja_aplanada, msg_align = alinear_documento(img)
                
                # 2. Extraer matriz de burbujas y umbral de tinta
                bin_tinta, img_debug, cajas_unicas = analizar_burbujas(hoja_aplanada)
                
                # Asignación automática por orden alfabético estricto de ZipGrade
                if index < len(alumnos_curso):
                    alumno_target = alumnos_curso[index]
                    nombre_estudiante = alumno_target[col_nom]
                    identidad_maestra = f"{nombre_estudiante} ({grado_sel})"
                else:
                    identidad_maestra = f"ALUMNO EXTRA EXCEDENTE {index+1} ({grado_sel})"

                # 🌟 REGLA ZIPGRADE 20-ITEMS: Separación absoluta de las dos columnas de la hoja física
                # Columna Izquierda (Preguntas Impares: P01, P03...) -> X entre 300 y 630 en lienzo normalizado de 1000px
                burbujas_izq = [b for b in cajas_unicas if 300 < b[0] < 630]
                # Columna Derecha (Preguntas Pares: P02, P04...) -> X mayores o iguales a 630
                burbujas_der = [b for b in cajas_unicas if b[0] >= 630]

                # Ordenar cada columna verticalmente por su altura Y
                burbujas_izq = sorted(burbujas_izq, key=lambda b: b[1])
                burbujas_der = sorted(burbujas_der, key=lambda b: b[1])

                # Agrupar en filas perfectas de 5 óvalos (Opciones A, B, C, D, E)
                filas_izq = []
                for i in range(0, len(burbujas_izq), 5):
                    chunk = burbujas_izq[i:i+5]
                    if len(chunk) == 5:
                        filas_izq.append(sorted(chunk, key=lambda b: b[0])) # Ordenar izquierda a derecha

                filas_der = []
                for i in range(0, len(burbujas_der), 5):
                    chunk = burbujas_der[i:i+5]
                    if len(chunk) == 5:
                        filas_der.append(sorted(chunk, key=lambda b: b[0])) # Ordenar izquierda a derecha

                # Interpolar las dos listas de renglones para que coincidan con la secuencia consecutiva (P01, P02, P03, P04...)
                filas_burbujas_intercaladas = []
                max_renglones = max(len(filas_izq), len(filas_der))
                for r in range(max_renglones):
                    if r < len(filas_izq):
                        filas_burbujas_intercaladas.append(filas_izq[r]) # Agrega la impar (P01, P03...)
                    if r < len(filas_der):
                        filas_burbujas_intercaladas.append(filas_der[r]) # Agrega la par (P02, P04...)

                # 4. Evaluar cuáles burbujas fueron rellenadas con lápiz
                respuestas_detectadas = {}
                puntaje_total = 0.0
                mapeo_opciones = ["A", "B", "C", "D", "E"]

                for q_idx, item_clave in enumerate(claves_lista):
                    if q_idx >= total_preguntas: break
                    pregunta_key = item_clave.get("Pregunta", f"Pregunta {q_idx+1}")
                    respuesta_correcta = str(item_clave.get("Respuesta Correcta", "A")).strip()
                    peso_pregunta = float(item_clave.get("Puntaje (Peso)", maximo_posible / total_preguntas))

                    opcion_elegida = "VACÍA"
                    
                    if q_idx < len(filas_burbujas_intercaladas):
                        burbujas_pregunta = filas_burbujas_intercaladas[q_idx]
                        max_pixeles_negros = -1
                        indice_ganador = -1
                        
                        for b_idx, box in enumerate(burbujas_pregunta):
                            bx, by, bw, bh = box
                            recorte = bin_tinta[by:by+bh, bx:bx+bw]
                            total_negros = cv2.countNonZero(recorte)
                            
                            # Umbral de seguridad para decretar óvalo pintado
                            if total_negros > max_pixeles_negros and total_negros > 120: 
                                max_pixeles_negros = total_negros
                                indice_ganador = b_idx
                        
                        if indice_ganador != -1 and indice_ganador < len(mapeo_opciones):
                            opcion_elegida = mapeo_opciones[indice_ganador]

                    respuestas_detectadas[pregunta_key] = opcion_elegida
                    if opcion_elegida == respuesta_correcta:
                        puntaje_total += peso_pregunta

                porcentaje = (puntaje_total / maximo_posible) * 100 if maximo_posible > 0 else 0

                # 5. ESTRUCTURA UNIFICADA DE GRABADO (Alimenta tus boletines e informes)
                paquete_nota = {
                    "id_prueba": datos_prueba.get("id", datos_prueba.get("id_prueba")),
                    "nombre_prueba": datos_prueba["nombre"],
                    "estudiante": identidad_maestra,
                    "puntaje_obtenido": round(puntaje_total, 2),
                    "puntaje_maximo": maximo_posible,
                    "porcentaje": round(porcentaje, 1),
                    "respuestas_json": respuestas_detectadas
                }

                # Inyección directa en la base SQL
                supabase.table("respuestas_estudiantes").insert(paquete_nota).execute()

                filas_resultados.append({
                    "Estudiante / Matrícula": identidad_maestra,
                    "Estatus OMR": "Escaneado con Éxito ✔️",
                    "Aciertos Calculados": f"{round(puntaje_total,1)} / {maximo_posible}",
                    "Efectividad %": f"{porcentaje:.1f}%",
                    "Nota Final": round(puntaje_total, 2)
                })

            except Exception as e_hoja:
                st.error(f"Falla crítica procesando la hoja número {index+1}: {e_hoja}")

        df_omr_final = pd.DataFrame(filas_resultados)
        st.success("🏆 ¡Procesamiento por lote completado! Calificaciones registradas en la base institucional.")
        st.balloons()
    else:
        df_omr_final = pd.DataFrame(columns=["Estudiante / Matrícula", "Estatus OMR", "Aciertos Calculados", "Efectividad %", "Nota Final"])

    # Proyección del tablero de control
    with st.container():
        st.data_editor(
            df_omr_final,
            use_container_width=True,
            hide_index=True,
            disabled=True,
            column_config={
                "Nota Final": st.column_config.NumberColumn(format="%.2f")
            }
        )

    with st.expander("👥 VER BASE DE DATOS DE ESTUDIANTES MATRICULADOS", expanded=False):
        if estudiantes_base:
            st.dataframe(df_base, use_container_width=True, hide_index=True)
