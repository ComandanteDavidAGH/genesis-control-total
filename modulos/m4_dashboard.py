import streamlit as st
import pandas as pd
from supabase import create_client
from estilos_globales import inyectar_estilos_omega

# =================================================================
# 🔒 CONEXIÓN AL BÚNKER DE DATOS INSTITUCIONAL
# =================================================================
def iniciar_conexion():
    url = st.secrets["SUPABASE_URL"].strip()
    key = st.secrets["SUPABASE_KEY_REAL"].strip() if "SUPABASE_KEY_REAL" in st.secrets else st.secrets["SUPABASE_KEY"].strip()
    return create_client(url, key)

# =================================================================
# ⚡ FUNCIÓN PRINCIPAL DEL DASHBOARD
# =================================================================
def ejecutar():
    # Inyección visual unificada Génesis Omega Pro
    inyectar_estilos_omega()
    
    # Encabezado Principal
    st.markdown("<h1 style='text-align: center; color: #0F172A; font-size: 3rem;'>📊 Dashboard Estratégico</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2rem; color: #D97706; font-weight: bold; letter-spacing: 1px;'>VISIÓN GLOBAL DEL ESTADO INSTITUCIONAL</p>", unsafe_allow_html=True)
    st.markdown("---")

    # =====================================================================
    # 📥 EXTRACCIÓN MASIVA BLINDADA (LA MISMA LÓGICA TÁCTICA)
    # =====================================================================
    supabase = iniciar_conexion()
    estudiantes_base = []
    offset, chunk_size = 0, 1000
    
    with st.spinner("Sincronizando radares y calculando métricas globales..."):
        try:
            # Bucle infinito para vaciar el búnker de datos sin importar el límite
            while True:
                resultado = supabase.table("data_estudiantes").select('*').range(offset, offset + chunk_size - 1).execute()
                if not resultado.data: 
                    break
                estudiantes_base.extend(resultado.data)
                if len(resultado.data) < chunk_size: 
                    break
                offset += chunk_size
        except Exception as e:
            st.error(f"🚨 Falla de telemetría con el búnker: {e}")
            return

    if estudiantes_base:
        # --- PROCESAMIENTO E HIGIENIZACIÓN ---
        df = pd.DataFrame(estudiantes_base)
        df.columns = [c.lower().strip() for c in df.columns]
        
        # Identificación dinámica de columnas
        col_id = "id_estudiante" if "id_estudiante" in df.columns else df.columns[0]
        col_grado = "grado" if "grado" in df.columns else ("grupo" if "grupo" in df.columns else None)
        
        # --- ELIMINACIÓN DE DUPLICADOS (FILTRO ANTI-CLONES) ---
        df[col_id] = df[col_id].astype(str).str.strip()
        df_unicos = df.drop_duplicates(subset=[col_id]).copy()
        
        # Limpieza de grados para las estadísticas
        if col_grado:
            df_unicos[col_grado] = df_unicos[col_grado].astype(str).str.upper().str.strip()
            # Filtramos valores nulos o vacíos
            df_unicos = df_unicos[~df_unicos[col_grado].isin(["NAN", "NONE", "", "SIN GRADO"])]

        # --- CÁLCULO DE MÉTRICAS EXACTAS ---
        total_matricula = len(df_unicos)
        total_grados = df_unicos[col_grado].nunique() if col_grado else 0
        
        # =================================================================
        # 📈 PANEL DE INDICADORES (HUD PRINCIPAL)
        # =================================================================
        with st.container(border=True):
            c1, c2 = st.columns(2)
            
            with c1:
                st.markdown(f"<div style='text-align: center;'><h4 style='color: #64748B; margin-bottom: 0px;'>TROPAS TOTALES (ALUMNOS ACTIVOS)</h4><h2 style='color: #0F172A; font-size: 3.5rem; margin-top: 0px;'>{total_matricula}</h2></div>", unsafe_allow_html=True)
            with c2:
                st.markdown(f"<div style='text-align: center; border-left: 2px solid #E2E8F0;'><h4 style='color: #D97706; margin-bottom: 0px;'>ESCUADRONES (GRADOS ACTIVOS)</h4><h2 style='color: #D97706; font-size: 3.5rem; margin-top: 0px;'>{total_grados}</h2></div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # =================================================================
        # 📊 DESPLIEGUE TÁCTICO: DISTRIBUCIÓN POR GRADO
        # =================================================================
        if col_grado and total_grados > 0:
            st.markdown("### 📉 Distribución de Estudiantes por Grado")
            
            # Agrupamos los datos para contar alumnos por grado
            distribucion = df_unicos.groupby(col_grado).size().reset_index(name='Cantidad de Estudiantes')
            
            # Ordenamos lógicamente (asumiendo que los grados empiezan con números)
            distribucion = distribucion.sort_values(by=col_grado)
            
            # Layout con columnas para gráfica y tabla resumen
            col_grafica, col_tabla = st.columns([2, 1])
            
            with col_grafica:
                # Gráfica de barras nativa de Streamlit
                st.bar_chart(distribucion.set_index(col_grado), use_container_width=True, color="#1D4ED8")
                
            with col_tabla:
                # Tabla de resumen rápido
                st.dataframe(distribucion, use_container_width=True, hide_index=True)
                
    else:
        st.warning("📭 Los radares no detectan registros en la base de datos.")

if __name__ == "__main__":
    ejecutar()
