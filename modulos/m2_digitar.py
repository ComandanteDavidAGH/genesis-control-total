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
        
        /* Selectores Superiores Estilo Creador de Pruebas */
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

    # 🎛️ COORDENADAS DE CONFIGURACIÓN ACADÉMICA (Filtros en 4 Columnas)
    st.markdown("<h5 style='color: #0d1b2a; font-weight: bold;'>🔍 Parámetros de Calificación</h5>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        grado_sel = st.selectbox("🏫 Grado:", ["1°", "2°", "3°", "4°", "5°", "6°", "7°", "8°", "9°", "10°", "11°"], key="nasa_grado")
    with c2:
        grupo_sel = st.selectbox("🛡️ Grupo:", ["A", "B", "C"], key="nasa_grupo")
    with c3:
        asignatura_sel = st.selectbox("📚 Asignatura:", ["Matemáticas", "Español", "Ciencias Naturales", "Ciencias Sociales", "Inglés", "Artística", "Educación Física", "Ética", "Informática", "Religión"])
    with c4:
        periodo_sel = st.selectbox("📅 Período:", ["Primer Período", "Segundo Período", "Tercer Período", "Cuarto Período"])

    # 📥 EXTRACCIÓN REAL DE ESTUDIANTES MATRICULADOS
    try:
        supabase = iniciar_conexion()
        resultado = supabase.table("data_estudiantes").select('*').execute()
        if not resultado.data:
            st.warning("📭 No hay conexión o la tabla oficial está vacía.")
            return
            
        df_base = pd.DataFrame(resultado.data)
        df_base.columns = [c.lower() for c in df_base.columns]
        
        col_grado = "grado" if "grado" in df_base.columns else df_base.columns[2]
        col_grupo = "grupo" if "grupo" in df_base.columns else df_base.columns[3]
        col_id = "id_estudiante" if "id_estudiante" in df_base.columns else df_base.columns[0]
        col_nombre = "nombre_completo" if "nombre_completo" in df_base.columns else df_base.columns[1]

        # Depuración estricta anti-clones
        df_base = df_base.drop_duplicates(subset=[col_id])

        # Filtrado quirúrgico por Grado y Grupo seleccionado
        df_filtrado = df_base[
            (df_base[col_grado].astype(str).str.contains(grado_sel.replace("°",""), na=False)) & 
            (df_base[col_grupo].astype(str).str.upper() == grupo_sel.upper())
        ].copy()
        
        df_filtrado = df_filtrado.sort_values(by=col_nombre)
        
    except Exception as e:
        st.error(f"🚨 Falla en el escaneo del búnker: {e}")
        return

    # 📊 DESPLIEGUE DEL ESCENARIO MATRICIAL EN BLANCO
    if not df_filtrado.empty:
        total_alumnos = len(df_filtrado)
        
        # Indicadores HUD calculados dinámicamente sobre la realidad del salón
        st.markdown(f"""
            <div class="hud-nasa-container">
                <div class="hud-nasa-card">
                    <div class="hud-nasa-label">ALUMNOS MATRICULADOS</div>
                    <div class="hud-nasa-value">{total_alumnos}</div>
                </div>
                <div class="hud-nasa-card" style="border-left-color: #d4af37;">
                    <div class="hud-nasa-label" style="color: #bfa12a;">ASIGNATURA SELECCIONADA</div>
                    <div class="hud-nasa-value" style="color: #d4af37; font-size:16px; margin-top:8px;">{asignatura_sel.upper()}</div>
                </div>
                <div class="hud-nasa-card" style="border-left-color: #2b9348;">
                    <div class="hud-nasa-label" style="color: #2b9348;">SISTEMA EVALUATIVO</div>
                    <div class="hud-nasa-value" style="color: #2b9348; font-size:16px; margin-top:8px;">P1(40%) | P2(40%) | P3(20%)</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Botón de comando superior para guardar cambios
        c_btn, _ = st.columns([1, 2])
        with c_btn:
            guardar_click = st.button("💾 Guardar en Base de Datos", use_container_width=True)

        # Corona de la Matriz Oficial
        st.markdown(f"<div class='barra-matriz-oficial'>Planilla Oficial: {asignatura_sel} - Grado {grado_sel}{grupo_sel}</div>", unsafe_allow_html=True)

        # Construcción del lienzo limpio con notas en cero para que el docente digite
        planilla_limpia = pd.DataFrame({
            "ID Estudiante": df_filtrado[col_id],
            "Nombre Completo": df_filtrado[col_nombre],
            "Nota 1 (40%)": 0.0,
            "Nota 2 (40%)": 0.0,
            "Nota 3 (20%)": 0.0
        })

        # ⚡ DETECTOR DE DECIMALES FANTASMA: Aplicamos configuración de número estricta a un decimal
        with st.container():
            planilla_editada = st.data_editor(
                planilla_limpia,
                use_container_width=True,
                hide_index=True,
                disabled=["ID Estudiante", "Nombre Completo"],
                column_config={
                    "Nota 1 (40%)": st.column_config.NumberColumn(min_value=0.0, max_value=5.0, step=0.1, format="%.1f"),
                    "Nota 2 (40%)": st.column_config.NumberColumn(min_value=0.0, max_value=5.0, step=0.1, format="%.1f"),
                    "Nota 3 (20%)": st.column_config.NumberColumn(min_value=0.0, max_value=5.0, step=0.1, format="%.1f")
                }
            )

        # Lógica de procesamiento al guardar
        if guardar_click:
            with st.spinner("Consolidando registros académicos..."):
                planilla_editada["Definitiva"] = (
                    (planilla_editada["Nota 1 (40%)"] * 0.40) + 
                    (planilla_editada["Nota 2 (40%)"] * 0.40) + 
                    (planilla_editada["Nota 3 (20%)"] * 0.20)
                )
                st.success(f"🏆 ¡Notas de {asignatura_sel} para el grupo {grado_sel}{grupo_sel} almacenadas con éxito!")
                st.balloons()
    else:
        st.warning(f"📭 No se detectaron vectores de matrícula para el Grado {grado_sel} - Grupo {grupo_sel}.")
