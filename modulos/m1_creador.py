import streamlit as st
from estilos_globales import inyectar_estilos_omega
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
    # ⚡ Inyección visual unificada Génesis Omega Pro (Prioridad Alta)
    inyectar_estilos_omega()
    
    # ✨ TÍTULOS BLINDADOS (Estándar Industrial Omega)
    st.markdown("<h1 class='titulo-dash'>📝 CREADOR Y DISEÑADOR DE PRUEBAS</h1>", unsafe_allow_html=True)
    st.markdown("<h3 class='subtitulo-dash'>Diseño, Almacenamiento de Claves y Generación de Hojas OMR</h3>", unsafe_allow_html=True)
    st.markdown("---")

    try:
        supabase = iniciar_conexion()
    except Exception:
        st.error("🚨 Falla en el enlace con el búnker de Supabase.")
        return

    # 📥 BARRIDO TÁCTICO EN SEGUNDO PLANO
    with st.spinner("Sincronizando catálogo oficial..."):
        try:
            res_consolidado = supabase.table("notas_consolidadas").select("ASIGNATURA").execute()
            materias_raw = res_consolidado.data if res_consolidado.data else []
            
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

    # 🧮 Procesamiento de listas
    lista_materias = sorted(pd.DataFrame(materias_raw)["ASIGNATURA"].dropna().unique().tolist()) if materias_raw else ["MATEMÁTICAS", "CIENCIAS", "LENGUAJE"]
    lista_grados = sorted(pd.DataFrame(estudiantes_base)["Grado"].dropna().unique().tolist()) if estudiantes_base else ["SEXTO A", "SÉPTIMO A"]

    # 🏛️ CONSOLA CENTRAL
    with st.container(border=True):
        r1_c1, r1_c2 = st.columns(2)
        with r1_c1: nombre_evaluacion = st.text_input("🎯 NOMBRE DE LA EVALUACIÓN:", placeholder="Ej: Bimestral Segundo Periodo").strip().upper()
        with r1_c2: grado_objetivo = st.selectbox("👥 CURSO / GRADO OBJETIVO:", lista_grados)

        r2_c1, r2_c2 = st.columns(2)
        with r2_c1: asignatura = st.selectbox("🎨 ASIGNATURA / MATERIA:", lista_materias)
        with r2_c2: nota_maxima = st.number_input("💯 NOTA MÁXIMA:", min_value=1.0, max_value=10.0, value=5.0, step=0.1)

        r3_c1, r3_c2 = st.columns(2)
        with r3_c1: tipo_evaluacion = st.selectbox("📝 TIPO:", ["QUIZ", "PARCIAL", "BIMESTRAL", "TALLER"])
        with r3_c2: periodo_academico = st.selectbox("📂 PERIODO:", ["PRIMER PERIODO", "SEGUNDO PERIODO", "TERCER PERIODO", "CUARTO PERIODO"])

    # 🔑 MATRIZ DE RESPUESTAS
    st.markdown("<h3 class='subtitulo-dash'>🔑 Matriz Clave de Respuestas (20 Preguntas):</h3>", unsafe_allow_html=True)
    st.info("💡 Marque la opción correcta para cada pregunta. Deje en 'N/A' las no utilizadas.")

    claves_seleccionadas = {}
    for i in range(1, 21):
        if (i - 1) % 4 == 0: cols_matriz = st.columns(4)
        with cols_matriz[(i - 1) % 4]:
            claves_seleccionadas[f"p{i}"] = st.selectbox(f"PREGUNTA {i:02d}:", ["A", "B", "C", "D", "E", "N/A"], key=f"key_p_{i}")

    # 💾 SALVAGUARDA
    st.markdown("---")
    if st.button("🚀 SALVAGUARDAR EVALUACIÓN EN EL BÚNKER", use_container_width=True, type="primary"):
        if not nombre_evaluacion:
            st.error("❌ Debe asignar un nombre a la evaluación.")
        else:
            payload = {
                "nombre": f"{tipo_evaluacion} - {nombre_evaluacion} ({periodo_academico})",
                "materia": asignatura, "grado": grado_objetivo,
                "puntaje_maximo": nota_maxima, "total_preguntas": len([v for v in claves_seleccionadas.values() if v != "N/A"]),
                "clave_respuestas": claves_seleccionadas
            }
            try:
                supabase.table("pruebas_maestras").insert(payload).execute()
                st.success("🎉 ¡ÉXITO! Examen indexado.")
                st.balloons()
            except Exception as e:
                st.error(f"🚨 Falla en el búnker: {e}")

if __name__ == "__main__":
    ejecutar()
