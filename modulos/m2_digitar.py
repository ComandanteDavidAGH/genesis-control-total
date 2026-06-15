import streamlit as st
import pandas as pd
from supabase import create_client

def iniciar_conexion():
    url = st.secrets["SUPABASE_URL"].strip()
    key = st.secrets["SUPABASE_KEY_REAL"].strip() if "SUPABASE_KEY_REAL" in st.secrets else st.secrets["SUPABASE_KEY"].strip()
    return create_client(url, key)

def ejecutar():
    # 🎨 ESTILOS DE INTERFAZ INSTITUCIONAL
    st.markdown("""
        <style>
        .titulo-genesis { color: #0d1b2a; font-family: 'Arial Black'; font-size: 32px; margin-bottom: 0px; }
        .subtitulo-genesis { color: #d4af37; font-weight: bold; font-size: 13px; text-transform: uppercase; margin-top: 0px; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<p class='titulo-genesis'>🖮 Digitar Notas</p>", unsafe_allow_html=True)
    st.markdown("<p class='subtitulo-genesis'>Planilla Central de Calificaciones Académicas</p>", unsafe_allow_html=True)
    st.markdown("---")

    # 🎛️ FILTROS DE SELECCIÓN DE SALÓN
    st.markdown("##### 🔍 Selección de Curso y Periodo")
    c1, c2, c3 = st.columns(3)
    with c1:
        grado_sel = st.selectbox("🏫 Seleccione el Grado:", ["1°", "2°", "3°", "4°", "5°", "6°", "7°", "8°", "9°", "10°", "11°"], key="dig_grado")
    with c2:
        grupo_sel = st.selectbox("🛡️ Seleccione el Grupo:", ["A", "B", "C"], key="dig_grupo")
    with c3:
        periodo_sel = st.selectbox("📅 Período Académico:", ["Primer Período", "Segundo Período", "Tercer Período", "Cuarto Período"])

    # 📥 EXTRACCIÓN FILTRADA DESDE EL BÚNKER DE SUPABASE
    estudiantes_filtrados = []
    try:
        supabase = iniciar_conexion()
        resultado = supabase.table("data_estudiantes").select('*').execute()
        if resultado.data:
            df_base = pd.DataFrame(resultado.data)
            df_base.columns = [c.lower() for c in df_base.columns]
            
            # Buscador adaptativo de columnas
            col_grado = "grado" if "grado" in df_base.columns else df_base.columns[2]
            col_grupo = "grupo" if "grupo" in df_base.columns else df_base.columns[3]
            col_id = "id_estudiante" if "id_estudiante" in df_base.columns else df_base.columns[0]
            col_nombre = "nombre_completo" if "nombre_completo" in df_base.columns else df_base.columns[1]

            # Filtrado por salón seleccionado
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
        st.error(f"🚨 Error al conectar con la lista de alumnos: {e}")
        return

    # 📊 PLANILLA INTERACTIVA ESTILO EXCEL
    if not estudiantes_filtrados.empty:
        st.markdown("---")
        st.markdown(f"### 📋 Planilla Oficial: Grado {grado_sel} - Grupo {grupo_sel}")
        st.caption("Digita las notas directamente sobre las casillas de la tabla.")

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
            if st.button("💾 Guardar Calificaciones Oficiales", use_container_width=True):
                with st.spinner("Procesando registros académicos..."):
                    planilla_editada["Definitiva"] = (
                        (planilla_editada["Nota 1 (40%)"] * 0.40) + 
                        (planilla_editada["Nota 2 (40%)"] * 0.40) + 
                        (planilla_editada["Nota 3 (20%)"] * 0.20)
                    )
                    aprobados = len(planilla_editada[planilla_editada["Definitiva"] >= 3.0])
                    total_salon = len(planilla_editada)
                    
                    st.success(f"🏆 ¡Planilla de {grado_sel} '{grupo_sel}' procesada con éxito!")
                    st.info(f"📈 **Telemetría:** {aprobados} de {total_salon} estudiantes aprobaron.")
                    st.balloons()
    else:
        st.warning(f"📭 No se encontraron estudiantes matriculados en el Grado {grado_sel} - Grupo {grupo_sel}.")
