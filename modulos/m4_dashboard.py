import streamlit as st
import pandas as pd
import plotly.express as px
import io
import sys
import os
from supabase import create_client

# =================================================================
# 🛡️ PUENTE TÁCTICO DE RUTA (SOLUCIONA ERROR DE IMPORTACIÓN)
# =================================================================
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from estilos_globales import inyectar_estilos_omega

# =================================================================
# 🔒 CONEXIÓN AL BÚNKER DE DATOS INSTITUCIONAL
# =================================================================
def iniciar_conexion():
    """Establece conexión segura con la base de datos Supabase."""
    url = st.secrets["SUPABASE_URL"].strip()
    key = st.secrets["SUPABASE_KEY"].strip()
    return create_client(url, key)

def buscar_campo(diccionario, nombre_campo, predeterminado=""):
    """Busca un campo en un diccionario de forma segura."""
    if diccionario is None: return predeterminado
    for llave, valor in diccionario.items():
        if str(llave).lower() == nombre_campo.lower():
            if valor is not None: return valor
    return predeterminado

# =================================================================
# 🚀 EJECUCIÓN CENTRAL DEL MÓDULO DASHBOARD
# =================================================================
def ejecutar():
    # 1. Aplicar estilos sin sobreescribir contenedores nativos
    inyectar_estilos_omega()

    st.markdown("<h1 class='titulo-dash'>📊 Dashboard Analítico e Informes</h1>", unsafe_allow_html=True)
    st.markdown("<h3 class='subtitulo-dash'>Consola Central de Rendimiento Institucional</h3>", unsafe_allow_html=True)
    st.markdown("---")

    # 2. Conexión y Carga de Datos
    try:
        supabase = iniciar_conexion()
        res_pruebas = supabase.table("pruebas_maestras").select("*").execute()
        res_notas = supabase.table("respuestas_estudiantes").select("*").execute()
    except Exception as e:
        st.error(f"🚨 Error crítico de conexión: {e}")
        return

    pruebas = res_pruebas.data
    notas_raw = res_notas.data

    if not pruebas:
        st.info("📭 No hay evaluaciones maestras registradas.")
        return

    # 3. Mapeo Exhaustivo de Pruebas (SIN FILTROS)
    # Esto asegura que todas las pruebas aparezcan en el selector
    mapa_pruebas = {}
    for p in pruebas:
        nombre = str(buscar_campo(p, 'nombre', 'EXAMEN')).strip().upper()
        materia = str(buscar_campo(p, 'materia', 'MATERIA')).strip().upper()
        grado = str(buscar_campo(p, 'grado', 'GENERAL')).strip().upper()
        etiqueta = f"{nombre} - {materia} ({grado})"
        mapa_pruebas[etiqueta] = p

    # 4. Widget Selector Maestro
    prueba_sel = st.selectbox("🎯 SELECCIONE LA EVALUACIÓN MÁSTER PARA AUDITAR:", list(mapa_pruebas.keys()))
    
    # 5. Procesamiento
    datos_prueba = mapa_pruebas[prueba_sel]
    id_prueba = datos_prueba.get("id_prueba") or datos_prueba.get("id")
    
    df_notas = pd.DataFrame(notas_raw)
    if not df_notas.empty:
        df_notas.columns = [c.lower() for c in df_notas.columns]
        df_filtrado = df_notas[df_notas['id_prueba'] == id_prueba]
    else:
        df_filtrado = pd.DataFrame()

    # 6. Salida Visual
    c1, c2 = st.columns([1, 1.5])
    
    with c1:
        st.markdown("### 📝 Detalles Técnicos")
        tabla_detalles = pd.DataFrame({
            "Especificación": ["Examen", "Asignatura", "Puntaje Máximo"],
            "Detalle": [
                str(buscar_campo(datos_prueba, 'nombre')).upper(),
                str(buscar_campo(datos_prueba, 'materia')).upper(),
                str(buscar_campo(datos_prueba, 'puntaje_maximo', '5.0'))
            ]
        })
        st.dataframe(tabla_detalles, use_container_width=True, hide_index=True)

    with c2:
        st.markdown("### 📊 Registro de Notas")
        if not df_filtrado.empty:
            st.data_editor(df_filtrado, use_container_width=True, hide_index=True, disabled=True)
        else:
            st.warning("⚠️ No se registran notas para esta evaluación.")

if __name__ == "__main__":
    ejecutar()
