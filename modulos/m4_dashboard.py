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
# 🚀 EJECUCIÓN CENTRAL DEL MÓDULO DASHBOARD
# =================================================================
def ejecutar():
    inyectar_estilos_omega()

    st.markdown("<h1 class='titulo-dash'>📊 Dashboard Analítico e Informes</h1>", unsafe_allow_html=True)
    st.markdown("<h3 class='subtitulo-dash'>Consola Central: Auditoría de notas_consolidadas</h3>", unsafe_allow_html=True)
    st.markdown("---")

    try:
        supabase = iniciar_conexion()
        # Traemos toda la data de la tabla maestra de notas
        res_notas = supabase.table("notas_consolidadas").select("*").execute()
        df_total = pd.DataFrame(res_notas.data)
        
        if df_total.empty:
            st.info("📭 No hay registros en notas_consolidadas.")
            return

        # =================================================================
        # 🎛️ SELECTOR DE ASIGNATURAS (Alimentado por la tabla correcta)
        # =================================================================
        materias = sorted(df_total['ASIGNATURA'].dropna().unique().tolist())
        materia_sel = st.selectbox("🎯 SELECCIONE LA ASIGNATURA PARA AUDITAR:", materias)

        # Filtramos data para la asignatura elegida
        df_filtrado = df_total[df_total['ASIGNATURA'] == materia_sel].copy()

        # =================================================================
        # 📐 PANELES DE DETALLE Y DISTRIBUCIÓN
        # =================================================================
        c1, c2 = st.columns([1, 1.2])

        with c1:
            st.markdown("### 📝 Detalles de Operación")
            # Resumen técnico
            total_estudiantes = len(df_filtrado)
            promedio = df_filtrado[['P1', 'P2']].mean().mean() # Ajustar según columnas P1, P2...
            
            st.metric("Total Registros", total_estudiantes)
            st.metric("Promedio General", f"{promedio:.2f}")

            # Exportación
            st.markdown("### 📥 Descargar Reportes:")
            csv = df_filtrado.to_csv(index=False).encode('utf-8')
            st.download_button("📄 Descargar CSV", csv, f"REPORTE_{materia_sel}.csv", "text/csv", use_container_width=True)

        with c2:
            st.markdown("### 📊 Comportamiento de Notas")
            # Gráfico de barras simple para P1
            fig = px.bar(df_filtrado, x="NOMBRE_COMPLETO", y="P1", title=f"Resultados P1 - {materia_sel}")
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")
        st.markdown("### 📋 Sabana Detallada")
        st.data_editor(df_filtrado, use_container_width=True, hide_index=True, disabled=True)

    except Exception as e:
        st.error(f"🚨 Error en el sistema: {e}")

if __name__ == "__main__":
    ejecutar()
