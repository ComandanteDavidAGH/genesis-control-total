import streamlit as st
from estilos_globales import inyectar_estilos_omega  # <--- ESTA ES LA LÍNEA NUEVA
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
    # ⚡ Inyección visual unificada Génesis Omega Pro
    inyectar_estilos_omega()

    # ==========================================
    # 📊 ENCABEZADO PRINCIPAL DE ALTO IMPACTO
    # ==========================================
    st.markdown("<h1 style='text-align: center; color: #0F172A; font-size: 3rem;'>⌨️ Ingreso Manual de Calificaciones</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2rem; color: #D97706; font-weight: bold; letter-spacing: 1px;'>MÓDULO DE DIGITACIÓN DIRECTA Y SINCRONIZACIÓN EN TIEMPO REAL</p>", unsafe_allow_html=True)
    st.markdown("---")

    try:
        supabase = iniciar_conexion()
    except Exception:
        st.error("🚨 Falla en el enlace satelital con Supabase.")
        return

    # 📥 EXTRACCIÓN MAESTRA EN RÁFAGAS
    with st.spinner("Sincronizando el ecosistema de asignaturas y cursos oficiales..."):
        try:
            # 📡 Traemos las materias de la mina de históricos
            res_consolidado = supabase.table("notas_consolidadas").select("ASIGNATURA").execute()
            materias_raw = res_consolidado.data if res_consolidado.data else []
            
            # 📡 Traemos la lista completa de matrículas (paginación de 1000 en 1000)
            estudiantes_base = []
            offset, chunk_size = 0, 1000
            while True:
                resultado = supabase.table("data_estudiantes").select('Nombre_Completo, Grado').range(offset, offset + chunk_size - 1).execute()
                if not resultado.data: break
                estudiantes_base.extend(resultado.data)
                if len(resultado.data) < chunk_size: break
                offset += chunk_size
        except Exception as e:
            st.error(f"🚨 Error de lectura en el búnker de datos: {e}")
            return

    # 🧮 NORMALIZACIÓN Y LIMPIEZA DE ASIGNATURAS
    if materias_raw:
        df_mat = pd.DataFrame(materias_raw)
        lista_materias = sorted(df_mat["ASIGNATURA"].dropna().astype(str).str.upper().str.strip().unique().tolist())
    else:
        lista_materias = ["MATEMÁTICAS", "CIENCIAS NATURALES", "LENGUAJE", "INGLÉS", "SOCIALES"]

    # 🧮 CONVERSIÓN DE LA MATRÍCULA A DATAFRAME SEGURO
    if estudiantes_base:
        df_est = pd.DataFrame(estudiantes_base)
        # Forzamos minúsculas internas en las columnas de Pandas para no sufrir por mayúsculas
        df_est.columns = [col.lower() for col in df_est.columns]
        df_est["grado"] = df_est["grado"].dropna().astype(str).str.upper().str.strip()
        df_est["nombre_completo"] = df_est["nombre_completo"].dropna().astype(str).str.upper().str.strip()
        
        # Extraemos la lista oficial de cursos reales que contienen alumnos
        lista_grados_disponibles = sorted(df_est["grado"].unique().tolist())
    else:
        df_est = pd.DataFrame()
        lista_grados_disponibles = ["3°", "SEXTO A", "SÉPTIMO A"]

    # =================================================================
    # 🏛️ DESPLIEGUE DEL NUEVO FORMULARIO ESTRUCTURADO
    # =================================================================
    st.markdown("### ⚙️ PASO 1: Parámetros del Examen")
    with st.container(border=True):
        c1, c2 = st.columns(2)
        with c1:
            materia_seleccionada = st.selectbox("🎯 ASIGNATURA / MATERIA CORRESPONDIENTE:", lista_materias)
        with c2:
            grado_seleccionado = st.selectbox("👥 CURSO / GRADO A CALIFICAR:", lista_grados_disponibles)

    st.markdown("### 👤 PASO 2: Selección y Resultados")
    with st.container(border=True):
        c3, c4 = st.columns(2)
        with c3:
            # FILTRADO INTELIGENTE: Extraemos solo los alumnos que pertenecen al grado seleccionado
            if not df_est.empty:
                df_alumnos_filtrados = df_est[df_est["grado"] == grado_seleccionado]
                lista_alumnos_final = sorted(df_alumnos_filtrados["nombre_completo"].unique().tolist())
                
                if not lista_alumnos_final:
                    lista_alumnos_final = ["SIN ALUMNOS EN ESTE GRADO"]
            else:
                lista_alumnos_final = ["NO HAY ALUMNOS EN MATRÍCULA"]

            alumno_sel = st.selectbox("👤 NOMBRE DEL ESTUDIANTE:", lista_alumnos_final)
            
        with c4:
            max_questions = st.number_input("📋 CANTIDAD TOTAL DE PREGUNTAS:", min_value=1, max_value=100, value=10, step=1)

    # =================================================================
    # 🧮 PANEL DE CONTEO DE ACIERTOS Y CÓMPUTO AUTOMÁTICO
    # =================================================================
    st.markdown("---")
    
    cc1, cc2 = st.columns([1, 1.5])
    
    with cc1:
        aciertos = st.number_input(
            f"✍ ACIERTOS OBTENIDOS (MÁX: {max_questions}):",
            min_value=0,
            max_value=int(max_questions),
            value=0,
            step=1
        )
        
        porcentaje_rendimiento = (aciertos / max_questions) * 100 if max_questions > 0 else 0.0
        nota_proyectada = (aciertos / max_questions) * 5.0 if max_questions > 0 else 0.0

    with cc2:
        st.markdown(f"""
            <div style="background-color: #0d1b2a; padding: 15px; border-radius: 6px; text-align: center; border-left: 4px solid #d4af37; border: 2px solid #0d1b2a; margin-top: 25px;">
                <div style="display: flex; justify-content: space-around; align-items: center;">
                    <div>
                        <p style="margin:0; font-size:11px; color:#d4af37; font-weight:bold;">RENDIMIENTO</p>
                        <p style="margin:5px 0 0 0; font-size:26px; color:white; font-family:'Arial Black';">{porcentaje_rendimiento:.1f}%</p>
                    </div>
                    <div style="border-left: 1px solid rgba(255,255,255,0.2); padding-left:20px;">
                        <p style="margin:0; font-size:11px; color:#d4af37; font-weight:bold;">NOTA PROYECTADA</p>
                        <p style="margin:5px 0 0 0; font-size:26px; color:#00ff66; font-family:'Arial Black';">{nota_proyectada:.2f} / 5.0</p>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    boton_inyectar = st.button("🚀 INYECTAR CALIFICACIÓN AL BÚNKER DE DATOS", use_container_width=True, type="primary")

    if boton_inyectar:
        if alumno_sel in ["NO HAY ALUMNOS EN MATRÍCULA", "SIN ALUMNOS EN ESTE GRADO"]:
            st.error("❌ Operación denegada: Selección de estudiante inválida.")
            return

        # Firma institucional exacta exigida por las planillas: "NOMBRE (GRADO)"
        firma_estudiante = f"{alumno_sel} ({grado_seleccionado})"

        payload_nota = {
            "id_prueba": 1,  
            "estudiante": firma_estudiante,
            "puntaje_obtenido": round(nota_proyectada, 2),
            "puntaje_maximo": 5.0,
            "porcentaje": round(porcentaje_rendimiento, 2)
        }

        with st.spinner("Asentando registros en caliente dentro del búnker..."):
            try:
                supabase.table("respuestas_estudiantes").insert(payload_nota).execute()
                st.success(f"🎯 ¡IMPACTO EXITOSO! Calificación asentada para {alumno_sel} ({grado_seleccionado}) en la asignatura {materia_seleccionada}.")
                st.balloons()
            except Exception as error_db:
                st.error(f"🚨 Falla en el volcado transaccional: {error_db}")

if __name__ == "__main__":
    pass
