import streamlit as st
import pandas as pd
from supabase import create_client

# =================================================================
# 🔒 CONEXIÓN AL BÚNKER DE DATOS INSTITUCIONAL
# =================================================================
def iniciar_conexion():
    url = st.secrets["SUPABASE_URL"].strip()
    key = st.secrets["SUPABASE_KEY"].strip()
    return create_client(url, key)

def ejecutar():
    # 🎨 INYECCIÓN VISUAL DE ALTA INGENIERÍA (GÉNESIS GOLDEN STYLING) - Tu diseño exacto
    st.markdown("""
        <style>
        .subtitulo-dorado {
            color: #d4af37;
            font-weight: bold;
            font-size: 14px;
            text-transform: uppercase;
            text-align: center;
            letter-spacing: 1px;
            margin-bottom: 25px;
        }
        .seccion-titulo {
            color: #0d1b2a;
            font-family: 'Arial Black', sans-serif;
            font-size: 24px;
            font-weight: bold;
            margin-top: 15px;
            margin-bottom: 15px;
        }
        
        /* Ajuste estricto de etiquetas de alto contraste */
        div[data-testid="stMainBlockContainer"] label p {
            color: #0d1b2a !important;
            font-weight: 800 !important;
            font-size: 12px !important;
            text-transform: uppercase;
        }
        div[data-baseweb="select"] {
            color: #0d1b2a !important;
            font-weight: bold !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<p class='subtitulo-dorado'>DISEÑO, ALMACENAMIENTO DE CLAVES DE RESPUESTAS Y GENERACIÓN AUTÓNOMA DE HOJAS OMR</p>", unsafe_allow_html=True)

    try:
        supabase = iniciar_conexion()
    except Exception:
        st.error("🚨 Falla en el enlace con el búnker de Supabase.")
        return

    # 📥 BARRIDO TÁCTICO EN SEGUNDO PLANO (Homologación de Datos)
    with st.spinner("Sincronizando catálogo oficial de asignaturas y grados desde el búnker..."):
        try:
            # 📡 Extracción de asignaturas de tu mina de 7,700 registros históricos
            res_consolidado = supabase.table("notas_consolidadas").select("ASIGNATURA").execute()
            materias_raw = res_consolidado.data if res_consolidado.data else []
            
            # 📡 Extracción paralela de grados de la matrícula real de alumnos
            estudiantes_base = []
            offset, chunk_size = 0, 1000
            while True:
                resultado = supabase.table("data_estudiantes").select('Grado').range(offset, offset + chunk_size - 1).execute()
                if not resultado.data: break
                estudiantes_base.extend(resultado.data)
                if len(resultado.data) < chunk_size: break
                offset += chunk_size
        except Exception as e:
            st.error(f"🚨 Error de sincronización perimetral: {e}")
            return

    # 🧮 Procesamiento y limpieza de Asignaturas Únicas
    if materias_raw:
        df_mat = pd.DataFrame(materias_raw)
        lista_materias = sorted(df_mat["ASIGNATURA"].dropna().astype(str).str.upper().str.strip().unique().tolist())
    else:
        lista_materias = ["MATEMÁTICAS", "CIENCIAS NATURALES", "LENGUAJE", "INGLÉS", "SOCIALES"]

    # 🧮 Procesamiento y limpieza de Grados Únicos de Matrícula
    if estudiantes_base:
        df_est = pd.DataFrame(estudiantes_base)
        df_est.columns = [col.lower() for col in df_est.columns]
        lista_grados = sorted(df_est["grado"].dropna().astype(str).str.upper().str.strip().unique().tolist())
    else:
        lista_grados = ["SEXTO A", "SÉPTIMO A", "OCTAVO A", "NOVENO A", "DÉCIMO A", "ONCE A"]

    # =================================================================
    # 🏛️ CONSOLA CENTRAL: CONFIGURACIÓN MÁSTER DE LA EVALUACIÓN
    # =================================================================
    with st.container(border=True):
        # Fila 1: Nombre de la evaluación y Grado Objetivo Dinámico
        r1_c1, r1_c2 = st.columns(2)
        with r1_c1:
            nombre_evaluacion = st.text_input("🎯 NOMBRE DE LA EVALUACIÓN:", placeholder="Ej: Bimestral Segundo Periodo").strip().upper()
        with r1_c2:
            grado_objetivo = st.selectbox("👥 CURSO / GRADO OBJETIVO:", lista_grados)

        # Fila 2: Asignatura Dinámica de Consolidados y Nota Máxima
        r2_c1, r2_c2 = st.columns(2)
        with r2_c1:
            # ⚡ ¡CAMBIO MAESTRO EFECTUADO! Ahora la lista se alimenta de tus 7,700 registros históricos reales
            asignatura = st.selectbox("🎨 ASIGNATURA / MATERIA:", lista_materias)
        with r2_c2:
            nota_maxima = st.number_input("💯 NOTA MÁXIMA CONFIGURADA:", min_value=1.0, max_value=10.0, value=5.0, step=0.1)

        # Fila 3: Tipo de Evaluación y Periodo Académico
        r3_c1, r3_c2 = st.columns(2)
        with r3_c1:
            tipo_evaluacion = st.selectbox("📝 TIPO DE EVALUACIÓN:", ["QUIZ", "EVALUACIÓN PARCIAL", "EVALUACIÓN BIMESTRAL", "TALLER EVALUATIVO"])
        with r3_c2:
            periodo_academico = st.selectbox("📂 PERIODO ACADÉMICO:", ["PRIMER PERIODO", "SEGUNDO PERIODO", "TERCER PERIODO", "CUARTO PERIODO"])

    # =================================================================
    # 🔑 MATRIZ DE RESPUESTAS CORRECTAS (20 PREGUNTAS MÁXIMAS)
    # =================================================================
    st.markdown("<p class='seccion-titulo'>🔑 Matriz Clave de Respuestas Correctas (20 Preguntas Máximas):</p>", unsafe_allow_html=True)
    st.info("💡 Marque la opción correcta para cada pregunta. Si su examen tiene menos de 20 preguntas, deje las sobrantes en la opción 'N/A' e ignore esas filas.")

    opciones_abc = ["A", "B", "C", "D", "E", "N/A"]
    claves_seleccionadas = {}

    for i in range(1, 21):
        if (i - 1) % 4 == 0:
            cols_matriz = st.columns(4)
        
        id_columna = (i - 1) % 4
        with cols_matriz[id_columna]:
            claves_seleccionadas[f"p{i}"] = st.selectbox(f"PREGUNTA {i:02d}:", opciones_abc, index=0, key=f"key_p_{i}")

    # =================================================================
    # 💾 PROCESADOR DE ALMACENAMIENTO EN EL BÚNKER
    # =================================================================
    st.markdown("---")
    boton_guardar_prueba = st.button("🚀 SALVAGUARDAR EVALUACIÓN MÁSTER EN EL BÚNKER", use_container_width=True, type="primary")

    if boton_guardar_prueba:
        if not nombre_evaluacion:
            st.error("❌ Operación rechazada: Debe asignarle un nombre a la evaluación para poder guardarla.")
        else:
            preguntas_reales = [val for val in claves_seleccionadas.values() if val != "N/A"]
            total_preguntas = len(preguntas_reales)

            if total_preguntas == 0:
                st.error("❌ Operación rechazada: No puede registrar una prueba con 0 preguntas activas.")
                return

            payload_prueba = {
                "nombre": f"{tipo_evaluacion} - {nombre_evaluacion} ({periodo_academico})",
                "materia": asignatura,
                "grado": grado_objetivo,
                "puntaje_maximo": nota_maxima,
                "total_preguntas": total_preguntas,
                "clave_respuestas": claves_seleccionadas
            }

            with st.spinner("Inyectando configuración criptográfica de examen..."):
                try:
                    supabase.table("pruebas_maestras").insert(payload_prueba).execute()
                    st.success(f"🎉 ¡COMPLETADO IMPECABLE! El examen de {asignatura} fue indexado con éxito para el curso {grado_objetivo}.")
                    st.balloons()
                except Exception as e:
                    st.error(f"🚨 Falla en el búnker de Supabase: {e}")

if __name__ == "__main__":
    pass
