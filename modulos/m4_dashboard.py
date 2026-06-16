import streamlit as st
import pandas as pd
import plotly.express as px
import io
import sys
import os
from supabase import create_client

# 🛡️ PUENTE DE RUTA TÁCTICO (NECESARIO PARA IMPORTAR ESTILOS)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
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
    # ⚡ Inyección visual
    inyectar_estilos_omega()

    # ✨ Títulos
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

    # 🎛️ SELECTOR GENERAL (RECONSTRUCCIÓN PARA MOSTRAR TODO)
    diccionario_pruebas = {}
    for idx, p in enumerate(pruebas):
        nombre_raw = str(buscar_campo(p, 'nombre', 'EXAMEN SIN NOMBRE')).strip().upper()
        materia_raw = str(buscar_campo(p, 'materia', 'MATERIA')).strip().upper()
        grado_raw = str(buscar_campo(p, 'grado', 'GENERAL')).strip().upper()
        
        etiqueta_selector = f"{nombre_raw} - {materia_raw} ({grado_raw})"
        diccionario_pruebas[etiqueta_selector] = p

    prueba_sel = st.selectbox("🎯 SELECCIONE LA EVALUACIÓN MÁSTER PARA AUDITAR:", list(diccionario_pruebas.keys()))

    # 🗃️ PROCESAMIENTO BIÓNICO
    datos_prueba_activa = diccionario_pruebas[prueba_sel]
    id_prueba_activa = datos_prueba_activa.get("id_prueba") or datos_prueba_activa.get("id")
    
    df_notas = pd.DataFrame(notas_raw) if notas_raw else pd.DataFrame()
    
    if not df_notas.empty:
        df_notas.columns = [c.lower() for c in df_notas.columns]
        df_notas = df_notas[df_notas['id_prueba'] == id_prueba_activa]

    df_informe_limpio = pd.DataFrame()
    conteo_niveles = {"Bajo (<60%)": 0, "Básico (60-79%)": 0, "Alto (80-89%)": 0, "Superior (≥90%)": 0}

    if not df_notas.empty:
        filas_limpias = []
        for _, fila in df_notas.iterrows():
            estudiante_str = str(buscar_campo(fila, 'estudiante', 'ALUMNO ANÓNIMO'))
            nombre_final = estudiante_str
            curso_final = "SIN CURSO"
            if "(" in estudiante_str and ")" in estudiante_str:
                parts = estudiante_str.split("(")
                nombre_final = parts[0].strip()
                curso_final = parts[1].replace(")", "").strip()

            try:
                pct = float(buscar_campo(fila, 'porcentaje', 0.0))
                nota = float(buscar_campo(fila, 'puntaje_obtenido', 0.0))
                max_p = float(buscar_campo(fila, 'puntaje_maximo', 5.0))
            except: pct, nota, max_p = 0.0, 0.0, 5.0
            
            if pct < 60.0: nivel, estado = "Bajo (<60%)", "REPROBADO ❌"
            elif 60.0 <= pct < 80.0: nivel, estado = "Básico (60-79%)", "APROBADO ✅"
            elif 80.0 <= pct < 90.0: nivel, estado = "Alto (80-89%)", "APROBADO ✅"
            else: nivel, estado = "Superior (≥90%)", "APROBADO ✅"
            
            conteo_niveles[nivel] += 1
            filas_limpias.append({
                "ESTUDIANTE MATRÍCULA": nombre_final.upper(),
                "CURSO / GRADO": curso_final.upper(),
                "NOTA LOGRADA": round(nota, 2),
                "NOTA MÁXIMA": round(max_p, 2),
                "EFECTIVIDAD %": f"{pct:.1f}%",
                "RANGO COGNITIVO": nivel,
                "ESTADO ACADÉMICO": estado
            })
        if filas_limpias:
            df_informe_limpio = pd.DataFrame(filas_limpias).sort_values(by="ESTUDIANTE MATRÍCULA")

    # 📐 DISTRIBUCIÓN GRÁFICA Y PANELES
    c1, c2 = st.columns([1, 1.2])
    with c1:
        st.markdown("### 📝 Detalles de Operación")
        tabla_detalles = pd.DataFrame({
            "Especificación": ["Examen Activo", "Asignatura", "Puntaje Máximo"],
            "Detalle": [
                str(buscar_campo(datos_prueba_activa, 'nombre', 'EXAMEN')).upper(),
                str(buscar_campo(datos_prueba_activa, 'materia', 'MATERIA')).upper(),
                f"{float(buscar_campo(datos_prueba_activa, 'puntaje_maximo', 5.0)):.1f} Pts"
            ]
        })
        st.dataframe(tabla_detalles, use_container_width=True, hide_index=True)

    with c2:
        st.markdown("### 📊 Distribución de Puntuaciones")
        df_grafico = pd.DataFrame({"Nivel": list(conteo_niveles.keys()), "Hojas": list(conteo_niveles.values())})
        fig = px.bar(df_grafico, x="Nivel", y="Hojas", color="Nivel", text_auto=True, height=320)
        fig.update_layout(showlegend=False, margin=dict(l=10, r=10, t=10, b=10), xaxis_title=None)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    st.markdown("---")
    st.markdown("### 📋 Control de Asistencia y Sabana Escaneada")
    if not df_informe_limpio.empty:
        st.data_editor(df_informe_limpio, use_container_width=True, hide_index=True, disabled=True)
    else:
        st.info("💡 Consola Vacía: No se registran exámenes presentados.")

if __name__ == "__main__":
    ejecutar()
