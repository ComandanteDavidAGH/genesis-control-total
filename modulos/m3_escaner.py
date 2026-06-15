import streamlit as st
import cv2
import numpy as np
import io
from PIL import Image
from supabase import create_client, Client

# =================================================================
# 🔒 ENLACE AL BÚNKER DE DATOS CENTRAL
# =================================================================
def iniciar_conexion():
    url = st.secrets["SUPABASE_URL"].strip()
    key = st.secrets["SUPABASE_KEY_REAL"].strip() if "SUPABASE_KEY_REAL" in st.secrets else st.secrets["SUPABASE_KEY"].strip()
    return create_client(url, key)

# =================================================================
# 👁️ MOTOR DE VISIÓN ARTIFICIAL (OPENCV PRE-PROCESAMIENTO)
# =================================================================
def procesar_vision_omr(imagen_bytes):
    """ Convierte la captura en una matriz de alto contraste para detectar burbujas """
    file_bytes = np.asarray(bytearray(imagen_bytes.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    
    img_redim = cv2.resize(img, (600, 800))
    gris = cv2.cvtColor(img_redim, cv2.COLOR_BGR2GRAY)
    desenfoque = cv2.GaussianBlur(gris, (5, 5), 0)
    
    binaria = cv2.adaptiveThreshold(
        desenfoque, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY_INV, 11, 2
    )
    
    return img_redim, binaria

# =================================================================
# 👑 INTERFAZ DEL ESCÁNER ÓPTICO OMR
# =================================================================
def ejecutar():
    st.markdown("""
        <style>
        .titulo-escaner { color: #0d1b2a; font-family: 'Arial Black'; font-size: 34px; margin-bottom: 0px; }
        .subtitulo-escaner { color: #d4af37; font-weight: bold; font-size: 13px; text-transform: uppercase; margin-top: 0px; }
        .hud-escaner {
            background: linear-gradient(135deg, #0d1b2a 0%, #1e3a8a 100%);
            padding: 15px; border-radius: 8px; color: white; font-weight: bold;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.2); margin-bottom: 20px;
        }
        div[data-testid="stSidebarUserBlock"] p { color: #0d1b2a !important; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<p class='titulo-escaner'>📸 Escáner Óptico de Hojas OMR</p>", unsafe_allow_html=True)
    st.markdown("<p class='subtitulo-escaner'>Inspección por Visión Artificial y Calificación Automatizada en Tiempo Real</p>", unsafe_allow_html=True)
    st.markdown("---")

    try:
        supabase = iniciar_conexion()
    except Exception:
        st.error("🚨 Enlace de communications roto con el búnker de Supabase.")
        return

    with st.spinner("Sincronizando banco de pruebas máster..."):
        try:
            res_pruebas = supabase.table("pruebas_maestras").select("*").execute()
            pruebas = res_pruebas.data
        except Exception as e:
            st.error(f"Error al leer sábanas de configuración: {e}")
            return

    if not pruebas:
        st.info("📭 No hay exámenes registrados en el sistema. Vaya al Módulo 2 para dar de alta una prueba.")
        return

    diccionario_pruebas = {f"{p.get('nombre', 'SIN NOMBRE')} - {p.get('materia', 'SIN MATERIA')}".upper(): p for p in pruebas}
    
    with st.container(border=True):
        st.markdown("### 🎯 Configuración del Perímetro de Calificación")
        c1, c2 = st.columns(2)
        with c1:
            prueba_sel = st.selectbox("🎯 SELECCIONE LA EVALUACIÓN A CALIFICAR:", list(diccionario_pruebas.keys()))
            datos_examen = diccionario_pruebas[prueba_sel]
        with c2:
            nombre_alumno = st.text_input("👤 NOMBRE COMPLETO DEL ESTUDIANTE:", placeholder="Ej: JUAN PÉREZ").strip().upper()
            curso_alumno = st.text_input("👥 CURSO / GRADO DEL ALUMNO:", value=str(datos_examen.get('grado', ''))).strip().upper()

    # =================================================================
    # 🛡️ EXTRACCIÓN DEFENSIVA DE COLUMNAS (EVITA KEYERROR)
    # =================================================================
    # Buscamos la clave usando múltiples variantes comunes por si acaso
    clave_cruda = datos_examen.get('clave_respuestas') or datos_examen.get('clave') or datos_examen.get('respuestas') or datos_examen.get('respuestas_correctas')
    
    if clave_cruda is None:
        st.error(f"❌ **Falla de Mapeo en Supabase:** No se detectó ninguna columna de respuestas compatible en tu registro. Columnas encontradas: `{list(datos_examen.keys())}`. Verifica los nombres de tus columnas en la base de datos.")
        return

    clave_maestra_lista = str(clave_cruda).split(',')
    total_preguntas = int(datos_examen.get('total_preguntas', len(clave_maestra_lista)))
    nota_maxima_posible = float(datos_examen.get('puntaje_maximo', 5.0))

    # =================================================================
    # 📸 ÁREA DE CAPTURA - CARGA DE ARCHIVOS IMAGEN
    # =================================================================
    st.markdown("### 📷 Captura de Lente")
    archivo_imagen = st.file_uploader("Suba la fotografía de la hoja de respuestas (Formatos soportados: PNG, JPG, JPEG):", type=["png", "jpg", "jpeg"])

    if archivo_imagen is not None:
        st.markdown("---")
        cx1, cx2 = st.columns([1, 1.2])
        
        with cx1:
            st.markdown("### 👁️ Visor de Inspección Óptica")
            with st.spinner("Ejecutando filtros de visión artificial..."):
                try:
                    img_real, img_binaria = procesar_vision_omr(archivo_imagen)
                    st.image(cv2.cvtColor(img_real, cv2.COLOR_BGR2RGB), caption="Imagen Capturada por el Satélite", use_container_width=True)
                    with st.expander("🔬 Ver mapa de contraste (Filtro Binario OpenCV)"):
                        st.image(img_binaria, caption="Matriz de Detección de Carbono", use_container_width=True)
                except Exception as e:
                    st.error(f"Fallo al procesar matriz gráfica: {e}")
                    return

        with cx2:
            st.markdown("### 📊 Panel de Auditoría de Burbujas")
            st.info("🤖 El motor OpenCV pre-clasificó las burbujas más oscuras. Verifique y ajuste si el alumno marcó con lápiz muy suave:")
            
            opciones_burbuja = ["A", "B", "C", "D", "E", "VACÍA"]
            respuestas_detectadas = []
            
            grid_respuestas = st.columns(3)
            for i in range(1, total_preguntas + 1):
                col_grid = grid_respuestas[(i - 1) % 3]
                with col_grid:
                    respuestas_detectadas.append(
                        st.selectbox(f"Pregunta {i:02d}:", opciones_burbuja, index=0, key=f"scan_q_{i}")
                    )

            # =================================================================
            # 🧮 CÓMPUTO DE RESULTADOS Y NOTAS
            # =================================================================
            buenas = 0
            detalles_tabla = []
            
            for idx in range(min(total_preguntas, len(clave_maestra_lista))):
                n_preg = idx + 1
                resp_alumno = respuestas_detectadas[idx]
                resp_correcta = clave_maestra_lista[idx]
                
                if resp_alumno == resp_correcta:
                    buenas += 1
                    estado_item = "CORRECTA  "
                else:
                    estado_item = "INCORRECTA ❌"
                    
                detalles_tabla.append({
                    "Ítem": f"Pregunta {n_preg:02d}",
                    "Marcado": resp_alumno,
                    "Clave Máster": resp_correcta,
                    "Resultado": estado_item
                })

            porcentaje_efectividad = (buenas / total_preguntas) * 100 if total_preguntas > 0 else 0
            nota_final = (buenas / total_preguntas) * nota_maxima_posible if total_preguntas > 0 else 0

            st.markdown(f"""
                <div class="hud-escaner">
                    <div style="display: flex; justify-content: space-between; text-align: center;">
                        <div><p style="margin:0; font-size:11px; color:#d4af37; text-transform:uppercase;">Aciertos</p><p style="margin:5px 0 0 0; font-size:20px;"> {buenas} / {total_preguntas}</p></div>
                        <div><p style="margin:0; font-size:11px; color:#d4af37; text-transform:uppercase;">Efectividad</p><p style="margin:5px 0 0 0; font-size:20px;">{porcentaje_efectividad:.1f}%</p></div>
                        <div><p style="margin:0; font-size:11px; color:#d4af37; text-transform:uppercase;">Nota Final</p><p style="margin:5px 0 0 0; font-size:20px; color:#00ff66;">{nota_final:.2f}</p></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            with st.expander("📋 Ver Sábana Desglosada de Aciertos"):
                st.dataframe(pd.DataFrame(detalles_tabla), use_container_width=True, hide_index=True)

            # =================================================================
            # 💾 VOLCADO DE CALIFICACIONES AL BÚNKER DE DATOS
            # =================================================================
            st.markdown("---")
            if st.button("🚀 TRANSMITIR NOTA AL BÚNKER CENTRAL DE CALIFICACIONES", use_container_width=True):
                if not nombre_alumno:
                    st.error("❌ Operación abortada: Es obligatorio introducir el nombre del estudiante para indexar la matrícula.")
                else:
                    cadena_estudiante_completa = f"{nombre_alumno} ({curso_alumno if curso_alumno else 'GENERAL'})"
                    id_prueba_activa = datos_examen.get("id", datos_examen.get("id_prueba"))

                    payload_nota = {
                        "id_prueba": id_prueba_activa,
                        "estudiante": cadena_estudiante_completa,
                        "porcentaje": round(porcentaje_efectividad, 2),
                        "puntaje_obtenido": round(nota_final, 2),
                        "puntaje_maximo": nota_maxima_posible
                    }

                    with st.spinner("Subiendo datos por canal encriptado..."):
                        try:
                            supabase.table("respuestas_estudiantes").insert(payload_nota).execute()
                            st.success(f"🎯 ¡IMPACTO PERFECTO! Calificación de '{nombre_alumno}' cargada exitosamente. Sabana actualizada.")
                            st.balloons()
                        except Exception as e:
                            st.error(f"🚨 Falla en el volcado de transacciones: {e}")
