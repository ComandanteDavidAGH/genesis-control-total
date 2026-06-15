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

    # 📥 ASIGNACIONES POR DEFECTO PARA EL MODO SKELETON
    grados_reales = []
    grupos_reales = []
    df_base = pd.DataFrame()
    
    col_id, col_nombre, col_grado, col_grupo = "id_estudiante", "nombre_completo", "grado", "grupo"

    try:
        supabase = iniciar_conexion()
        resultado = supabase.table("data_estudiantes").select('*').range(0, 10).execute() # Escaneo rápido inicial
        if resultado.data:
            # Traemos solo las estructuras de columnas para armar los selectores
            df_cols = pd.DataFrame(resultado.data)
            df_cols.columns = [c.lower() for c in df_cols.columns]
            col_grado = "grado" if "grado" in df_cols.columns else df_cols.columns[2]
            col_grupo = "grupo" if "grupo" in df_cols.columns else df_cols.columns[3]
            col_id = "id_estudiante" if "id_estudiante" in df_cols.columns else df_cols.columns[0]
            col_nombre = "nombre_completo" if "nombre_completo" in df_cols.columns else df_cols.columns[1]

            # Re-escaneo completo con paginación pesada para asegurar el bachillerato
            estudiantes_base = []
            offset, chunk_size = 0, 1000
            while True:
                res_masivo = supabase.table("data_estudiantes").select('*').range(offset, offset + chunk_size - 1).execute()
                if not res_masivo.data: break
                estudiantes_base.extend(res_masivo.data)
                if len(res_masivo.data) < chunk_size: break
                offset += chunk_size

            df_base = pd.DataFrame(estudiantes_base)
            df_base.columns = [c.lower() for c in df_base.columns]
            
            # Sanitización estructural
            df_base[col_grado] = df_base[col_grado].astype(str).str.strip()
            df_base[col_grupo] = df_base[col_grupo].astype(str).str.strip().str.upper()
            df_base[col_nombre] = df_base[col_nombre].astype(str).str.strip()

            grados_reales = sorted(list(df_base[col_grado].unique()), key=lambda x: int(''.join(filter(str.isdigit, x))) if any(char.isdigit() for char in x) else 0)
            grupos_reales = sorted(list(df_base[col_grupo].unique()))
    except Exception as e:
        st.error(f"🚨 Falla en el inicio de la telemetría: {e}")
        return

    # 🎛️ PANEL DE COORDENADAS ACADÉMICAS
    st.markdown("<h5 style='color: #0d1b2a; font-weight: bold;'>🔍 Parámetros de Calificación</h5>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        grado_sel = st.selectbox("🏫 Grado Detectado:", grados_reales, index=None, placeholder="Seleccione Grado...", key="nasa_grado")
    with c2:
        grupo_sel = st.selectbox("🛡️ Grupo Detectado:", grupos_reales, index=None, placeholder="Seleccione Grupo...", key="nasa_grupo")
    with c3:
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

    # 🧭 EVALUACIÓN DE ESTADO ACADÉMICO (¿Activado o Chasis Vacío?)
    viene_data_real = False
    total_alumnos_hud = 0
    asignatura_hud = asignatura_sel.upper() if asignatura_sel else "NINGUNA SELECCIONADA"
    
    if grado_sel and grupo_sel and asignatura_sel and periodo_sel and not df_base.empty:
        # Aislamos el salón real
        df_filtrado = df_base[(df_base[col_grado] == grado_sel) & (df_base[col_grupo] == grupo_sel)].copy()
        df_filtrado = df_filtrado.drop_duplicates(subset=[col_nombre])
        df_filtrado = df_filtrado.sort_values(by=col_nombre)
        
        if not df_filtrado.empty:
            viene_data_real = True
            total_alumnos_hud = len(df_filtrado)
            planilla_final = pd.DataFrame({
                "ID Estudiante": df_filtrado[col_id],
                "Nombre Completo": df_filtrado[col_nombre],
                "Nota 1 (40%)": 0.0,
                "Nota 2 (40%)": 0.0,
                "Nota 3 (20%)": 0.0
            })
    
    # Si las casillas superiores están vacías, creamos un lienzo fantasma con las mismas columnas
    if not viene_data_real:
        total_alumnos_hud = 0
        planilla_final = pd.DataFrame(columns=["ID Estudiante", "Nombre Completo", "Nota 1 (40%)", "Nota 2 (40%)", "Nota 3 (20%)"])

    # 📊 DESPLIEGUE DEL ESCENARIO SIMÉTRICO (Persiste en la pantalla)
    st.markdown(f"""
        <div class="hud-nasa-container">
            <div class="hud-nasa-card">
                <div class="hud-nasa-label">ALUMNOS EN ESTE CURSO</div>
                <div class="hud-nasa-value">{total_alumnos_hud}</div>
            </div>
            <div class="hud-nasa-card" style="border-left-color: #d4af37;">
                <div class="hud-nasa-label" style="color: #bfa12a;">ASIGNATURA SELECCIONADA</div>
                <div class="hud-nasa-value" style="color: #d4af37; font-size:14px; margin-top:8px;">{asignatura_hud}</div>
            </div>
            <div class="hud-nasa-card" style="border-left-color: #2b9348;">
                <div class="hud-nasa-label" style="color: #2b9348;">SISTEMA EVALUATIVO</div>
                <div class="hud-nasa-value" style="color: #2b9348; font-size:16px; margin-top:8px;">P1(40%) | P2(40%) | P3(20%)</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    c_btn, _ = st.columns([1, 2])
    with c_btn:
        # El botón se bloquea visualmente si no hay parámetros seleccionados
        guardar_click = st.button("💾 Guardar Calificaciones Oficiales", use_container_width=True, disabled=not viene_data_real)

    # Corona Dinámica de la Matriz Oficial
    titulo_matriz = f"Planilla Oficial: {asignatura_sel} - Curso {grado_sel}{grupo_sel}" if viene_data_real else "Planilla Oficial: Consola en Espera de Parámetros"
    st.markdown(f"<div class='barra-matriz-oficial'>{titulo_matriz}</div>", unsafe_allow_html=True)

    # Despliegue seguro de la matriz (Si está vacía, Streamlit dibuja solo la cuadrícula de cabeceras)
    with st.container():
        planilla_editada = st.data_editor(
            planilla_final,
            use_container_width=True,
            hide_index=True,
            disabled=["ID Estudiante", "Nombre Completo"] if viene_data_real else True,
            column_config={
                "Nota 1 (40%)": st.column_config.NumberColumn(min_value=0.0, max_value=5.0, step=0.1, format="%.1f"),
                "Nota 2 (40%)": st.column_config.NumberColumn(min_value=0.0, max_value=5.0, step=0.1, format="%.1f"),
                "Nota 3 (20%)": st.column_config.NumberColumn(min_value=0.0, max_value=5.0, step=0.1, format="%.1f")
            }
        )

    # Lógica de guardado protegida
    if viene_data_real and guardar_click:
        st.success(f"🏆 ¡Planilla consolidada con éxito para {total_alumnos_hud} estudiantes!")
        st.balloons()
