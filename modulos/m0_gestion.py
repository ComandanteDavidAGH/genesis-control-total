import streamlit as st
from estilos_globales import inyectar_estilos_omega
import pandas as pd
from supabase import create_client

# =================================================================
# 🔒 CONEXIÓN AL BÚNKER DE DATOS INSTITUCIONAL
# =================================================================
def iniciar_conexion():
    url = st.secrets["SUPABASE_URL"].strip()
    key = st.secrets["SUPABASE_KEY_REAL"].strip() if "SUPABASE_KEY_REAL" in st.secrets else st.secrets["SUPABASE_KEY"].strip()
    return create_client(url, key)

def ejecutar():
    # ⚡ Inyección visual unificada Génesis Omega Pro
    inyectar_estilos_omega()
    
    # ==========================================
    # 📊 ENCABEZADO PRINCIPAL DE ALTO IMPACTO
    # ==========================================
    st.markdown("<h1 style='text-align: center; color: #0F172A; font-size: 3rem;'>👥 Gestión de Estudiantes</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2rem; color: #D97706; font-weight: bold; letter-spacing: 1px;'>CONSOLA CENTRAL DE CONTROL DE MATRÍCULA INSTITUCIONAL</p>", unsafe_allow_html=True)
    st.markdown("---")

    # 📥 EXTRACCIÓN MASIVA POR PAGINACIÓN
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

        # =================================================================
        # 📈 PANEL DE INDICADORES (HUD OMEGA)
        # =================================================================
        st.markdown("### 📊 Panel de Indicadores Globales")
        with st.container(border=True):
            c1, c2, c3 = st.columns(3)
            
            with c1:
                st.markdown(f"<div style='text-align: center;'><h4 style='color: #64748B; margin-bottom: 0px;'>MATRÍCULA TOTAL ACTIVA</h4><h2 style='color: #0F172A; font-size: 2.5rem; margin-top: 0px;'>{total_matricula}</h2></div>", unsafe_allow_html=True)
            with c2:
                st.markdown(f"<div style='text-align: center; border-left: 2px solid #E2E8F0; border-right: 2px solid #E2E8F0;'><h4 style='color: #D97706; margin-bottom: 0px;'>GRADOS ACTIVOS</h4><h2 style='color: #D97706; font-size: 2.5rem; margin-top: 0px;'>{total_grados}</h2></div>", unsafe_allow_html=True)
            with c3:
                st.markdown(f"<div style='text-align: center;'><h4 style='color: #16A34A; margin-bottom: 0px;'>GRUPOS OPERATIVOS</h4><h2 style='color: #16A34A; font-size: 2.5rem; margin-top: 0px;'>{total_grupos}</h2></div>", unsafe_allow_html=True)

        # =================================================================
        # 📋 MATRIZ OFICIAL DE ESTUDIANTES
        # =================================================================
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 📋 Matriz Oficial de Estudiantes Registrados")
        st.info("💡 Esta tabla muestra el consolidado maestro. Úsela para auditar que todos los estudiantes de su institución estén correctamente cargados en el sistema.")

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

        # 🎯 FILTRO ESTRATÉGICO POR GRADO
        if "Grado" in df_ordenado.columns:
            lista_grados_disponibles = ["TODOS LOS GRADOS"] + sorted(df_ordenado["Grado"].dropna().unique().tolist())
            grado_seleccionado = st.selectbox("🔎 FILTRAR POR CURSO/GRADO:", lista_grados_disponibles)
            
            # Aplicar el filtro si no se seleccionó "TODOS"
            if grado_seleccionado != "TODOS LOS GRADOS":
                df_mostrar = df_ordenado[df_ordenado["Grado"] == grado_seleccionado]
            else:
                df_mostrar = df_ordenado
        else:
            df_mostrar = df_ordenado

        # Despliegue blindado del Dataframe sin índices feos
        with st.container(border=True):
            st.dataframe(df_mostrar[columnas_finales], use_container_width=True, hide_index=True)
            
    else:
        st.warning("📭 No se encontraron registros de estudiantes en el hangar de datos.")

if __name__ == "__main__":
    ejecutar()
