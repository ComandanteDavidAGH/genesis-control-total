import streamlit as st
import pandas as pd
from supabase import create_client

def iniciar_conexion():
    # 🔒 PROTOCOLO OFICIAL: Extracción segura desde el entorno cifrado de Streamlit
    url = st.secrets["SUPABASE_URL"].strip()
    key = st.secrets["SUPABASE_KEY"].strip()
    
    # Telemetría de diagnóstico (Solo mide longitud y puntas para auditoría)
    st.info(f"""🔍 **Rastreador de Conexión Institucional:**
* 🛰️ URL activa: `{url}`
* 📏 Longitud en Secrets: **{len(key)}** caracteres.
* 🛡️ Firma actual: `{key[:8]}...` | Final: `...{key[-8:]}`""")
    
    return create_client(url, key)

def ejecutar():
    st.markdown("""
        <style>
        .titulo-genesis { color: #0d1b2a; font-family: 'Arial Black'; font-size: 32px; }
        .subtitulo-genesis { color: #d4af37; font-weight: bold; font-size: 13px; text-transform: uppercase; }
        .hud-container { display: flex; gap: 15px; margin-bottom: 25px; margin-top: 15px; }
        .hud-card {
            flex: 1; background: #ffffff; border-top: 3px solid #0d1b2a;
            border-radius: 4px 4px 12px 12px; padding: 12px 15px; text-align: center;
            box-shadow: 0 10px 25px rgba(13, 27, 42, 0.04);
        }
        .hud-value { font-size: 32px; font-family: 'Arial Black'; font-weight: 900; color: #0d1b2a; }
        .contenedor-matriz { background: #ffffff; border-radius: 12px; border: 1px solid #e5e5e5; border-top: 4px solid #0d1b2a; padding: 20px; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<p class='titulo-genesis'>👥 Gestión de Estudiantes</p>", unsafe_allow_html=True)
    st.markdown("<p class='subtitulo-genesis'>Consola Central de Control de Matrícula</p>", unsafe_allow_html=True)
    st.markdown("---")

    try:
        supabase = iniciar_conexion()
        estudiantes_base = []
        offset, chunk_size = 0, 1000
        
        with st.spinner("Sincronizando base de datos masiva..."):
            while True:
                resultado = supabase.table("data_estudiantes")\
                    .select('*')\
                    .range(offset, offset + chunk_size - 1).execute()
                if not resultado.data: break
                estudiantes_base.extend(resultado.data)
                if len(resultado.data) < chunk_size: break
                offset += chunk_size
    except Exception as e:
        st.error(f"🚨 Error de enlace masivo: {e}")
        return

    if estudiantes_base:
        df = pd.DataFrame(estudiantes_base)
        df.columns = [c.lower() for c in df.columns]
        
        col_id = "id_estudiante" if "id_estudiante" in df.columns else df.columns[0]
        df_unicos = df.drop_duplicates(subset=[col_id])
        total_matricula = len(df_unicos)
        
        col_grado = "grado" if "grado" in df.columns else df.columns[2]
        col_grupo = "grupo" if "grupo" in df.columns else df.columns[3]
        
        total_grados = df_unicos[col_grado].nunique() if col_grado in df_unicos.columns else 0
        total_grupos = df_unicos[col_grupo].nunique() if col_grupo in df_unicos.columns else 0

        st.markdown(f"""
            <div class="hud-container">
                <div class="hud-card">
                    <div style="font-size:11px; font-weight:800; color:#5c677d;">👥 MATRÍCULA TOTAL</div>
                    <div class="hud-value">{total_matricula}</div>
                </div>
                <div class="hud-card" style="border-top-color: #d4af37;">
                    <div style="font-size:11px; font-weight:800; color:#bfa12a;">🏫 GRADOS ACTIVOS</div>
                    <div class="hud-value" style="color: #d4af37;">{total_grados}</div>
                </div>
                <div class="hud-card" style="border-top-color: #2b9348;">
                    <div style="font-size:11px; font-weight:800; color:#2b9348;">🛡️ GRUPOS OPERATIVOS</div>
                    <div class="hud-value" style="color: #2b9348;">{total_grupos}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="contenedor-matriz">', unsafe_allow_html=True)
        st.markdown("<h4 style='color: #0d1b2a; font-weight: bold; margin-top: 0px; margin-bottom: 15px;'>MATRIZ OFICIAL DE ESTUDIANTES MATRICULADOS</h4>", unsafe_allow_html=True)
        
        mapeo_visual = {}
        for c in df.columns:
            if "id" in c: mapeo_visual[c] = "ID Estudiante"
            elif "nombre" in c: mapeo_visual[c] = "Nombre Completo"
            elif "grado" in c: mapeo_visual[c] = "Grado"
            elif "grupo" in c: mapeo_visual[c] = "Grupo"
            elif "correo" in c or "mail" in c: mapeo_visual[c] = "Correo Institucional"
            else: mapeo_visual[c] = c.replace("_", " ").title()

        df_visual = df_unicos.rename(columns=mapeo_visual)
        col_orden = "Nombre Completo" if "Nombre Completo" in df_visual.columns else df_visual.columns[1]
        df_ordenado = df_visual.sort_values(by=col_orden)
        
        st.dataframe(df_ordenado, use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)
