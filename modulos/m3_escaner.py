import streamlit as st
from estilos_globales import inyectar_estilos_omega
import pandas as pd
import cv2
import numpy as np
from supabase import create_client

# =================================================================
# 🔒 CONEXIÓN AL BÚNKER DE DATOS INSTITUCIONAL
# =================================================================
def iniciar_conexion():
    url = st.secrets["SUPABASE_URL"].strip()
    key = st.secrets["SUPABASE_KEY"].strip()
    return create_client(url, key)

# =================================================================
# 🛡️ SENSOR DETECTOR INALÁMBRICO DE COLUMNAS (Anti-Case-Sensitivity)
# =================================================================
def buscar_campo(diccionario, nombre_campo, predeterminado=""):
    if not diccionario:
        return predeterminado
    for llave, valor in diccionario.items():
        if llave.lower() == nombre_campo.lower():
            if valor is not None and str(valor).strip().lower() not in ['none', 'null', '']:
                return valor
    return predeterminado

# =================================================================
# 👁️ MOTOR CORE DE VISIÓN ARTIFICIAL
# =================================================================
def escanear_burbujas_opencv(imagen_bytes, llave_correcta):
    """
    Procesa la imagen, detecta burbujas marcadas y las compara con la llave maestra.
    """
    img = cv2.imdecode(imagen_bytes, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Error al decodificar la imagen.")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    # Buscar contornos (Burbujas)
    cnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    burbujas = []

    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        ar = w / float(h)
        if w >= 15 and h >= 15 and 0.8 <= ar <= 1.2:
            burbujas.append(c)

    if len(burbujas) < len(llave_correcta) * 4: 
        return img, -1, None

    burbujas = sorted(burbujas, key=lambda b: cv2.boundingRect(b)[1])
    
    aciertos = 0
    opciones_letras = ['A', 'B', 'C', 'D']
    
    for (q, i) in enumerate(np.arange(0, len(llave_correcta) * 4, 4)):
        fila_burbujas = sorted(burbujas[i:i + 4], key=lambda b: cv2.boundingRect(b)[0])
        
        burbuja_marcada = None
        max_pixeles = 0
        
        for (j, b) in enumerate(fila_burbujas):
            mask = np.zeros(thresh.shape, dtype="uint8")
            cv2.drawContours(mask, [b], -1, 255, -1)
            mask = cv2.bitwise_and(thresh, thresh, mask=mask)
            total_pixeles = cv2.countNonZero(mask)
            
            if total_pixeles > max_pixeles:
                max_pixeles = total_pixeles
                burbuja_marcada = j
        
        respuesta_detectada = opciones_letras[burbuja_marcada]
        if respuesta_detectada == llave_correcta[q].strip().upper():
            aciertos += 1
            cv2.drawContours(img, [fila_burbujas[burbuja_marcada]], -1, (0, 255, 0), 3)
        else:
            cv2.drawContours(img, [fila_burbujas[burbuja_marcada]], -1, (0, 0, 255), 3)

    return img, aciertos, burbujas

def ejecutar():
    inyectar_estilos_omega()

    st.markdown("<h1 style='text-align: center; color: #0F172A; font-size: 3rem;'>📸 Motor de Escaneo OMR v3.0</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2rem; color: #D97706; font-weight: bold; letter-spacing: 1px;'>IDENTIFICACIÓN AUTÓNOMA Y CALIFICACIÓN TÁCTICA</p>", unsafe_allow_html=True)
    st.markdown("---")

    try:
        supabase = iniciar_conexion()
    except Exception:
        st.error("🚨 Falla en el enlace satelital con Supabase.")
        return

    with st.spinner("Sincronizando el catálogo oficial del búnker..."):
        try:
            res_consolidado = supabase.table("notas_consolidadas").select("ASIGNATURA").execute()
            materias_raw = res_consolidado.data if res_consolidado.data else []
            
            res_pruebas = supabase.table("pruebas_maestras").select("*").execute()
            pruebas = res_pruebas.data if res_pruebas.data else []
            
            estudiantes_base = []
            offset, chunk_size = 0, 1000
            while True:
                resultado = supabase.table("data_estudiantes").select('Nombre_Completo, Grado').range(offset, offset + chunk_size - 1).execute()
                if not resultado.data: break
                estudiantes_base.extend(resultado.data)
                if len(resultado.data) < chunk_size: break
                offset += chunk_size
        except Exception as e:
            st.error(f"🚨 Error de lectura: {e}")
            return

    if materias_raw:
        df_mat = pd.DataFrame(materias_raw)
        lista_materias = sorted(df_mat["ASIGNATURA"].dropna().astype(str).str.upper().str.strip().unique().tolist())
    else:
        lista_materias = ["MATEMÁTICAS", "CIENCIAS NATURALES"]

    if estudiantes_base:
        df_est = pd.DataFrame(estudiantes_base)
        df_est.columns = [col.lower() for col in df_est.columns]
        df_est["grado"] = df_est["grado"].dropna().astype(str).str.upper().str.strip()
        df_est["nombre_completo"] = df_est["nombre_completo"].dropna().astype(str).str.upper().str.strip()
        lista_grados_disponibles = sorted(df_est["grado"].unique().tolist())
    else:
        df_est = pd.DataFrame()
        lista_grados_disponibles = ["10°", "11°"]

    st.markdown("### ⚙️ PASO 1: Parámetros de Calibración (Coincidencia Exacta)")
    
    with st.container(border=True):
        c1, c2 = st.columns(2)
        with c1:
            materia_seleccionada = st.selectbox("🎯 ASIGNATURA:", lista_materias)
            grado_seleccionado = st.selectbox("👥 CURSO / GRADO:", lista_grados_disponibles)

        with c2:
            id_prueba_master = 1  
            max_preguntas = 10
            puntaje_maximo = 5.0
            llave_maestra_lista = []
            
            match_prueba = [p for p in pruebas if str(buscar_campo(p, 'materia')).strip().upper() == materia_seleccionada and str(buscar_campo(p, 'grado')).strip().upper() == grado_seleccionado]
            
            if match_prueba:
                datos_prueba = match_prueba[0]
                id_prueba_master = datos_prueba.get("id_prueba") or datos_prueba.get("id", 1)
                max_preguntas = int(buscar_campo(datos_prueba, 'total_preguntas', 10))
                puntaje_maximo = float(buscar_campo(datos_prueba, 'puntaje_maximo', 5.0))
                
                llave_raw = str(buscar_campo(datos_prueba, 'llave_maestra', ''))
                if llave_raw:
                    llave_maestra_lista = llave_raw.split(',')
                    st.success(f"🔑 Matriz detectada: {max_preguntas} Preguntas | Base {puntaje_maximo}.")
                else:
                    st.warning("⚠️ Prueba detectada, pero no tiene Llave Maestra configurada.")
            else:
                max_preguntas = st.number_input("📋 CANTIDAD DE PREGUNTAS:", min_value=1, max_value=100, value=10, step=1)
                st.info("ℹ️ No se detectó plantilla en el búnker para este cruce. Operación Manual requerida.")

    lista_alumnos_salón = []
    if not df_est.empty:
        df_alumnos_filtrados = df_est[df_est["grado"] == grado_seleccionado]
        lista_alumnos_salón = sorted(df_alumnos_filtrados["nombre_completo"].unique().tolist())
    
    if not lista_alumnos_salón:
        lista_alumnos_salón = ["SIN ALUMNOS REGISTRADOS EN ESTE GRADO"]

    st.markdown("---")
    st.markdown("### 📷 PASO 2: Procesamiento Óptico (OMR)")
    
    file_bytes = None
    
    # 📡 INTERCEPCIÓN TÁCTICA: ¿Venimos de la app móvil (Google Drive)?
    if "imagen_satelital" in st.session_state and st.session_state.imagen_satelital is not None:
        st.warning(f"📡 VISTA ACTIVA: Procesando examen satelital `{st.session_state.nombre_imagen_satelital}`")
        # Convertimos los bytes guardados en memoria a array de numpy
        file_bytes = np.frombuffer(st.session_state.imagen_satelital, dtype=np.uint8)
        
        if st.button("❌ Descargar imagen y regresar al escáner local"):
            st.session_state.imagen_satelital = None
            st.session_state.nombre_imagen_satelital = None
            st.rerun()
    else:
        # Modo de contingencia tradicional (Carga manual)
        archivo_imagen = st.file_uploader("SUBA LA FOTOGRAFÍA DE LA TARJETA DE RESPUESTAS:", type=["png", "jpg", "jpeg"])
        if archivo_imagen is not None:
            file_bytes = np.asarray(bytearray(archivo_imagen.read()), dtype=np.uint8)

    alumno_final = st.selectbox("👤 SELECCIONE EL ESTUDIANTE A CALIFICAR:", lista_alumnos_salón)
    aciertos_detectados = 0
    mostrar_controles_finales = False

    if file_bytes is not None:
        if llave_maestra_lista and len(llave_maestra_lista) == max_preguntas:
            try:
                img_procesada, aciertos_auto, contornos = escanear_burbujas_opencv(file_bytes, llave_maestra_lista)
                
                if aciertos_auto != -1:
                    st.image(img_procesada, caption="📸 Imagen Procesada y Calificada por OpenCV", use_container_width=True, channels="BGR")
                    st.success(f"🤖 ¡Escaneo exitoso! OpenCV detectó {aciertos_auto} respuestas correctas basado en la Llave Maestra.")
                    aciertos_detectados = aciertos_auto
                    mostrar_controles_finales = True
                else:
                    raise Exception("Geometría de burbujas no detectada.")
                    
            except Exception as e:
                st.error("⚠️ La foto no tiene la claridad necesaria para el reconocimiento automático. Digite los aciertos manualmente.")
                aciertos_detectados = st.number_input("✍️ DIGITE LOS ACIERTOS REALES EVALUADOS VISUALMENTE:", min_value=0, max_value=int(max_preguntas), value=0)
                mostrar_controles_finales = True
        else:
            st.warning("No hay una Llave Maestra válida para comparar. Ingrese la nota manualmente.")
            if "imagen_satelital" in st.session_state and st.session_state.imagen_satelital is not None:
                st.image(st.session_state.imagen_satelital)
            else:
                st.image(archivo_imagen, caption="Imagen Subida")
            aciertos_detectados = st.number_input("✍️ DIGITE LOS ACIERTOS:", min_value=0, max_value=int(max_preguntas), value=0)
            mostrar_controles_finales = True

    if mostrar_controles_finales:
        preguntas_divisor = max_preguntas if max_preguntas > 0 else 10
        porcentaje_rendimiento = (aciertos_detectados / preguntas_divisor) * 100
        nota_final = (aciertos_detectados / preguntas_divisor) * puntaje_maximo

        st.markdown("<br>", unsafe_allow_html=True)
        cc1, cc2 = st.columns([1.5, 1])
        with cc1:
            st.markdown(f"""
                <div style="background-color: #0d1b2a; padding: 15px; border-radius: 6px; text-align: center; border-left: 4px solid #d4af37; border: 2px solid #0d1b2a;">
                    <div style="display: flex; justify-content: space-around; align-items: center;">
                        <div>
                            <p style="margin:0; font-size:11px; color:#d4af37; font-weight:bold;">RENDIMIENTO</p>
                            <p style="margin:5px 0 0 0; font-size:26px; color:white; font-family:'Arial Black';">{porcentaje_rendimiento:.1f}%</p>
                        </div>
                        <div style="border-left: 1px solid rgba(255,255,255,0.2); padding-left:20px;">
                            <p style="margin:0; font-size:11px; color:#d4af37; font-weight:bold;">NOTA PROYECTADA</p>
                            <p style="margin:5px 0 0 0; font-size:26px; color:#00ff66; font-family:'Arial Black';">{nota_final:.2f} / {puntaje_maximo:.1f}</p>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
        with cc2:
            st.markdown("<div style='margin-top:5px;'></div>", unsafe_allow_html=True)
            boton_inyectar = st.button("🚀 TRANSMITIR CALIFICACIÓN", use_container_width=True, type="primary")

        if boton_inyectar and alumno_final != "SIN ALUMNOS REGISTRADOS EN ESTE GRADO":
            firma_estudiante = f"{alumno_final} ({grado_seleccionado})"
            payload_nota = {
                "id_prueba": id_prueba_master,
                "estudiante": firma_estudiante,
                "puntaje_obtenido": round(nota_final, 2),
                "puntaje_maximo": puntaje_maximo,
                "porcentaje": round(porcentaje_rendimiento, 2)
            }

            try:
                supabase.table("respuestas_estudiantes").insert(payload_nota).execute()
                st.success(f"🎉 ¡ÉXITO TOTAL! Nota inyectada para {alumno_final}.")
                
                # 📡 LIMPIEZA LOGÍSTICA: Vaciamos la memoria tras la subida exitosa 
                if "imagen_satelital" in st.session_state:
                    st.session_state.imagen_satelital = None
                    st.session_state.nombre_imagen_satelital = None
                
                st.balloons()
                st.rerun() # Recargamos para dejar el panel limpio para el siguiente examen
            except Exception as ex:
                st.error(f"🚨 Falla transaccional: {ex}")

if __name__ == "__main__":
    pass
