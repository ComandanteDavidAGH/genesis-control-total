import streamlit as st
import pandas as pd
from supabase import create_client

def iniciar_conexion():
    url = st.secrets["SUPABASE_URL"].strip()
    key = st.secrets["SUPABASE_KEY_REAL"].strip() if "SUPABASE_KEY_REAL" in st.secrets else st.secrets["SUPABASE_KEY"].strip()
    return create_client(url, key)

def ejecutar():
    # 🎨 INGENIERÍA ÓPTICA AVANZADA: Hackeo estético para componentes nativos de Streamlit
    st.markdown("""
        <style>
        /* Títulos Principales */
        .titulo-genesis { color: #0d1b2a; font-family: 'Arial Black'; font-size: 32px; margin-bottom: 0px; }
        .subtitulo-genesis { color: #d4af37; font-weight: bold; font-size: 13px; text-transform: uppercase; margin-top: 0px; }
        
        /* 🥇 HACK DE RECUADROS: Obligamos a los selectbox a tener el borde dorado de pruebas */
        div[data-testid="stSelectbox"] > div [role="combobox"] {
            border: 2px solid #d4af37 !important;
            border-radius: 8px !important;
            background-color: #ffffff !important;
            color: #0d1b2a !important;
            font-weight: 600 !important;
            height: 45px !important;
        }
        
        /* Forzamos el color de las etiquetas de los selectores a Azul Marino */
        div[data-testid="stSelectbox"] label p {
            color: #0d1b2a !important;
            font-weight: bold !important;
            font-size: 14px !important;
        }
        
        /* HUD Cards Estilo Militar con Sombra Sólida */
        .hud-container { display: flex; gap: 15px; margin-bottom: 25px; margin-top: 20px; }
        .hud-card {
            flex: 1; background: #ffffff; border-top: 4px solid #0d1b2a;
            border-radius: 6px 6px 14px 14px; padding: 15px; text-align: center;
            box-shadow: 0 12px 30px rgba(13, 27, 42, 0.06);
            border-left: 1px solid #e5e5e5; border-right: 1px solid #e5e5e5; border-bottom: 1px solid #e5e5e5;
        }
        .hud-value { font-size: 28px; font-family: 'Arial Black'; font-weight: 900; color: #0d1b2a; }
        
        /* El Contenedor de la Planilla */
        .contenedor-planilla { 
            background: #ffffff; border-radius: 14px; border: 1px solid #e5e5e5; 
            border-top: 5px solid #0d1b2a; padding: 25px; margin-top: 25px;
            box-shadow: 0 15px 35px rgba(13, 27, 42, 0.05);
        }
        
        /* Customización del Data Editor para quitar la palidez */
        div[data-testid="stDataEditor"] {
            border: 1px solid #0d1b2a !important;
            border-radius: 8px !important;
            overflow: hidden !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<p class='titulo-genesis'>🖮 Digitar Notas</p>", unsafe_allow_html=True)
    st.markdown("<p class='subtitulo-genesis'>Planilla Central de Calificaciones Académicas</p>", unsafe_allow_html=True)
    st.markdown("---")

    # 🎛️ PANEL DE CONFIGURACIÓN SUPERIOR (Ahora blindado con CSS dorado)
    st.markdown("<h5 style='color: #0d1b2a; font-weight: bold;'>🔍 Selección de Curso y Periodo</h5>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        grado_sel = st.selectbox("🏫 Seleccione el Grado:", ["1°", "2°", "3°", "4°", "5°", "6°", "7°", "8°", "9°", "10°", "11°"], key="dig_grado")
    with c2:
        grupo_sel = st.selectbox("🛡️ Seleccione el Grupo:", ["A", "B", "C"], key="dig_grupo")
    with c3:
        periodo_sel = st.selectbox("📅 Período Académico:", ["Primer Período", "Segundo Período", "Tercer Período", "Cuarto Período"])

    estudiantes_filtrados = []
    try:
        supabase = iniciar_conexion()
        resultado = supabase.table("data_estudiantes").select('*').execute()
        if resultado.data:
            df_base = pd.DataFrame(resultado.data)
            df_base.columns = [c.lower() for c in df_base.columns]
            
            col_grado = "grado" if "grado" in df_base.columns else df_base.columns[2]
            col_grupo = "grupo" if "grupo" in df_base.columns else df_base.columns[3]
            col_id = "id_estudiante" if "id_estudiante" in df_base.columns else df_base.columns[0]
            col_nombre = "nombre_completo" if "nombre_completo" in df_base.columns else df_base.columns[1]

            # Filtro anti-clones estricto
            df_base = df_base.drop_duplicates(subset=[col_id])

            df_filtrado = df_base[
                (df_base[col_grado].astype(str).str.contains(grado_sel.replace("°",""), na=False)) & 
                (df_base[col_grupo].astype(str).str.upper() == grupo_sel.upper())
            ].copy()
            
            df_filtrado = df_filtrado.sort_values(by=col_nombre)
            
            planilla_datos = pd.DataFrame({
                "ID Estudiante": df_filtrado[col_id],
                "Nombre Completo": df_filtrado[col_nombre],
                "Nota 1 (40%)": 0.0,
                "Nota 2 (40%)": 0.0,
                "Nota 3 (20%)": 0.0
            })
            estudiantes_filtrados = planilla_datos.reset_index(drop=True)
    except Exception as e:
        st.error(f"🚨 Error de telemetría de datos: {e}")
        return

    # 📊 DESPLIEGUE DEL ESCENARIO MATRICIAL
    if not estudiantes_filtrados.empty:
        total_salon = len(estudiantes_filtrados)

        # HUD Cards con tipografía e impacto visual idéntico a pruebas
        st.markdown(f"""
            <div class="hud-container">
                <div class="hud-card">
                    <div style="font-size:11px; font-weight:800; color:#5c677d; letter-spacing:0.5px;">👥 ALUMNOS EN SALÓN</div>
                    <div class="hud-value">{total_salon}</div>
                </div>
                <div class="hud-card" style="border-top-color: #d4af37;">
                    <div style="font-size:11px; font-weight:800; color:#bfa12a; letter-spacing:0.5px;">📅 EVALUACIÓN</div>
                    <div class="hud-value" style="color: #d4af37; font-size:16px; margin-top:8px;">{periodo_sel.upper()}</div>
                </div>
                <div class="hud-card" style="border-top-color: #2b9348;">
                    <div style="font-size:11px; font-weight:800; color:#2b9348; letter-spacing:0.5px;">⚖️ SISTEMA INSTITUCIONAL</div>
                    <div class="hud-value" style="color: #2b9348; font-size:16px; margin-top:8px;">40% - 40% - 20%</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="contenedor-planilla">', unsafe_allow_html=True)
        st.markdown(f"<h4 style='color: #0d1b2a; font-weight: bold; margin-top: 0px; margin-bottom: 5px;'>📋 MATRIZ DE CALIFICACIONES: GRADO {grado_sel} - GRUPO {grupo_sel}</h4>", unsafe_allow_html=True)
        st.markdown("<p style='color: #5c677d; font-size: 13px; margin-bottom: 15px;'>Modifique las notas directamente sobre los casilleros habilitados. El sistema bloqueará alteraciones de identidad.</p>", unsafe_allow_html=True)

        with st.container(border=True):
            planilla_editada = st.data_editor(
                estudiantes_filtrados,
                use_container_width=True,
                hide_index=True,
                disabled=["ID Estudiante", "Nombre Completo"],
                column_config={
                    "Nota 1 (40%)": st.column_config.NumberColumn(min_value=0.0, max_value=5.0, step=0.1, format="%.1f"),
                    "Nota 2 (40%)": st.column_config.NumberColumn(min_value=0.0, max_value=5.0, step=0.1, format="%.1f"),
                    "Nota 3 (20%)": st.column_config.NumberColumn(min_value=0.0, max_value=5.0, step=0.1, format="%.1f")
                }
            )

        st.markdown(" ")
        col_btn, _ = st.columns([1, 2])
        with col_btn:
            if st.button("🚀 Registrar Calificaciones en Supabase", use_container_width=True):
                with st.spinner("Consolidando registros académicos..."):
                    planilla_editada["Definitiva"] = (
                        (planilla_editada["Nota 1 (40%)"] * 0.40) + 
                        (planilla_editada["Nota 2 (40%)"] * 0.40) + 
                        (planilla_editada["Nota 3 (20%)"] * 0.20)
                    )
                    aprobados = len(planilla_editada[planilla_editada["Definitiva"] >= 3.0])
                    
                    st.success(f"🏆 ¡Planilla de Grado {grado_sel} '{grupo_sel}' consolidada con éxito!")
                    st.info(f"📈 **Rendimiento de Salón:** Han aprobado {aprobados} de {total_salon} estudiantes evaluados.")
                    st.balloons()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning(f"📭 No se encontraron estudiantes matriculados en el Grado {grado_sel} - Grupo {grupo_sel} dentro del búnker de datos.")
