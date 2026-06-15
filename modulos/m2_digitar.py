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
    # 🎨 INJECTION VISUAL (GÉNESIS HIGH-CONTRAST DESIGN) - Tu estilo premium intacto
    st.markdown("""
        <style>
        .titulo-nasa { color: #0d1b2a; font-family: 'Arial Black'; font-size: 34px; margin-bottom: 0px; }
        .subtitulo-nasa { color: #d4af37; font-weight: bold; font-size: 13px; text-transform: uppercase; margin-top: 0px; }
        
        /* Contenedores de Formulario Premium */
        div[data-testid="stMainBlockContainer"] label p {
            color: #0d1b2a !important; font-weight: 800 !important; font-size: 12px !important; text-transform: uppercase;
        }
        div[data-baseweb="select"] {
            color: #0d1b2a !important; font-weight: bold !important;
        }
        
        /* HUD de Rendimiento en Tiempo Real */
        .hud-digitar {
            background: linear-gradient(135deg, #0d1b2a 0%, #1a365d 100%);
            border-radius: 6px; padding: 15px; color: white; text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<p class='titulo-nasa'>📝 Formato de Carga Directa</p>", unsafe_allow_html=True)
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
    # 🏛️ DESPLIEGUE DEL NUEVO FORMULARIO COMANDADO POR CURSO
    # =================================================================
    with st.container(border=True):
        c1, c2 = st.columns(2)
        
        with c1:
            # 1. El docente selecciona la materia
            materia_seleccionada = st.selectbox("🎯 ASIGNATURA / MATERIA CORRESPONDIENTE:", lista_materias)
            
            # 2. El docente elige el Grado que va a dictar (¡Mando restaurado!)
            grado_seleccionado = st.selectbox("👥 CURSO / GRADO A CALIFICAR:", lista_grados_disponibles)

        with c2:
            # 3. FILTRADO INTELIGENTE: Extraemos solo los alumnos que pertenecen al grado seleccionado
            if not df_est.empty:
                df_alumnos_filtrados = df_est[df_est["grado"] == grado_seleccionado]
                lista_alumnos_final = sorted(df_alumnos_filtrados["nombre_completo"].unique().tolist())
                
                if not lista_alumnos_final:
                    lista_alumnos_final = ["SIN ALUMNOS EN ESTE GRADO"]
            else:
                lista_alumnos_final = ["NO HAY ALUMNOS EN MATRÍCULA"]

            # El selector ahora es una delicia: solo muestra los niños de ese salón específico
            alumno_sel = st.selectbox("👤 NOMBRE DEL ESTUDIANTE:", lista_alumnos_final)
            
            # Selector estático de control de ítems
            max_questions = st.number_input("📋 CANTIDAD DE PREGUNTAS DEL EXAMEN:", min_value=1, max_value=100, value=10, step=1)

    # =================================================================
    # 🧮 PANEL DE CONTEO DE ACIERTOS Y CÓMPUTO AUTOMÁTICO
    # =================================================================
    st.markdown("### 🎮 Entrada de Aciertos Reales")
    
    cc1, cc2 = st.columns([1.5, 1])
    
    with cc1:
        aciertos = st.number_input(
            f"✍ *RESPUESTAS CORRECTAS LOGRADAS (MÁXIMO: {max_questions}):*",
            min_value=0,
            max_value=int(max_questions),
            value=0,
            step=1
        )
        
        porcentaje_rendimiento = (aciertos / max_questions) * 100 if max_questions > 0 else 0.0
        nota_proyectada = (aciertos / max_questions) * 5.0 if max_questions > 0 else 0.0

    with cc2:
        st.markdown(f"""
            <div class="hud-digitar">
                <div style="display: flex; justify-content: space-around;">
                    <div>
                        <p style="margin:0; font-size:11px; color:#d4af37; font-weight:bold;">RENDIMIENTO</p>
                        <p style="margin:5px 0 0 0; font-size:24px; font-family:'Arial Black';">{porcentaje_rendimiento:.1f}%</p>
                    </div>
                    <div style="border-left: 1px solid rgba(255,255,255,0.2); padding-left:15px;">
                        <p style="margin:0; font-size:11px; color:#d4af37; font-weight:bold;">NOTA PROYECTADA</p>
                        <p style="margin:5px 0 0 0; font-size:24px; font-family:'Arial Black'; color:#00ff66;">{nota_proyectada:.2f} / 5.0</p>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
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
