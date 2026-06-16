import streamlit as st
from estilos_globales import inyectar_estilos_omega  # <--- ESTA ES LA LÍNEA NUEVA
import pandas as pd
from supabase import create_client

def iniciar_conexion():
    url = st.secrets["SUPABASE_URL"].strip()
    key = st.secrets["SUPABASE_KEY_REAL"].strip() if "SUPABASE_KEY_REAL" in st.secrets else st.secrets["SUPABASE_KEY"].strip()
    return create_client(url, key)

def ejecutar():
    # ⚡ Inyección visual unificada Génesis Omega Pro
    inyectar_estilos_omega()
    st.markdown("<p class='titulo-nasa'>👥 Gestión de Estudiantes</p>", unsafe_allow_html=True)
    st.markdown("<p class='subtitulo-nasa'>Consola Central de Control de Matrícula Institucional</p>", unsafe_allow_html=True)
    st.markdown("---")

    # 📥 EXTRACCIÓN MASIVA POR PAGINACIÓN (Fiel a tus 750 alumnos reales)
    try:
        supabase = iniciar_conexion()
        estudiantes_base = []
        offset, chunk_size = 0, 1000
        
        with st.spinner("Sincronizando registro maestro de estudiantes..."):
            while True:
                resultado = supabase.table("data_estudiantes").select('*').range(offset, offset + chunk_size - 1).execute()
                if not resultado.data: 
                    break
                estudiantes_base.extend(resultado.data)
                if len(resultado.data) < chunk_size: 
                    break
                offset += chunk_size
    except Exception as e:
        st.error(f"🚨 Error de enlace masivo en el búnker: {e}")
        return

    if estudiantes_base:
        df = pd.DataFrame(estudiantes_base)
        df.columns = [c.lower() for c in df.columns]
        
        col_id = "id_estudiante" if "id_estudiante" in df.columns else df.columns[0]
        col_nombre = "nombre_completo" if "nombre_completo" in df.columns else df.columns[1]
        col_grupo = "grupo" if "grupo" in df.columns else df.columns[3]
        col_grado = "grado" if "grado" in df.columns else df.columns[2]
        
        # Higienización de cadenas
        df[col_id] = df[col_id].astype(str).str.strip()
        df[col_nombre] = df[col_nombre].astype(str).str.strip()
        
        # Filtro anti-clones para la estadística global
        df_unicos = df.drop_duplicates(subset=[col_id])
        total_matricula = len(df_unicos)
        
        total_grados = df_unicos[col_grado].nunique() if col_grado in df_unicos.columns else 0
        total_grupos = df_unicos[col_grupo].nunique() if col_grupo in df_unicos.columns else 0

        # ⚡ INDICADORES HUD DE ALTA DENSIDAD VISUAL (Mismo formato de notas)
        st.markdown(f"""
            <div class="hud-nasa-container">
                <div class="hud-nasa-card">
                    <div class="hud-nasa-label">MATRÍCULA TOTAL ACTIVA</div>
                    <div class="hud-nasa-value">{total_matricula}</div>
                </div>
                <div class="hud-nasa-card" style="border-left-color: #d4af37;">
                    <div class="hud-nasa-label" style="color: #bfa12a;">GRADOS ACTIVOS</div>
                    <div class="hud-nasa-value" style="color: #d4af37;">{total_grados}</div>
                </div>
                <div class="hud-nasa-card" style="border-left-color: #2b9348;">
                    <div class="hud-nasa-label" style="color: #2b9348;">GRUPOS OPERATIVOS</div>
                    <div class="hud-nasa-value" style="color: #2b9348;">{total_grupos}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # 👑 CINTURÓN MILITAR OSCURO DE LA MATRIZ GENERAL
        st.markdown("<div class='barra-matriz-oficial'>Matriz Maestro de Estudiantes Registrados</div>", unsafe_allow_html=True)

        # Mapeo y ordenamiento estricto de columnas para los reportes oficiales
        mapeo_visual = {}
        for c in df.columns:
            if "id" in c: mapeo_visual[c] = "ID Estudiante"
            elif "nombre" in c: mapeo_visual[c] = "Nombre Completo"
            elif "grado" in c: mapeo_visual[c] = "Grado"
            elif "grupo" in c: mapeo_visual[c] = "Grupo"
            elif "correo" in c or "mail" in c: mapeo_visual[c] = "Correo Institucional"
            else: mapeo_visual[c] = c.replace("_", " ").title()

        df_visual = df_unicos.rename(columns=mapeo_visual)
        
        col_orden = "Nombre Completo" if "Nombre Completo" in df_visual.columns else df_visual.columns[1]
        df_ordenado = df_visual.sort_values(by=col_orden)

        # Estructuramos la visualización alineando las columnas más importantes primero
        columnas_ordenadas = ["ID Estudiante", "Nombre Completo", "Grado", "Grupo", "Correo Institucional"]
        columnas_finales = [col for col in columnas_ordenadas if col in df_ordenado.columns] + [col for col in df_ordenado.columns if col not in columnas_ordenadas]

        # Despliegue blindado del Dataframe sin índices feos
        st.markdown('<div class="contenedor-planilla">', unsafe_allow_html=True)
        st.dataframe(df_ordenado[columnas_finales], use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("📭 No se encontraron registros de estudiantes en el hangar de datos.")
