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
    # 🎨 INJECTION VISUAL (GÉNESIS HIGH-CONTRAST DESIGN) - Tu estilo intacto
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

    # 📥 EXTRACCIÓN MAESTRA DESDE LAS DOS TABLAS EN VIVO
    with st.spinner("Realizando barrido analítico de asignaturas en 7,700 registros..."):
        try:
            # 📡 BARRIDO TÁCTICO: Traemos las materias directamente de 'notas_consolidadas'
            res_consolidado = supabase.table("notas_consolidadas").select("ASIGNATURA").execute()
            materias_raw = res_consolidado.data if res_consolidado.data else []
            
            # Descarga paralela de la matrícula de estudiantes (de 1000 en 1000)
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

    # 🧮 PROCESAMIENTO DE ASIGNATURAS ÚNICAS
    if materias_raw:
        df_mat = pd.DataFrame(materias_raw)
        # Limpiamos y extraemos valores únicos de la columna ASIGNATURA (Mayúsculas de la imagen)
        lista_materias = sorted(df_mat["ASIGNATURA"].dropna().astype(str).str.upper().str.strip().unique().tolist())
    else:
        lista_materias = ["MATEMÁTICAS", "CIENCIAS NATURALES", "LENGUAJE", "INGLÉS", "SOCIALES"]

    # PROCESAMIENTO DE ESTUDIANTADO Y GRADOS AUTOMÁTICOS
    diccionario_alumnos_grados = {}
    if estudiantes_base:
        for e in estudiantes_base:
            nom = str(e.get("Nombre_Completo", "")).strip().upper()
            gra = str(e.get("Grado", "GENERAL")).strip().upper()
            if nom:
                diccionario_alumnos_grados[nom] = gra
        lista_alumnos = sorted(list(diccionario_alumnos_grados.keys()))
    else:
        lista_alumnos = ["NO HAY ALUMNOS EN MATRÍCULA"]

    # =================================================================
    # 🏛️ DESPLIEGUE DE CONFIGURACIÓN DE CARGA DIRECTA
    # =================================================================
    with st.container(border=True):
        c1, c2 = st.columns(2)
        
        with c1:
            # Ahora la lista se alimenta de tus 7,700 registros históricos
            materia_seleccionada = st.selectbox("🎯 ASIGNATURA / MATERIA CORRESPONDIENTE:", lista_materias)
            
            # Selector de límite de preguntas para el cálculo de notas
            max_preguntas = st.number_input("📋 CANTIDAD DE PREGUNTAS DEL EXAMEN:", min_value=1, max_value=100, value=10, step=1)

        with c2:
            alumno_sel = st.selectbox("👤 NOMBRE DEL ESTUDIANTE:", lista_alumnos)
            
            # ⚡ DETECTOR AUTOMÁTICO: Extrae el grado real del alumno seleccionado al vuelo
            grado_automatico = diccionario_alumnos_grados.get(alumno_sel, "GENERAL")
            st.selectbox("👥 CURSO / GRADO DEL ALUMNO:", [grado_automatico], disabled=True)

    # =================================================================
    # 🧮 PANEL DE CONTEO DE ACIERTOS Y CÓMPUTO AUTOMÁTICO
    # =================================================================
    st.markdown("### 🎮 Entrada de Aciertos Reales")
    
    cc1, cc2 = st.columns([1.5, 1])
    
    with cc1:
        aciertos = st.number_input(
            f"✍️ RESPUESTAS CORRECTAS LOGRADAS (MÁXIMO: {max_preguntas}):",
            min_value=0,
            max_value=max_preguntas,
            value=0,
            step=1
        )
        
        # Fórmulas máster de conversión sobre base 5.0
        porcentaje_rendimiento = (aciertos / max_preguntas) * 100 if max_preguntas > 0 else 0.0
        nota_proyectada = (aciertos / max_preguntas) * 5.0 if max_preguntas > 0 else 0.0

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
        if alumno_sel == "NO HAY ALUMNOS EN MATRÍCULA":
            st.error("❌ Operación denegada: Registro de estudiante inválido.")
            return

        # Formato unificado de firma para las planillas: "NOMBRE (GRADO)"
        firma_estudiante = f"{alumno_sel} ({grado_automatico})"

        payload_nota = {
            "id_prueba": 1,  # ID comodín de compatibilidad con tu tabla Delaware
            "estudiante": firma_estudiante,
            "puntaje_obtenido": round(nota_proyectada, 2),
            "puntaje_maximo": 5.0,
            "porcentaje": round(porcentaje_rendimiento, 2)
        }

        with st.spinner("Volcando registros en caliente dentro del búnker..."):
            try:
                supabase.table("respuestas_estudiantes").insert(payload_nota).execute()
                st.success(f"🎯 ¡IMPACTO EXITOSO! Calificación asentada para {alumno_sel} en la materia {materia_seleccionada}.")
                st.balloons()
            except Exception as error_db:
                st.error(f"🚨 Falla en el volcado transaccional: {error_db}")

if __name__ == "__main__":
    pass
