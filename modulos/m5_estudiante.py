import streamlit as st
import pandas as pd
import re
from supabase import create_client
# Asumo que tienes tu inyector de estilos basado en tu primera captura
from estilos_globales import inyectar_estilos_omega 

# =====================================================================
# 🔐 CONEXIÓN AL BÚNKER DE DATOS INSTITUCIONAL
# =====================================================================
def iniciar_conexion():
    url = st.secrets["SUPABASE_URL"].strip()
    key = st.secrets["SUPABASE_KEY"].strip()
    return create_client(url, key)

# =====================================================================
# ⚡ FUNCIÓN PRINCIPAL DEL MÓDULO
# =====================================================================
def ejecutar():
    # 1. Inyección visual unificada
    inyectar_estilos_omega()
    
    st.markdown("### 🔍 Inspector de Listados Oficiales")
    
    # 2. Creación de las pestañas tácticas
    tab_listados, tab_individual, tab_masiva = st.tabs([
        "📄 Listados por Curso", 
        "➕ Matrícula Individual", 
        "📥 Carga Masiva Táctica"
    ])
    
    # 3. Operaciones dentro de la pestaña de Listados
    with tab_listados:
        supabase = iniciar_conexion()
        
        # Extracción de datos con indicador de carga
        with st.spinner("Sincronizando con el búnker de datos..."):
            try:
                # Límite alto para traer todas las materias y no dejar grados por fuera
                respuesta = supabase.table("datos_estudiantes").select("nombre_completo, grado").limit(15000).execute()
                listado_crudo = respuesta.data
            except Exception as e:
                st.error(f"🚨 Enlace de comunicaciones roto con el búnker de Supabase: {e}")
                listado_crudo = []

        if listado_crudo:
            st.markdown("🟢 **Sincronizado**")
            df_est = pd.DataFrame(listado_crudo)
            
            # --- LIMPIEZA NUCLEAR ---
            # Función para estandarizar los grados (ej. "2°C" -> "2°", "10° A" -> "10°")
            def aplanar_grado(g):
                if pd.isna(g): return "SIN GRADO"
                match = re.search(r'(\d+)', str(g))
                return match.group(1) + "°" if match else str(g).upper().strip()
                
            df_est['grado'] = df_est['grado'].apply(aplanar_grado)
            df_est['nombre_completo'] = df_est['nombre_completo'].astype(str).str.upper().str.strip()
            
            # --- ELIMINACIÓN DE DUPLICADOS (LA MAGIA) ---
            # Aquí reducimos los 7,772 registros a tus 750 alumnos reales
            df_unicos = df_est.drop_duplicates(subset=['nombre_completo', 'grado']).reset_index(drop=True)
            
            # Ordenamos los grados disponibles de forma lógica
            grados_disponibles = sorted([g for g in df_unicos['grado'].unique() if g != "SIN GRADO"])
            
            # --- INTERFAZ DEL SELECTOR ---
            if grados_disponibles:
                grado_seleccionado = st.selectbox("Seleccione el Grado a auditar:", grados_disponibles)
                
                if grado_seleccionado:
                    # Filtramos los alumnos que pertenecen únicamente al grado seleccionado
                    df_filtrado = df_unicos[df_unicos['grado'] == grado_seleccionado].sort_values(by="nombre_completo").reset_index(drop=True)
                    
                    # Ajustamos el índice para que la tabla empiece en 1 visualmente
                    df_filtrado.index += 1
                    
                    # Mostramos el consolidado final
                    st.markdown(f"📊 **Listado Oficial de {grado_seleccionado} — ({len(df_filtrado)} Alumnos):**")
                    
                    # Renderizamos la tabla mostrando solo el nombre completo
                    st.dataframe(
                        df_filtrado[['nombre_completo']].rename(columns={'nombre_completo': 'Nombre Completo'}),
                        use_container_width=True
                    )
            else:
                st.warning("No se encontraron grados válidos en la base de datos.")
        else:
            st.info("La base de datos está vacía o no se pudo extraer la información.")

    # Espacios reservados para las otras pestañas
    with tab_individual:
        st.write("Interfaz para matrícula individual en construcción...")
        
    with tab_masiva:
        st.write("Interfaz para carga masiva táctica en construcción...")

# =====================================================================
# Bloque de ejecución si se corre el archivo directamente (opcional)
# =====================================================================
if __name__ == "__main__":
    ejecutar()
