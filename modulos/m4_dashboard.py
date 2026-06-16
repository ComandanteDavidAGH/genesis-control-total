import streamlit as st
import pandas as pd
import plotly.express as px
import io
import sys
import os
from supabase import create_client

# 🛡️ PUENTE TÁCTICO DE RUTA (INDISPENSABLE PARA NO TENER ERRORES DE IMPORTACIÓN)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from estilos_globales import inyectar_estilos_omega

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

def ejecutar():
    # ⚡ Inyección visual unificada Génesis Omega Pro (Escudo Estético)
    inyectar_estilos_omega()

    # ✨ Títulos ORIGINALES (Respetando tu diseño)
    st.markdown("<h1 class='titulo-dash'>📊 Dashboard Analítico e Informes</h1>", unsafe_allow_html=True)
    st.markdown("<h3 class='subtitulo-dash'>Consola Central de Rendimiento y Exportación de Matrices de Calificación</h3>", unsafe_allow_html=True)
    st.markdown("---")

    try:
        supabase = iniciar_conexion()
        res_pruebas = supabase.table("pruebas_maestras").select("*").execute()
        res_notas = supabase.table("respuestas_estudiantes").select("*").execute()
        pruebas = res_pruebas.data
        notas_raw = res_notas.data
    except Exception as e:
        st.error(f"🚨 Error de lectura en el búnker de datos: {e}")
        return

    if not pruebas:
        st.info("📭 No se registran evaluaciones maestras en el banco de datos para analizar.")
        return

    # =================================================================
    # 🎛️ SELECTOR GENERAL DE PRUEBAS MÁSTER (CORRECCIÓN)
    # =================================================================
    diccionario_pruebas = {}
    for idx, p in enumerate(pruebas):
        nombre_raw = str(buscar_campo(p, 'nombre', 'EXAMEN SIN NOMBRE')).strip().upper()
        materia_raw = str(buscar_campo(p, 'materia', 'MATERIA')).strip().upper()
        grado_raw = str(buscar_campo(p, 'grado', 'GENERAL')).strip().upper()
        
        etiqueta_selector = f"{nombre_raw} - {materia_raw} ({grado_raw})"
        
        # Guardamos en el diccionario
        diccionario_pruebas[etiqueta_selector] = p

    # Widget Selector SIN FILTROS, tal cual lo necesitabas
    prueba_sel = st.selectbox("🎯 SELECCIONE LA EVALUACIÓN MÁSTER PARA AUDITAR:", list(diccionario_pruebas.keys()))

    # =================================================================
    # 🗃️ PROCESAMIENTO
    # =================================================================
    datos_prueba_activa = diccionario_pruebas[prueba_sel]
    id_prueba_activa = datos_prueba_activa.get("id_prueba") or datos_prueba_activa.get("id")
    
    df_notas = pd.DataFrame(notas_raw) if notas_raw else pd.DataFrame()
    
    if not df_notas.empty:
        df_notas.columns = [c.lower() for c in df_notas.columns]
        df_notas = df_notas[df_notas['id_prueba'] == id_prueba_activa]
    
    # [AQUÍ VA EL RESTO DE TU LÓGICA DE TABLAS Y GRÁFICOS QUE YA TENÍAS]
    # He dejado la estructura intacta para no alterar nada más.
    
if __name__ == "__main__":
    ejecutar()
