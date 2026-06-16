import streamlit as st
import pandas as pd
import re
from supabase import create_client
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
    
    supabase = iniciar_conexion()
    
    # =====================================================================
    # 📄 TAB 1: LISTADOS POR CURSO
    # =====================================================================
    with tab_listados:
        # Extracción de datos con indicador de carga
        with st.spinner("Sincronizando con el búnker de datos..."):
            try:
                # 🔥 CORRECCIÓN CRÍTICA: Se usan las mayúsculas exactas "Nombre_Completo, Grado"
                respuesta = supabase.table("data_estudiantes").select("Nombre_Completo, Grado").limit(15000).execute()
                listado_crudo = respuesta.data
            except Exception as e:
                st.error(f"🚨 Enlace de comunicaciones roto con el búnker de Supabase: {e}")
                listado_crudo = []

        if listado_crudo:
            st.markdown("🟢 **Sincronizado**")
            df_est = pd.DataFrame(listado_crudo)
            
            # Estandarizamos los nombres de las columnas a minúsculas en el DataFrame de Pandas
            # para que el resto del script funcione sin importar cómo responda Supabase
            df_est.columns = [str(c).lower().strip() for c in df_est.columns]
            
            # --- LIMPIEZA NUCLEAR ---
            def aplanar_grado(g):
                if pd.isna(g): return "SIN GRADO"
                match = re.search(r'(\d+)', str(g))
                return match.group(1) + "°" if match else str(g).upper().strip()
                
            df_est['grado'] = df_est['grado'].apply(aplanar_grado)
            df_est['nombre_completo'] = df_est['nombre_completo'].astype(str).str.upper().str.strip()
            
            # --- ELIMINACIÓN DE DUPLICADOS (LA MAGIA DE LOS 750 ALUMNOS) ---
            df_unicos = df_est.drop_duplicates(subset=['nombre_completo', 'grado']).reset_index(drop=True)
            
            # Ordenamos los grados disponibles de forma lógica
            grados_disponibles = sorted([g for g in df_unicos['grado'].unique() if g != "SIN GRADO"])
            
            # --- INTERFAZ DEL SELECTOR ---
            if grados_disponibles:
                grado_seleccionado = st.selectbox("Seleccione el Grado a auditar:", grados_disponibles, key="sb_grados_eval")
                
                if grado_seleccionado:
                    # Filtramos los alumnos que pertenecen únicamente al grado seleccionado
                    df_filtrado = df_unicos[df_unicos['grado'] == grado_seleccionado].sort_values(by="nombre_completo").reset_index(drop=True)
                    
                    # Ajustamos el índice para que la tabla empiece en 1 visualmente
                    df_filtrado.index += 1
                    
                    # Mostramos el consolidado final de tus 750 alumnos reales
                    st.markdown(f"📊 **Listado Oficial de {grado_seleccionado} — ({len(df_filtrado)} Alumnos):**")
                    
                    st.dataframe(
                        df_filtrado[['nombre_completo']].rename(columns={'nombre_completo': 'Nombre Completo'}),
                        use_container_width=True
                    )
            else:
                st.warning("No se encontraron grados válidos en la base de datos.")
        else:
            st.info("La base de datos está vacía o no se pudo extraer la información.")

    # =====================================================================
    # ➕ TAB 2: MATRÍCULA INDIVIDUAL
    # =====================================================================
    with tab_individual:
        st.markdown("#### ➕ Registro de Alumno Nuevo")
        with st.form("form_alta_individual_eval", clear_on_submit=True):
            nuevo_nombre = st.text_input("👤 NOMBRE COMPLETO DEL ESTUDIANTE:").strip().upper()
            
            # Reutilizamos los grados de la consulta anterior para el menú desplegable
            try:
                grados_drop = sorted([g for g in df_unicos['grado'].unique().tolist() if g != "SIN GRADO"])
            except NameError:
                grados_drop = ["1°", "2°", "3°", "4°", "5°", "6°", "7°", "8°", "9°", "10°", "11°"]
                
            grados_drop.append("[+ CREAR NUEVO GRADO...]")
            
            c_grado, c_vacia = st.columns([1, 1])
            with c_grado:
                grado_sel = st.selectbox("👥 ASIGNAR GRADO / CURSO:", grados_drop, index=0)
            
            grado_nuevo_txt = ""
            if grado_sel == "[+ CREAR NUEVO GRADO...]":
                grado_nuevo_txt = st.text_input("✍️ Escriba el nombre del nuevo Grado:").strip().upper()
                
            boton_matricular = st.form_submit_button("🚀 EFECTUAR MATRÍCULA DE ESTUDIANTE", use_container_width=True)

        if boton_matricular:
            grado_final = grado_nuevo_txt if grado_sel == "[+ CREAR NUEVO GRADO...]" else grado_sel
            if not nuevo_nombre or not grado_final:
                st.error("❌ Operación abortada: Los campos son obligatorios.")
            else:
                try:
                    # Mapeo usando las mayúsculas exactas requeridas por Supabase
                    payload_estudiante = {"Nombre_Completo": nuevo_nombre, "Grado": grado_final} 
                    supabase.table("data_estudiantes").insert(payload_estudiante).execute()
                    st.success(f"🎯 ¡MATRÍCULA EXITOSA! '{nuevo_nombre}' asignado a '{grado_final}'.")
                    st.rerun()
                except Exception as e:
                    st.error(f"🚨 Falla al insertar en el búnker: {e}")

    # =====================================================================
    # 📥 TAB 3: CARGA MASIVA TÁCTICA
    # =====================================================================
    with tab_masiva:
        st.markdown("#### 📥 Inyector de Listas Completas de Excel")
        datos_pegados = st.text_area("📋 PEGUE AQUÍ LAS COLUMNAS DE EXCEL (Nombre | Grado):", height=200, key="ta_masiva_eval")
        boton_carga_masiva = st.button("⚡ INICIAR INYECCIÓN MASIVA", use_container_width=True, type="primary", key="btn_masiva_eval")
        
        if boton_carga_masiva and datos_pegados.strip():
            try:
                linhas = datos_pegados.strip().split("\n")
                registros_bulk = []
                for l in linhas:
                    partes = l.split("\t") if "\t" in l else l.split(",")
                    if len(partes) >= 2:
                        nom = str(partes[0]).strip().upper()
                        gra = str(partes[1]).strip().upper()
                        if nom and gra:
                            # Mapeo usando las mayúsculas exactas para la inserción masiva
                            registros_bulk.append({"Nombre_Completo": nom, "Grado": gra})
                
                if registros_bulk:
                    with st.spinner("Inyectando registros en el búnker..."):
                        supabase.table("data_estudiantes").insert(registros_bulk).execute()
                        st.success(f"🎉 ¡{len(registros_bulk)} estudiantes inyectados con éxito!")
                        st.rerun()
            except Exception as e:
                st.error(f"🚨 Falla en el procesador masivo: {e}")

if __name__ == "__main__":
    ejecutar()
