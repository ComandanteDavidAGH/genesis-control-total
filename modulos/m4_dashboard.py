import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os
from supabase import create_client

# 🛡️ PUENTE TÁCTICO DE RUTA
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from estilos_globales import inyectar_estilos_omega

def iniciar_conexion():
    return create_client(st.secrets["SUPABASE_URL"].strip(), st.secrets["SUPABASE_KEY"].strip())

def ejecutar():
    inyectar_estilos_omega()
    st.markdown("<h1 class='titulo-dash'>📊 Dashboard Analítico e Informes</h1>", unsafe_allow_html=True)
    st.markdown("<h3 class='subtitulo-dash'>Consola Central de Rendimiento y Exportación de Matrices de Calificación</h3>", unsafe_allow_html=True)
    
    supabase = iniciar_conexion()

    # 1. Traer TODAS las pruebas maestras
    res_p = supabase.table("pruebas_maestras").select("*").execute()
    pruebas = res_p.data
    
    # 2. Traer TODAS las notas (la tabla de respuestas)
    res_n = supabase.table("respuestas_estudiantes").select("*").execute()
    notas = res_n.data
    
    if not pruebas:
        st.info("📭 No hay evaluaciones en el sistema.")
        return

    # 3. Mapeo: Creamos el índice de pruebas disponibles
    mapa_pruebas = {f"{p.get('nombre')} - {p.get('materia')} ({p.get('grado')})": p for p in pruebas}
    
    # 4. Selector Maestro
    seleccion = st.selectbox("🎯 SELECCIONE LA EVALUACIÓN MÁSTER PARA AUDITAR:", list(mapa_pruebas.keys()))
    
    # 5. Cruce de Datos (Lógica de filtrado por ID)
    prueba_activa = mapa_pruebas[seleccion]
    id_activa = prueba_activa.get("id_prueba") or prueba_activa.get("id")
    
    # Filtramos el DataFrame de notas con los datos que llegaron de Supabase
    df_notas = pd.DataFrame(notas)
    if not df_notas.empty:
        df_notas.columns = [c.lower() for c in df_notas.columns]
        df_filtrado = df_notas[df_notas['id_prueba'] == id_activa]
    else:
        df_filtrado = pd.DataFrame()

    # 6. Mostrar resultados
    st.markdown(f"### Resultados para: {seleccion}")
    if not df_filtrado.empty:
        st.dataframe(df_filtrado, use_container_width=True)
    else:
        st.warning("⚠️ No se encontraron notas para esta materia en la tabla de respuestas.")

if __name__ == "__main__":
    ejecutar()
