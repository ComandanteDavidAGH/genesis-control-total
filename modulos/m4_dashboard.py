import streamlit as st
import pandas as pd
from supabase import create_client

def iniciar_conexion():
    url = st.secrets["SUPABASE_URL"].strip()
    key = st.secrets["SUPABASE_KEY"].strip()
    return create_client(url, key)

def ejecutar():
    st.markdown("""
        <style>
        .titulo-genesis { color: #0d1b2a; font-family: 'Arial Black'; font-size: 32px; }
        .subtitulo-genesis { color: #d4af37; font-weight: bold; font-size: 13px; text-transform: uppercase; }
        .hud-container { display: flex; gap: 15px; margin-bottom: 25px; margin-top: 15px; }
        .hud-card { flex: 1; background: #ffffff; border-top: 3px solid #0d1b2a; border-radius: 4px 4px 12px 12px; padding: 12px 15px; text-align: center; box-shadow: 0 10px 25px rgba(13, 27, 42, 0.04); }
        .hud-value { font-size: 32px; font-family: 'Arial Black'; font-weight: 900; color: #0d1b2a; }
        .contenedor-matriz { background: #ffffff; border-radius: 12px; border: 1px solid #e5e5e5; border-top: 4px solid #0d1b2a; padding: 20px; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<p class='titulo-genesis'>📊 Panel del Cuestionario y Analítica</p>", unsafe_allow_html=True)
    st.markdown("<p class='subtitulo-genesis'>Ecosistema de Inteligencia Académica</p>", unsafe_allow_html=True)
    st.markdown("---")

    tab1, tab2 = st.tabs(["📊 Analítica General", "📂 Consolidación por Período"])

    with tab1:
        try:
            supabase = iniciar_conexion()
            estudiantes_base = []
            offset, chunk_size = 0, 1000
            
            with st.spinner("Compilando telemetría analítica..."):
                while True:
                    resultado = supabase.table("data_estudiantes")\
                        .select('*')\
                        .range(offset, offset + chunk_size - 1).execute()
                    if not resultado.data: break
                    estudiantes_base.extend(resultado.data)
                    if len(resultado.data) < chunk_size: break
                    offset += chunk_size
        except Exception as e:
            st.error(f"🚨 Error en la Sincronización de Tablas: {e}")
            return

        if estudiantes_base:
            df = pd.DataFrame(estudiantes_base)
            df.columns = [c.lower() for c in df.columns]
            
            col_id = "id_estudiante" if "id_estudiante" in df.columns else df.columns[0]
            df_unicos = df.drop_duplicates(subset=[col_id])
            total_alumnos = len(df_unicos)

            st.markdown(f"""
                <div class="hud-container">
                    <div class="hud-card">
                        <div style="font-size:11px; font-weight:800; color:#5c677d;">👥 AUDITORÍA DE ALUMNOS</div>
                        <div class="hud-value">{total_alumnos}</div>
                    </div>
                    <div class="hud-card" style="border-top-color: #d4af37;">
                        <div style="font-size:11px; font-weight:800; color:#bfa12a;">📝 EVALUACIONES PROCESADAS</div>
                        <div class="hud-value" style="color: #d4af37;">0</div>
                    </div>
                    <div class="hud-card" style="border-top-color: #2b9348;">
                        <div style="font-size:11px; font-weight:800; color:#2b9348;">📈 EFECTIVIDAD INSTITUCIONAL</div>
                        <div class="hud-value" style="color: #2b9348;">100%</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
