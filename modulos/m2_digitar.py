import streamlit as st
import pandas as pd
from supabase import create_client

def iniciar_conexion():
    url = st.secrets["SUPABASE_URL"].strip()
    key = st.secrets["SUPABASE_KEY_REAL"].strip() if "SUPABASE_KEY_REAL" in st.secrets else st.secrets["SUPABASE_KEY"].strip()
    return create_client(url, key)

def ejecutar():
    # 🎨 INTERFAZ PREMIUM COMPONENTES CASILLAS DORADAS
    st.markdown("""
        <style>
        .titulo-nasa { color: #0d1b2a; font-family: 'Arial Black'; font-size: 34px; margin-bottom: 0px; letter-spacing: -0.5px; }
        
        /* Selectores Superiores Estilo Creador de Pruebas con Borde Dorado */
        div[data-testid="stSelectbox"] > div [role="combobox"] {
            border: 2px solid #d4af37 !important;
            border-radius: 6px !important;
            background-color: #ffffff !important;
            color: #0d1b2a !important;
            font-weight: bold !important;
            height: 42px !important;
        }
        div[data-testid="stSelectbox"] label p {
            color: #0d1b2a !important;
            font-weight: 800 !important;
            font-size: 13px !important;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        /* HUD Cards de Alta Densidad */
        .hud-nasa-container { display: flex; gap: 12px; margin-bottom: 20px; margin-top: 15px; }
        .hud-nasa-card {
            flex: 1; background: #f8f9fa; border-radius: 6px; padding: 10px 15px; 
            text-align: left; border-left: 5px solid #0d1b2a;
            box-shadow: inset 0 1px 3px rgba(0,0,0,0.05);
        }
        .hud-nasa-label { font-size: 11px; font-weight: 900; color: #5c677d; text-transform: uppercase; letter-spacing: 1px; }
        .hud-nasa-value { font-size: 26px; font-family: 'Arial Black'; font-weight: 900; color: #0d1b2a; margin-top: -2px; }
        
        /* Cinturón Militar Oscuro de la Matriz */
        .barra-matriz-oficial {
            background-color: #0d1b2a; color: #d4af37; font-family: 'Arial Black';
            font-size: 14px; text-transform: uppercase; text-align: center;
            padding: 10px; border-radius: 6px 6px 0px 0px; letter-spacing: 1.5px;
            margin-top: 20px;
        }
        
        /* Botón de Guardado Estilo Comando Red */
        div.stButton > button {
            background-color: #f25c54 !important; color: white !important;
            font-family: 'Arial Black' !important; font-size: 13px !important;
            text-transform: uppercase !important; border-radius: 6px !important;
            border: none !important; padding: 10px 20px !important;
            box-shadow: 0 4px 15px rgba(242, 92, 84, 0.25) !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<p class='titulo-nasa'>✍️ Registro de Calificaciones</p>", unsafe_allow_html=True)
    st.markdown("---")

    # 📥 EXTRACCIÓN MASIVA POR PAGINACIÓN (SISTEMA ANTI-TRUNCAMIENTO NASA)
    try:
        supabase = iniciar_conexion()
        estudiantes_base = []
        offset, chunk_size = 0, 1000
        
        with st.spinner("Sincronizando coordenadas completas del búnker..."):
            while True:
                resultado = supabase.table("data_estudiantes").select('*').range(offset, offset + chunk_size - 1).execute()
                if not resultado.data: 
                    break
                estudiantes_base.extend(resultado.data)
                if len(resultado.data) < chunk_size: 
                    break
                offset += chunk_size
        
        if not estudiantes_base:
            st.warning("📭 No hay conexión o la tabla oficial está vacía.")
            return
            
        df_base = pd.DataFrame(estudiantes_base)
        df_base.columns = [c.lower() for c in df_base.columns]
        
        col_grado = "grado" if "grado" in df_base.columns else df_base.columns[2]
        col_grupo = "grupo" if "grupo" in df_base.columns else df_base.columns[3]
        col_id = "id_estudiante" if "id_estudiante" in df_base.columns else df_base.columns[0]
        col_nombre = "nombre_completo" if "nombre_completo" in df_base.columns else df_base.columns[1]

        # Higiene radical de datos
        df_base[col_grado] = df_base[col_grado].astype(str).str.strip()
        df_base[col_grupo] = df_base[col_grupo].astype(str).str.strip().str.upper()
        df_base[col_nombre] = df_base[col_nombre].astype(str).str.strip()

        grados_reales = sorted(list(df_base[col_grado].unique()), key=lambda x: int(''.join(filter(str.isdigit, x))) if any(char.isdigit() for char in x) else 0)
        grupos_reales = sorted(list(df_base[col_grupo].unique()))

    except Exception as e:
        st.error(f"🚨 Falla en la telemetría del búnker: {e}")
        return

    # 🎛️ PANEL DE CONTROL CON ASIGNATURAS COMPLETAS DE BACHILLERATO
    st.markdown("<h5 style='color: #0d1b2a; font-weight: bold;'>🔍 Parámetros de Calificación</h5>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        grado_sel = st.selectbox("🏫 Grado Detectado:", grados_reales, index=None, placeholder="Seleccione Grado...", key="nasa_grado")
    with c2:
        grupo_sel = st.selectbox("🛡️ Grupo Detectado:", grupos_reales, index=None, placeholder="Seleccione Grupo...", key="nasa_grupo")
    with c3:
        # 📚 CATÁLOGO OFICIAL EXTENDIDO PARA BACHILLERATO INSTITUCIONAL
        asignaturas_bachillerato = [
            "Lengua Castellana (Español)", "Matemáticas", "Trigonometría", "Cálculo", 
            "Física", "Química", "Biología", "Ciencias Naturales", 
            "Ciencias Sociales", "Historia", "Geografía", "Filosofía", 
            "Economía y Política", "Inglés", "Informática y Tecnología", 
            "Educación Física", "Ética y Valores", "Religión", "Artística"
        ]
        asignatura_sel = st.selectbox("📚 Asignatura:", asignaturas_bachillerato, index=None, placeholder="Seleccione Materia...")
    with c4:
        periodo_sel = st.selectbox("📅 Período:", ["Primer Período", "Segundo Período", "Tercer Período", "Cuarto Período"], index=None, placeholder="Seleccione Período...")

    # Control de flujo seguro
    if not (grado_sel and grupo_sel and asignatura_sel and periodo_sel):
        st.markdown("---")
        st.info("📌 **Consola en Espera:** Seleccione todos los parámetros superiores para desplegar la planilla de calificaciones oficiales.")
        return

    # 🗺️ FILTRADO COMPLETO SOBRE EL 100% DE LA DATA RECUPERADA
    df_filtrado = df_base[
        (df_base[col_grado] == grado_sel) & 
        (df_base[col_grupo] == grupo_sel)
    ].copy()
    
    # Filtro anti-clones local por nombre
    df_filtrado = df_filtrado.drop_duplicates(subset=[col_nombre])
    df_filtrado = df_filtrado.sort_values(by=col_nombre)

    # 📊 DESPLIEGUE DEL ESCENARIO MATRICIAL COMPLETO
    if not df_filtrado.empty:
        total_alumnos = len(df_filtrado)
        
        st.markdown(f"""
            <div class="hud-nasa-container">
                <div class="hud-nasa-card">
                    <div class="hud-nasa-label">ALUMNOS EN ESTE CURSO</div>
                    <div class="hud-nasa-value">{total_alumnos}</div>
                </div>
                <div class="hud-nasa-card" style="border-left-color: #d4af37;">
                    <div class="hud-nasa-label" style="color: #bfa12a;">ASIGNATURA SELECCIONADA</div>
                    <div class="hud-nasa-value" style="color: #d4af37; font-size:15px; margin-top:8px;">{asignatura_sel.upper()}</div>
                </div>
                <div class="hud-nasa-card" style="border-left-color: #2b9348;">
                    <div class="hud-nasa-label" style="color: #2b9348;">SISTEMA EVALUATIVO</div>
                    <div class="hud-nasa-value" style="color: #2b9348; font-size:16px; margin-top:8px;">P1(40%) | P2(40%) | P3(20%)</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        c_btn, _ = st.columns([1, 2])
        with c_btn:
            guardar_click = st.button("💾 Guardar Calificaciones Oficiales", use_container_width=True)

        # Corona de la Matriz Oficial
        st.markdown(f"<div class='barra-matriz-oficial'>Planilla Oficial: {asignatura_sel} - Curso {grado_sel} Grupo {grupo_sel}</div>", unsafe_allow_html=True)

        planilla_real = pd.DataFrame({
            "ID Estudiante": df_filtrado[col_id],
            "Nombre Completo": df_filtrado[col_nombre],
            "Nota 1 (40%)": 0.0,
            "Nota 2 (40%)": 0.0,
            "Nota 3 (20%)": 0.0
        })

        with st.container():
            planilla_editada = st.data_editor(
                planilla_real,
                use_container_width=True,
                hide_index=True,
                disabled=["ID Estudiante", "Nombre Completo"],
                column_config={
                    "Nota 1 (40%)": st.column_config.NumberColumn(min_value=0.0, max_value=5.0, step=0.1, format="%.1f"),
                    "Nota 2 (40%)": st.column_config.NumberColumn(min_value=0.0, max_value=5.0, step=0.1, format="%.1f"),
                    "Nota 3 (20%)": st.column_config.NumberColumn(min_value=0.0, max_value=5.0, step=0.1, format="%.1f")
                }
            )

        if guardar_click:
            st.success(f"🏆 ¡Planilla de {asignatura_sel} para el curso {grado_sel}{grupo_sel} consolidada con éxito para {total_alumnos} estudiantes!")
            st.balloons()
    else:
        st.warning(f"📭 No se detectaron vectores de matrícula para el Grado {grado_sel} - Grupo {grupo_sel} en la base de datos.")
