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
    
    # ==========================================
    # 📊 ENCABEZADO PRINCIPAL DE ALTO IMPACTO
    # ==========================================
    st.markdown("<h1 style='text-align: center; color: #0F172A; font-size: 3rem;'>📝 Creador y Diseñador de Pruebas</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2rem; color: #D97706; font-weight: bold; letter-spacing: 1px;'>DISEÑO, ALMACENAMIENTO DE CLAVES Y GENERACIÓN DE MATRICES</p>", unsafe_allow_html=True)
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

    # =================================================================
    # 🏛️ PASO 1: CONSOLA CENTRAL DE CONFIGURACIÓN
    # =================================================================
    st.markdown("### ⚙️ PASO 1: Configuración de la Evaluación")
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

    # =================================================================
    # 🔑 PASO 2: MATRIZ DE RESPUESTAS
    # =================================================================
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🔑 PASO 2: Matriz Clave de Respuestas (Hasta 20 Ítems)")
    st.info("💡 Marque la opción correcta para cada pregunta. Deje en 'N/A' las preguntas no utilizadas para que el sistema las ignore automáticamente.")

    claves_seleccionadas = {}
    with st.container(border=True):
        for i in range(1, 21):
            if (i - 1) % 4 == 0: cols_matriz = st.columns(4)
            with cols_matriz[(i - 1) % 4]:
                claves_seleccionadas[f"p{i}"] = st.selectbox(f"PREGUNTA {i:02d}:", ["A", "B", "C", "D", "E", "N/A"], key=f"key_p_{i}")

    # =================================================================
    # 💾 PASO 3: SALVAGUARDA EN LA BASE DE DATOS
    # =================================================================
    st.markdown("---")
    
    # Pre-cálculo de preguntas activas para retroalimentación visual
    preguntas_activas = len([v for v in claves_seleccionadas.values() if v != "N/A"])
    
    if st.button(f"🚀 SALVAGUARDAR EVALUACIÓN EN EL BÚNKER ({preguntas_activas} Preguntas)", use_container_width=True, type="primary"):
        if not nombre_evaluacion:
            st.error("❌ Debe asignar un nombre válido a la evaluación antes de continuar.")
        elif preguntas_activas == 0:
            st.error("❌ No puede crear una evaluación con 0 preguntas válidas.")
        else:
            payload = {
                "nombre": f"{tipo_evaluacion} - {nombre_evaluacion} ({periodo_academico})",
                "materia": asignatura, 
                "grado": grado_objetivo,
                "puntaje_maximo": nota_maxima, 
                "total_preguntas": preguntas_activas,
                "clave_respuestas": claves_seleccionadas
            }
            try:
                supabase.table("pruebas_maestras").insert(payload).execute()
                st.success(f"🎉 ¡ÉXITO TOTAL! Examen indexado con {preguntas_activas} preguntas activas.")
                st.balloons()
            except Exception as e:
                st.error(f"🚨 Falla en el búnker transaccional: {e}")

if __name__ == "__main__":
    ejecutar()
