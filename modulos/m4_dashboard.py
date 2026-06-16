import streamlit as st
import pandas as pd
import plotly.express as px
import io
import sys
import os
from supabase import create_client

# 🛡️ PUENTE TÁCTICO PARA IMPORTAR ESTILOS DESDE LA RAÍZ
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
# 🚀 EJECUCIÓN CENTRAL
# =================================================================
def ejecutar():
    inyectar_estilos_omega()

    st.markdown("<h1 class='titulo-dash'>📊 Dashboard Analítico e Informes</h1>", unsafe_allow_html=True)
    st.markdown("<h3 class='subtitulo-dash'>Consola Central de Rendimiento y Exportación de Matrices de Calificación</h3>", unsafe_allow_html=True)
    st.markdown("---")

    try:
        supabase = iniciar_conexion()
    except Exception:
        st.error("⚠️ Falla de enlace con la base de datos central.")
        return

    with st.spinner("Sincronizando registros analíticos..."):
        try:
            res_pruebas = supabase.table("pruebas_maestras").select("*").execute()
            pruebas = res_pruebas.data
            res_notas = supabase.table("respuestas_estudiantes").select("*").execute()
            notas_raw = res_notas.data
        except Exception as e:
            st.error(f"🚨 Error de lectura: {e}")
            return

    if not pruebas:
        st.info("📭 No hay evaluaciones registradas.")
        return

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

    df_informe_limpio = pd.DataFrame()
    conteo_niveles = {"Bajo (<60%)": 0, "Básico (60-79%)": 0, "Alto (80-89%)": 0, "Superior (≥90%)": 0}

    if not df_notas.empty:
        filas_limpias = []
        for _, fila in df_notas.iterrows():
            estudiante_str = str(buscar_campo(fila, 'estudiante', 'ALUMNO ANÓNIMO'))
            nombre_final, curso_final = estudiante_str, "SIN CURSO"
            if "(" in estudiante_str and ")" in estudiante_str:
                parts = estudiante_str.split("(")
                nombre_final, curso_final = parts[0].strip(), parts[1].replace(")", "").strip()

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
                "ESTUDIANTE": nombre_final.upper(), "CURSO": curso_final.upper(),
                "NOTA": round(nota, 2), "MÁXIMA": round(max_p, 2),
                "EFECTIVIDAD": f"{pct:.1f}%", "RANGO": nivel, "ESTADO": estado
            })
        if filas_limpias:
            df_informe_limpio = pd.DataFrame(filas_limpias).sort_values(by="ESTUDIANTE")

    c1, c2 = st.columns([1, 1.2])
    with c1:
        st.markdown("### 📝 Detalles de Operación")
        tabla_detalles = pd.DataFrame({
            "Especificación": ["Examen", "Asignatura", "Preguntas", "Máximo"],
            "Detalle": [str(buscar_campo(datos_prueba_activa, 'nombre')).upper(), 
                        str(buscar_campo(datos_prueba_activa, 'materia')).upper(),
                        f"{buscar_campo(datos_prueba_activa, 'total_preguntas', 10)} Ítems",
                        f"{float(buscar_campo(datos_prueba_activa, 'puntaje_maximo', 5.0)):.1f} Pts"]
        })
        st.dataframe(tabla_detalles, use_container_width=True, hide_index=True)
        st.markdown("### 📥 Descargar Reportes:")
        if not df_informe_limpio.empty:
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                df_informe_limpio.to_excel(writer, index=False)
            st.download_button("🟢 Descargar Excel", buffer.getvalue(), "REPORTE.xlsx", "application/vnd.ms-excel", use_container_width=True)
    
    with c2:
        st.markdown("### 📊 Distribución")
        fig = px.bar(x=list(conteo_niveles.keys()), y=list(conteo_niveles.values()), color=list(conteo_niveles.keys()), text_auto=True, height=300)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.markdown("### 📋 Sabana General de Notas")
    if not df_informe_limpio.empty:
        st.data_editor(df_informe_limpio, use_container_width=True, hide_index=True, disabled=True)
