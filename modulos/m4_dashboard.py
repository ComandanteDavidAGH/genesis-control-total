import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os
from supabase import create_client

# 🛡️ PUENTE DE RUTA TÁCTICO
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
    # ⚡ Inyección visual
    inyectar_estilos_omega()

    st.markdown("<h1 class='titulo-dash'>📊 Dashboard Analítico e Informes</h1>", unsafe_allow_html=True)
    st.markdown("<h3 class='subtitulo-dash'>Consola Central de Rendimiento y Exportación</h3>", unsafe_allow_html=True)
    st.markdown("---")

    try:
        supabase = iniciar_conexion()
        
        # 1. Carga de datos
        res_pruebas = supabase.table("pruebas_maestras").select("*").execute()
        res_notas = supabase.table("respuestas_estudiantes").select("id_prueba, materia, nota").execute()
        
        pruebas = res_pruebas.data
        notas_raw = res_notas.data
        
        if not pruebas:
            st.warning("⚠️ No se encontraron pruebas en el sistema.")
            return
            
    except Exception as e:
        st.error(f"🚨 Error crítico de conexión: {e}")
        return

    # 2. Mapeo lógico (Consolidación)
    ids_con_notas = {n.get("id_prueba") for n in notas_raw if n.get("id_prueba")}
    diccionario_pruebas = {}
    
    for p in pruebas:
        id_p = p.get("id_prueba") or p.get("id")
        nom = str(buscar_campo(p, 'nombre', 'SIN NOMBRE')).strip().upper()
        mat = str(buscar_campo(p, 'materia', 'SIN MATERIA')).strip().upper()
        gra = str(buscar_campo(p, 'grado', 'SIN GRADO')).strip().upper()
        
        estado = "✅" if id_p in ids_con_notas else "⚠️"
        label = f"{estado} {nom} - {mat} ({gra})"
        diccionario_pruebas[label] = p

    # 3. Selector Universal
    opciones = sorted(list(diccionario_pruebas.keys()))
    prueba_sel = st.selectbox("🎯 SELECCIONE LA EVALUACIÓN MÁSTER PARA AUDITAR:", opciones)

    # 4. Procesamiento de datos filtrados
    datos_prueba_activa = diccionario_pruebas[prueba_sel]
    id_prueba_activa = datos_prueba_activa.get("id_prueba") or datos_prueba_activa.get("id")
    
    # Filtrar notas para la prueba seleccionada
    df_notas = pd.DataFrame(notas_raw)
    df_filtrado = df_notas[df_notas['id_prueba'] == id_prueba_activa] if not df_notas.empty else pd.DataFrame()

    # 5. Visualización de Resultados
    if not df_filtrado.empty:
        st.success(f"✅ Datos cargados correctamente para: {prueba_sel}")
        
        # Ejemplo de métrica rápida
        col1, col2 = st.columns(2)
        col1.metric("Estudiantes Evaluados", len(df_filtrado))
        col2.metric("Promedio General", round(df_filtrado['nota'].mean(), 2))
        
        # Gráfico (Ajusta según tu necesidad)
        fig = px.histogram(df_filtrado, x="nota", title="Distribución de Calificaciones")
        st.plotly_chart(fig, use_container_width=True)
        
        # Tabla de detalle
        st.subheader("📋 Matriz de Calificaciones")
        st.dataframe(df_filtrado, use_container_width=True)
    else:
        st.error("❌ La prueba seleccionada no tiene notas registradas en el sistema.")

# Ejecución
if __name__ == "__main__":
    ejecutar()
