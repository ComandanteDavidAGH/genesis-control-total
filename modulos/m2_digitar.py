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
        .contenedor-planilla { background: #ffffff; border-radius: 12px; border: 1px solid #e5e5e5; border-top: 4px solid #0d1b2a; padding: 20px; margin-top: 15px; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<p class='titulo-genesis'>🖮 Digitar Notas</p>", unsafe_allow_html=True)
    st.markdown("<p class='subtitulo-genesis'>Planilla Central de Calificaciones Académicas</p>", unsafe_allow_html=True)
    st.markdown("---")

    # 🎛️ FILTROS DE SELECCIÓN DE SALÓN (Filtro inteligente)
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
        # Traemos toda la lista para filtrar con Pandas de forma ultra veloz y adaptarnos a mayúsculas/minúsculas
        resultado = supabase.table("data_estudiantes").select('*').execute()
        if resultado.data:
            df_base = pd.DataFrame(resultado.data)
            df_base.columns = [c.lower() for c in df_base.columns]
            
            # Buscamos columnas de grado y grupo de forma adaptativa
            col_grado = "grado" if "grado" in df_base.columns else df_base.columns[2]
            col_grupo = "grupo" if "grupo" in df_base.columns else df_base.columns[3]
            col_id = "id_estudiante" if "id_estudiante" in df_base.columns else df_base.columns[0]
            col_nombre = "nombre_completo" if "nombre_completo" in df_base.columns else df_base.columns[1]

            # Filtramos solo los alumnos que pertenecen al grado y grupo seleccionado por el docente
            df_filtrado = df_base[
                (df_base[col_grado].astype(str).str.contains(grado_sel.replace("°",""), na=False)) & 
                (df_base[col_grupo].astype(str).str.upper() == grupo_sel.upper())
            ].copy()
            
            # Ordenamos alfabéticamente por nombre
            df_filtrado = df_filtrado.sort_values(by=col_nombre)
            
            # Estructuramos la planilla limpia para el docente
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

    # 📊 RENDERIZADO DE LA PLANILLA INTERACTIVA ESTILO EXCEL
    if not estudiantes_filtrados.empty:
        st.markdown("---")
        st.markdown(f"### 📋 Planilla Oficial: Grado {grado_sel} - Grupo {grupo_sel}")
        st.caption("Digita las notas directamente sobre las casillas de la tabla. El sistema permite valores decimales.")

        with st.container(border=True):
            # 🔐 CONFIGURACIÓN DE LA PLANILLA INTELIGENTE:
            # Deshabilitamos la edición en el ID y el Nombre para que el docente no altere la identidad del alumno,
            # solo permitimos ingresar calificaciones en los tres casilleros de notas.
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

        # 💾 PROCESAMIENTO Y CALCULO TÁCTICO DE NOTAS
        st.markdown(" ")
        col_btn, _ = st.columns([1, 2])
        with col_btn:
            if st.button("💾 Guardar Calificaciones Oficiales", use_container_width=True):
                with st.spinner("Procesando y promediando registros académicos..."):
                    # Calculamos el promedio ponderado institucional en milisegundos
                    planilla_editada["Definitiva"] = (
                        (planilla_editada["Nota 1 (40%)"] * 0.40) + 
                        (planilla_editada["Nota 2 (40%)"] * 0.40) + 
                        (planilla_editada["Nota 3 (20%)"] * 0.20)
                    )
                    
                    # Filtramos los que aprobaron (nota mayor o igual a 3.0)
                    aprobados = len(planilla_editada[planilla_editada["Definitiva"] >= 3.0])
                    total_salón = len(planilla_editada)
                    
                    st.success(f"🏆 ¡Planilla de {grado_sel} '{grupo_sel}' procesada con éxito para el {periodo_sel}!")
                    st.info(f"📈 **Telemetría de Rendimiento:** {aprobados} de {total_salón} estudiantes aprobaron la asignatura asignada.")
                    st.balloons()
    else:
        st.warning(f"📭 No se encontraron estudiantes matriculados en el Grado {grado_sel} - Grupo {grupo_sel} dentro del búnker de datos.")
