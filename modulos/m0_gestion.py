import streamlit as st
import pandas as pd
from supabase import create_client, Client

# =================================================================
# 🔒 CONEXIÓN AL BÚNKER DE DATOS INSTITUCIONAL
# =================================================================
def iniciar_conexion():
    url = st.secrets["SUPABASE_URL"].strip()
    key = st.secrets["SUPABASE_KEY_REAL"].strip() if "SUPABASE_KEY_REAL" in st.secrets else st.secrets["SUPABASE_KEY"].strip()
    return create_client(url, key)

def ejecutar():
    # 🎨 INYECCIÓN VISUAL DE ALTA GAMA (GÉNESIS STUDENT HUB)
    st.markdown("""
        <style>
        .titulo-portal { color: #0d1b2a; font-family: 'Arial Black'; font-size: 34px; margin-bottom: 0px; }
        .subtitulo-portal { color: #d4af37; font-weight: bold; font-size: 13px; text-transform: uppercase; margin-top: 0px; }
        
        /* HUD de Estado del Estudiante */
        .hud-estudiante {
            background: linear-gradient(135deg, #0d1b2a 0%, #1e3a8a 100%);
            padding: 15px; border-radius: 8px; color: white; font-weight: bold;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.15); margin-bottom: 25px;
        }
        
        /* Ajuste de tipografía para selectores */
        .stSelectbox label p { color: #0d1b2a !important; font-weight: 800 !important; text-transform: uppercase; }
        div[data-baseweb="select"] { color: #0d1b2a !important; font-weight: bold !important; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<p class='titulo-portal'>👤 Portal de Evaluación Estudiantil</p>", unsafe_allow_html=True)
    st.markdown("<p class='subtitulo-portal'>Consulta Autónoma de Rendimiento Académico e Historial de Calificaciones</p>", unsafe_allow_html=True)
    st.markdown("---")

    try:
        supabase = iniciar_conexion()
    except Exception:
        st.error("⚠️ Error de enlace satelital con el búnker central.")
        return

    # =================================================================
    # 📡 EXTRACCIÓN Y COMPILACIÓN DE RÁFAGAS DE MATRÍCULAS
    # =================================================================
    estudiantes_base = []
    with st.spinner("Sincronizando listas de acceso estudiantil..."):
        try:
            offset = 0
            chunk_size = 1000  
            while True:
                resultado = supabase.table("data_estudiantes").select('Nombre_Completo, Grado').range(offset, offset + chunk_size - 1).execute()
                if not resultado.data: break
                estudiantes_base.extend(resultado.data)
                if len(resultado.data) < chunk_size: break
                offset += chunk_size  
                
            res_pruebas = supabase.table("pruebas_maestras").select("id_prueba, nombre, materia").execute()
            pruebas_dict = {str(p['id_prueba']): f"{p['nombre']} ({p['materia']})".upper() for p in res_pruebas.data} if res_pruebas.data else {}
            
        except Exception as e:
            st.error(f"🚨 Falla en la descarga de credenciales: {e}")
            return

    if not estudiantes_base:
        st.info("📭 No hay estudiantes registrados en la matrícula general actualmente.")
        return

    df_matricula = pd.DataFrame(estudiantes_base)
    df_matricula['Grado'] = df_matricula['Grado'].str.upper().str.strip()
    df_matricula['Nombre_Completo'] = df_matricula['Nombre_Completo'].str.upper().str.strip()
    
    lista_grados = sorted(df_matricula['Grado'].unique().tolist())

    # =================================================================
    # 🗂️ FILTRADO ANIDADO DE IDENTIDAD SEGURA
    # =================================================================
    with st.container(border=True):
        st.markdown("### 🔐 Validación de Credenciales de Acceso")
        c1, c2 = st.columns(2)
        with c1:
            grado_sel = st.selectbox("1. SELECCIONE SU CURSO / GRADO:", lista_grados)
        with c2:
            alumnos_filtrados = sorted(df_matricula[df_matricula['Grado'] == grado_sel]['Nombre_Completo'].tolist())
            alumno_sel = st.selectbox("2. SELECCIONE SU NOMBRE COMPLETO:", alumnos_filtrados)

    if not alumno_sel:
        return

    # =================================================================
    # 🔍 BÚSQUEDA DE LOGROS ACADÉMICOS EN EL BÚNKER DE NOTAS
    # =================================================================
    firma_estudiante_busqueda = f"{alumno_sel} ({grado_sel})"

    with st.spinner("Extrayendo historial de calificaciones..."):
        try:
            res_notas = supabase.table("respuestas_estudiantes").select("*").eq("estudiante", firma_estudiante_busqueda).execute()
            notas_alumno = res_notas.data
        except Exception as e:
            st.error(f"Error al compilar el boletín: {e}")
            return

    if not notas_alumno:
        st.warning(f"📋 El estudiante '{alumno_sel}' no registra calificaciones procesadas en el período actual.")
        return

    # =================================================================
    # 🧮 PROCESAMIENTO MATEMÁTICO SEGURO ANTI-NULLS
    # =================================================================
    filas_boletin = []
    suma_porcentajes = 0.0
    validos = 0

    for fila in notas_alumno:
        id_p = str(fila.get('id_prueba', ''))
        nombre_examen = pruebas_dict.get(id_p, "EVALUACIÓN ACADÉMICA")

        raw_pct = fila.get('porcentaje')
        pct = float(raw_pct) if raw_pct is not None and str(raw_pct).strip().lower() not in ['none', 'null', ''] else 0.0

        raw_nota = fila.get('puntaje_obtenido')
        nota = float(raw_nota) if raw_nota is not None and str(raw_nota).strip().lower() not in ['none', 'null', ''] else 0.0

        raw_max = fila.get('puntaje_maximo')
        max_p = float(raw_max) if raw_max is not None and str(raw_max).strip().lower() not in ['none', 'null', ''] else 5.0

        estado_materia = "APROBADO ✅" if pct >= 60.0 else "AFECTADO ❌"
        
        suma_porcentajes += pct
        validos += 1

        filas_boletin.append({
            "EVALUACIÓN / ASIGNATURA": nombre_examen,
            "PUNTAJE LOGRADO": round(nota, 2),
            "PUNTAJE MÁXIMO": round(max_p, 2),
            "RENDIMIENTO": f"{pct:.1f}%",
            "ESTADO": estado_materia
        })

    promedio_efectividad = (suma_porcentajes / validos) if validos > 0 else 0.0

    # =================================================================
    # 📊 PANEL EJECUTIVO DE VISUALIZACIÓN DE RESULTADOS
    # =================================================================
    st.markdown("---")
    st.markdown(f"### 📋 Boleta Digital de Calificaciones: {alumno_sel}")
    
    st.markdown(f"""
        <div class="hud-estudiante">
            <div style="display: flex; justify-content: space-between; text-align: center;">
                <div><p style="margin:0; font-size:11px; color:#d4af37; text-transform:uppercase;">Evaluaciones Realizadas</p><p style="margin:5px 0 0 0; font-size:20px;">{validos} Exámenes</p></div>
                <div><p style="margin:0; font-size:11px; color:#d4af37; text-transform:uppercase;">Promedio General</p><p style="margin:5px 0 0 0; font-size:20px;">{promedio_efectividad:.1f}%</p></div>
                <div><p style="margin:0; font-size:11px; color:#d4af37; text-transform:uppercase;">Estado del Perímetro</p><p style="margin:5px 0 0 0; font-size:20px; color: {'#00ff66' if promedio_efectividad >= 60.0 else '#ff3333'};">{'VIGENTE CORRIENTE' if promedio_efectividad >= 60.0 else 'ALERTA DE REFUERZO'}</p></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    df_boletin = pd.DataFrame(filas_boletin)
    st.dataframe(df_boletin, use_container_width=True, hide_index=True)

    if promedio_efectividad >= 85.0:
        st.success("🏆 **¡Excelente Desempeño Academic!** Tus niveles de efectividad están en el rango superior. Mantén la disciplina en el perímetro.")
    elif 60.0 <= promedio_efectividad < 85.0:
        st.info("👍 **Progreso Estable:** Tus evaluaciones se encuentran en el rango aprobado. Continúa repasando para asegurar los objetivos del período.")
    else:
        st.error("🚨 **Alerta Operativa:** Tu promedio general se encuentra por debajo del umbral óptimo de aprobación. Se sugerirá un plan de refuerzo inmediato.")
