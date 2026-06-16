import streamlit as st
import pandas as pd
import plotly.express as px
import io
import sys
import os
from supabase import create_client

# 🛡️ PUENTE DE RUTA TÁCTICO (Mantiene la estabilidad sin error de importación)
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
                return valor if valor is not None else predeterminado
    except: pass
    return predeterminado

def ejecutar():
    # ⚡ Inyección visual unificada Génesis Omega Pro
    inyectar_estilos_omega()

    # ✨ Títulos ORIGINALES
    st.markdown("<h1 class='titulo-dash'>📊 Dashboard Analítico e Informes</h1>", unsafe_allow_html=True)
    st.markdown("<h3 class='subtitulo-dash'>Consola Central de Rendimiento y Exportación de Matrices de Calificación</h3>", unsafe_allow_html=True)
    st.markdown("---")

    try:
        supabase = iniciar_conexion()
        # Carga masiva sin filtros
        res_pruebas = supabase.table("pruebas_maestras").select("*").execute()
        res_notas = supabase.table("respuestas_estudiantes").select("*").execute()
        pruebas = res_pruebas.data
        notas_raw = res_notas.data
    except Exception as e:
        st.error(f"🚨 Error de conexión: {e}")
        return

    if not pruebas:
        st.info("📭 No hay datos disponibles.")
        return

    # 🎛️ SELECTOR GENERAL (RECONSTRUCCIÓN TOTAL)
    # Creamos un diccionario donde la clave es la descripción completa y el valor es el objeto p completo
    diccionario_pruebas = {}
    for p in pruebas:
        nom = str(buscar_campo(p, 'nombre', 'SIN NOMBRE')).strip().upper()
        mat = str(buscar_campo(p, 'materia', 'SIN MATERIA')).strip().upper()
        gra = str(buscar_campo(p, 'grado', 'SIN GRADO')).strip().upper()
        label = f"{nom} - {mat} ({gra})"
        diccionario_pruebas[label] = p

    # Widget selector que muestra TODAS las opciones encontradas
    opciones = list(diccionario_pruebas.keys())
    prueba_sel = st.selectbox("🎯 SELECCIONE LA EVALUACIÓN MÁSTER PARA AUDITAR:", opciones)

    # Procesamiento con la selección elegida
    datos_prueba_activa = diccionario_pruebas[prueba_sel]
    id_prueba_activa = datos_prueba_activa.get("id_prueba") or datos_prueba_activa.get("id")
    
    # ... (Aquí continúa tu lógica original de df_notas y gráficos)
