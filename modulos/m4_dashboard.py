import streamlit as st
import pandas as pd
import plotly.express as px
import io
from supabase import create_client
from estilos_globales import inyectar_estilos_omega

def iniciar_conexion():
    url = st.secrets["SUPABASE_URL"].strip()
    key = st.secrets["SUPABASE_KEY"].strip()
    return create_client(url, key)

def buscar_campo(diccionario, nombre_campo, predeterminado=""):
    if diccionario is None: return predeterminado
    try:
        if hasattr(diccionario, 'empty') and diccionario.empty: return predeterminado
    except: pass
    try:
        for llave, valor in diccionario.items():
            if str(llave).lower() == nombre_campo.lower():
                if valor is not None and str(valor).strip().lower() not in ['none', 'null', '']:
                    return valor
    except: pass
    return predeterminado

def ejecutar():
    inyectar_estilos_omega()
    
    st.markdown("<h1 class='titulo-dash'>📊 Dashboard Analítico e Informes</h1>", unsafe_allow_html=True)
    st.markdown("<h3 class='subtitulo-dash'>Consola Central de Rendimiento y Exportación de Matrices de Calificación</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    # ... (Aquí va el resto de tu lógica que tenías antes) ...
    # Asegúrate de que TODAS las líneas debajo de 'def ejecutar():' 
    # tengan un margen de 4 espacios a la izquierda.
