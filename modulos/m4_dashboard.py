import streamlit as st
import pandas as pd
import plotly.express as px
import io
from supabase import create_client
from estilos_globales import inyectar_estilos_omega

# =================================================================
# 🔒 CONEXIÓN AL BÚNKER DE DATOS INSTITUCIONAL
# =================================================================
def iniciar_conexion():
    url = st.secrets["SUPABASE_URL"].strip()
    key = st.secrets["SUPABASE_KEY"].strip()
    return create_client(url, key)

def buscar_campo(diccionario, nombre_campo, predeterminado=""):
    if diccionario is None: return predeterminado
    try:
        for llave, valor in diccionario.items():
            if str(llave).lower() == nombre_campo.lower():
                if valor is not None and str(valor).strip().lower() not in ['none', 'null', '']:
                    return valor
    except: pass
    return predeterminado

# =================================================================
# 🚀 EJECUCIÓN CENTRAL DEL MÓDULO DASHBOARD
# =================================================================
def ejecutar():
    inyectar_estilos_omega()

    st.markdown("<h1 class='titulo-dash'>📊 Dashboard Analítico e Informes</h1>", unsafe_allow_html=True)
    st.markdown("<h3 class='subtitulo-dash'>Consola Central de Rendimiento y Exportación de Matrices de Calificación</h3>", unsafe_allow_html=True)
    st.markdown("---")

    try:
        supabase = iniciar_conexion()
        # 1. CARGAMOS TODO EL CATÁLOGO MAESTRO (Independiente de si tienen notas)
        res_pruebas = supabase.table("pruebas_maestras").select("*").execute()
        pruebas = res_pruebas.data
        
        # 2. CARGAMOS TODAS LAS NOTAS
        res_notas = supabase.table("respuestas_estudiantes").select("*").execute()
        notas_raw = res_notas.data
    except Exception as e:
        st.error(f"🚨 Error de conexión: {e}")
        return

    if not pruebas:
        st.info("📭 No hay evaluaciones maestras registradas.")
        return

    # =================================================================
    # 🎛️ SELECTOR GENERAL (Cargando TODAS las materias del catálogo)
    # =================================================================
    diccionario_pruebas = {}
    for idx, p in enumerate(pruebas):
        nombre_raw = str(buscar_campo(p, 'nombre', 'EXAMEN')).strip().upper()
        materia_raw = str(buscar_campo(p, 'materia', 'MATERIA')).strip().upper()
        grado_raw = str(buscar_campo(p, 'grado', 'GENERAL')).strip().upper()
        
        etiqueta_selector = f"{nombre_raw} - {materia_raw} ({grado_raw})"
        diccionario_pruebas[etiqueta_selector] = p

    # El selector ahora se alimenta de TODAS las pruebas en el catálogo, no de las notas
    prueba_sel = st.selectbox("🎯 SELECCIONE LA EVALUACIÓN MÁSTER PARA AUDITAR:", list(diccionario_pruebas.keys()))

    # =================================================================
    # 🗃️ PROCESAMIENTO
    # =================================================================
    datos_prueba_activa = diccionario_pruebas[prueba_sel]
    id_prueba_activa = datos_prueba_activa.get("id_prueba") or datos_prueba_activa.get("id")
    
    # Filtramos las notas solo al momento de procesar, no antes
    df_notas = pd.DataFrame(notas_raw) if notas_raw else pd.DataFrame()
    if not df_notas.empty:
        df_notas.columns = [c.lower() for c in df_notas.columns]
        df_notas = df_notas[df_notas['id_prueba'] == id_prueba_activa]

    # ... (El resto de tu código de gráficos y tablas sigue igual abajo)
