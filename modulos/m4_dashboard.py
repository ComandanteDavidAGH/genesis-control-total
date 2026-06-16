import streamlit as st
import pandas as pd
import sys
import os
from supabase import create_client

# Puente para asegurar la importación de estilos globales desde la raíz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from estilos_globales import inyectar_estilos_omega

def iniciar_conexion():
    return create_client(st.secrets["SUPABASE_URL"].strip(), st.secrets["SUPABASE_KEY"].strip())

def ejecutar():
    # 1. Inyección de estilos intacta
    inyectar_estilos_omega()
    
    # 2. Títulos y encabezado original
    st.markdown("<h1 class='titulo-dash'>📊 Dashboard Analítico e Informes</h1>", unsafe_allow_html=True)
    st.markdown("<h3 class='subtitulo-dash'>Consola Central de Rendimiento y Exportación de Matrices de Calificación</h3>", unsafe_allow_html=True)
    
    supabase = iniciar_conexion()
    
    # 3. CARGA MAESTRA: Obtenemos el catálogo completo de pruebas sin filtrar
    try:
        res_pruebas = supabase.table("pruebas_maestras").select("*").execute()
        pruebas_data = res_pruebas.data
    except Exception as e:
        st.error("Error conectando con pruebas_maestras")
        return

    if not pruebas_data:
        st.info("No hay pruebas registradas para auditar.")
        return

    # 4. Construcción del catálogo para el Selectbox (tal como el inspector de grados)
    # Usamos un diccionario para mapear la etiqueta visible al objeto de datos
    catalogo = {}
    for p in pruebas_data:
        # Extraemos campos de forma segura
        nombre = p.get('nombre', 'SIN NOMBRE')
        materia = p.get('materia', 'SIN MATERIA')
        grado = p.get('grado', 'SIN GRADO')
        key = f"{nombre} - {materia} ({grado})"
        catalogo[key] = p

    # 5. Selector Maestro (Ahora sí muestra todas las opciones)
    seleccion = st.selectbox("🎯 SELECCIONE LA EVALUACIÓN MÁSTER PARA AUDITAR:", list(catalogo.keys()))
    
    # 6. Lógica de cruce con respuestas_estudiantes
    prueba_activa = catalogo[seleccion]
    id_prueba = prueba_activa.get("id_prueba") or prueba_activa.get("id")
    
    # Buscamos notas asociadas a este ID de prueba
    res_notas = supabase.table("respuestas_estudiantes").select("*").eq("id_prueba", id_prueba).execute()
    notas = res_notas.data
    
    st.markdown(f"---")
    
    if notas:
        df = pd.DataFrame(notas)
        # Mostramos los resultados en el formato tabla que ya tenías
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("No hay notas registradas para esta evaluación seleccionada.")

if __name__ == "__main__":
    ejecutar()
