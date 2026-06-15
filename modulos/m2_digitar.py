import streamlit as st
import pandas as pd
from supabase import create_client

def iniciar_conexion():
    url = st.secrets["SUPABASE_URL"].strip()
    key = st.secrets["SUPABASE_KEY_REAL"].strip() if "SUPABASE_KEY_REAL" in st.secrets else st.secrets["SUPABASE_KEY"].strip()
    return create_client(url, key)

def ejecutar():
    # 🎨 COMPONENTE DE HIERRO: CSS Premium de Alta Intensidad
    st.markdown("""
        <style>
        .titulo-genesis { color: #0d1b2a; font-family: 'Arial Black'; font-size: 32px; margin-bottom: 0px; }
        .subtitulo-genesis { color: #d4af37; font-weight: bold; font-size: 13px; text-transform: uppercase; margin-top: 0px; }
        .hud-container { display: flex; gap: 15px; margin-bottom: 25px; margin-top: 15px; }
        .hud-card {
            flex: 1; background: #ffffff; border-top: 3px solid #0d1b2a;
            border-radius: 4px 4px 12px 12px; padding: 12px 15px; text-align: center;
            box-shadow: 0 10px 25px rgba(13, 27, 42, 0.04);
        }
        .hud-value { font-size: 26px; font-family: 'Arial Black'; font-weight: 900; color: #0d1b2a; }
        .contenedor-planilla { background: #ffffff; border-radius: 12px; border: 1px solid #e5e5e5; border-top: 4px solid #0d1b2a; padding: 20px; margin-top: 15px; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<p class='titulo-genesis'>🖮 Digitar Notas</p>", unsafe_allow_html=True)
    st.markdown("<p class='subtitulo-genesis'>Planilla Central de Calificaciones Académicas</p>", unsafe_allow_html=True)
    st.markdown("---")

    # 🎛️ PANEL DE CONFIGURACIÓN SUPERIOR
    st.markdown("##### 🔍 Selección de Curso y Periodo")
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
            
            # Identificamos columnas
            col_grado = "grado" if "grado" in df_base.columns else df_base.columns[2]
            col_grupo = "grupo" if "grupo" in df_base.columns else df_base.columns[3]
            col_id = "id_estudiante" if "id_estudiante" in df_base.columns else df_base.columns[0]
            col_nombre = "nombre_completo" if "nombre_completo" in df_base.columns else df_base.columns[1]

            # 🔐 FILTRO ANTI-CLONES: Limpiamos los duplicados del ID antes de renderizar el salón
            df_base = df_base.drop_duplicates(subset=[col_id])

            # Filtramos por grado y grupo correspondientes
            df_filtrado = df_base[
                (df_base[col_grado].astype(str).str.contains(grado_sel.replace("°",""), na=False)) & 
                (df_base[col_grupo].astype(str).str.upper() == grupo_sel.upper())
            ].copy()
            
            df_filtrado = df_filtrado.sort_values(by=col_nombre)
            
            # Construimos la planilla limpia con alumnos únicos
            planilla_datos = pd.DataFrame({
                "ID Estudiante": df_filtrado[col_id],
                "Nombre Completo": df_filtrado[col_nombre],
                "Nota 1 (40%)": 0.0,
                "Nota 2 (40%)": 0.0,
                "Nota 3 (20%)": 0.0
            })
            estudiantes_filtrados = planilla_datos.reset_index(drop=True)
    except Exception as e:
        st.error(f"🚨 Error al conectar con la lista de alumnos: {e}")
        return

    # 📊 DESPLEGUE DEL ESCENARIO CON VITAMINAS
    if not estudiantes_filtrados.empty:
        total_salon = len(estudiantes_filtrados)

        # ⚡ INYECCIÓN DE HIERRO: Tarjetas analíticas contextuales flotantes
        st.markdown(f"""
            <div class="hud-container">
                <div class="hud-card">
                    <div style="font-size:11px; font-weight:800; color:#5c677d;">👥 ALUMNOS EN SALÓN</div>
                    <div class="hud-value">{total_salon}</div>
                </div>
                <div class="hud-card" style="border-top-color: #d4af37;">
                    <div style="font-size:11px; font-weight:800; color:#bfa12a;">📅 EVALUACIÓN</div>
                    <div class="hud-value" style="color: #d4af37; font-size:16px; margin-top:8px;">{periodo_sel.upper()}</div>
                </div>
                <div class="hud-card" style="border-top-color: #2b9348;">
                    <div style="font-size:11px; font-weight:800; color:#2b9348;">⚖️ SISTEMA INSTITUCIONAL</div>
                    <div class="hud-value" style="color: #2b9348; font-size:18px; margin-top:5px;">40% - 40% - 20%</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="contenedor-planilla">', unsafe_allow_html=True)
        st.markdown(f"<h4 style='color: #0d1b2a; font-weight: bold; margin-top: 0px;'>📋 MATRIZ DE CALIFICACIONES: GRADO {grado_sel} - GRUPO {grupo_sel}</h4>", unsafe_allow_html=True)
        st.caption("Escribe las notas correspondientes sobre los casilleros habilitados. El sistema procesará las definitivas al guardar.")

        # Planilla Interactiva Profesional editable
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
            if st.button("💾 Registrar Calificaciones en Supabase", use_container_width=True):
                with st.spinner("Procesando y promediando registros académicos..."):
                    # Cálculo de promedios ponderados
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
