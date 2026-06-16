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

# =================================================================
# 🛡️ SENSOR DETECTOR INALÁMBRICO DE COLUMNAS
# =================================================================
def buscar_campo(diccionario, nombre_campo, predeterminado=""):
    if diccionario is None:
        return predeterminado
    try:
        if hasattr(diccionario, 'empty') and diccionario.empty:
            return predeterminado
    except:
        pass
    try:
        for llave, valor in diccionario.items():
            if str(llave).lower() == nombre_campo.lower():
                if valor is not None and str(valor).strip().lower() not in ['none', 'null', '']:
                    return valor
    except:
        pass
    return predeterminado

def ejecutar():
    # ⚡ Inyección visual unificada Génesis Omega Pro (Llamada única)
    inyectar_estilos_omega()

    st.markdown("<p class='titulo-dash'>📊 Dashboard Analítico e Informes</p>", unsafe_allow_html=True)
    st.markdown("<p class='subtitulo-dash'>Consola Central de Rendimiento y Exportación de Matrices de Calificación</p>", unsafe_allow_html=True)
    st.markdown("---")

    try:
        supabase = iniciar_conexion()
    except Exception:
        st.error("⚠️ Falla de enlace con la base de datos central.")
        return

    # 📥 DESCARGA DE COMPONENTES CRIPTOGRÁFICOS
    with st.spinner("Sincronizando registros analíticos..."):
        try:
            res_pruebas = supabase.table("pruebas_maestras").select("*").execute()
            pruebas = res_pruebas.data
            res_notas = supabase.table("respuestas_estudiantes").select("*").execute()
            notas_raw = res_notas.data
        except Exception as e:
            st.error(f"Error de lectura en el búnker: {e}")
            return

    if not pruebas:
        st.info("📭 No se registran evaluaciones maestras en el banco de datos para analizar.")
        return

    # 🎛️ SELECTOR GENERAL DE PRUEBAS
    diccionario_pruebas = {}
    for idx, p in enumerate(pruebas):
        nombre_raw = str(buscar_campo(p, 'nombre', 'EXAMEN SIN NOMBRE')).strip().upper()
        materia_raw = str(buscar_campo(p, 'materia', 'MATERIA')).strip().upper()
        grado_raw = str(buscar_campo(p, 'grado', 'GENERAL')).strip().upper()
        etiqueta_selector = f"{nombre_raw} - {materia_raw} ({grado_raw})"
        if etiqueta_selector in diccionario_pruebas:
            id_seguro = p.get('id_prueba', p.get('id', idx))
            etiqueta_selector = f"{etiqueta_selector} (ID: {id_seguro})"
        diccionario_pruebas[etiqueta_selector] = p

    prueba_sel = st.selectbox("🎯 SELECCIONE LA EVALUACIÓN MÁSTER PARA AUDITAR:", list(diccionario_pruebas.keys()))

    datos_prueba_activa = diccionario_pruebas[prueba_sel]
    id_prueba_activa = datos_prueba_activa.get("id_prueba") or datos_prueba_activa.get("id")
    df_notas = pd.DataFrame(notas_raw) if notas_raw else pd.DataFrame()
    
    if not df_notas.empty:
        df_notas.columns = [c.lower() for c in df_notas.columns]
        df_notas = df_notas[df_notas['id_prueba'] == id_prueba_activa]

    # [RESTO DE TU LÓGICA DE DATOS AQUÍ...]
    # (El código continúa igual hasta el final, solo asegúrate de mantener la sangría de 4 espacios)
