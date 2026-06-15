import streamlit as st
import pandas as pd
from supabase import create_client

def iniciar_conexion():
    url = st.secrets["SUPABASE_URL"].strip()
    key = st.secrets["SUPABASE_KEY"].strip()
    
    # 🛰️ TELEMETRÍA DE SEGURIDAD EN VIVO
    # Las llaves reales de Supabase son tokens JWT larguísimos (más de 100 caracteres).
    # Si este indicador muestra un número bajo (como 15 o 20), descubrimos al culpable.
    st.system_log = f"Longitud: {len(key)}" 
    st.info(f"🔍 **Rastreador de Credenciales:**\n* URL enlazada: `{url}`\n* Longitud de la clave detectada: **{len(key)}** caracteres.\n* Inicio de la clave: `{key[:6]}...` | Final de la clave: `...{key[-6:]}`")
    
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
                    .select('ID_Estudiante, Nombre_Completo, Grado, Grupo, "Correo Institucional"')\
                    .order('ID_Estudiante')\
                    .range(offset, offset + chunk_size - 1).execute()
                if not resultado.data: break
                estudiantes_base.extend(resultado.data)
                if len(resultado.data) < chunk_size: break
                offset += chunk_size
                
    except Exception as e:
        st.error(f"🚨 Error de enlace masivo: {e}")
        st.warning("💡 **Sugerencia de reparación:** Si la longitud de la clave arriba no supera los 100 caracteres, estás usando la contraseña de tu cuenta o de la base de datos en lugar de la API KEY original.")
        return

    if estudiantes_base:
        df_unicos = pd.DataFrame(estudiantes_base).drop_duplicates(subset=["ID_Estudiante"])
        total_matricula = len(df_unicos)
        total_grados = df_unicos["Grado"].nunique() if "Grado" in df_unicos.columns else 0
        total_grupos = df_unicos["Grupo"].nunique() if "Grupo" in df_unicos.columns else 0

        st.markdown(f"""
            <div class="hud-container">
                <div class="hud-card"><div style="font-size:11px; font-weight:800; color:#5c677d;">👥 MATRÍCULA TOTAL</div><div class="hud-value">{total_matricula}</div></div>
                <div class="hud-card" style="border-top-color: #d4af37;"><div style="font-size:11px; font-weight:800; color:#bfa12a;">🏫 GRADOS ACTIVOS</div><div class="hud-value" style="color: #d4af37;">{total_grados}</div></div>
                <div class="hud-card" style="border-top-color: #2b9348;">
                    <div style="font-size:11px; font-weight:800; color:#2b9348;">🛡️ GRUPOS OPERATIVOS</div><div class="hud-value" style="color: #2b9348;">{total_grupos}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
