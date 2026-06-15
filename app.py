import streamlit as st
# 🛰️ TRAMPA DE TELEMETRÍA DE ARCHIVOS (TEMPORAL)
import os
with st.sidebar.expander("🕵️‍♂️ Radar de Conexión de Módulos", expanded=True):
    st.write(f"**Selección actual:** `{seleccion if 'seleccion' in locals() else 'No asignada'}`")
    if os.path.exists("modulos"):
        archivos = os.listdir("modulos")
        st.write("**Archivos reales en la carpeta 'modulos':**")
        for arc in archivos:
            st.code(f"📁 {arc}")
    else:
        st.error("🚨 La carpeta 'modulos' no existe en la raíz.")
# ────────────────────────────────────────────────────────

# Configuración de página de alta definición
st.set_page_config(page_title="GÉNESIS v2.5", layout="wide", page_icon="⚙️")

# Inyección de Estilo para el Menú Lateral Militar Oscuro
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #0d1b2a; }
    [data-testid="stSidebar"] * { color: #ffffff; }
    </style>
""", unsafe_allow_html=True)

# Menú Lateral Institucional
with st.sidebar:
    st.title("🛡️ Panel de Mando")
    seleccion = st.radio("SELECCIONE EL MÓDULO:", [
        "0. Gestión de Estudiantes",
        "1. Creador de Pruebas",
        "2. Digitar Notas",
        "3. Escáner OMR",
        "4. Dashboard Analítico"
    ])

# Enrutador Inteligente del Búnker
if seleccion == "0. Gestión de Estudiantes":
    from modulos import m0_gestion
    m0_gestion.ejecutar()
elif seleccion == "1. Creador de Pruebas":
    from modulos import m1_creador
    m1_creador.ejecutar()
elif seleccion == "4. Dashboard Analítico":
    from modulos import m4_dashboard
    m4_dashboard.ejecutar()
else:
    st.title(seleccion)
    st.info("Módulo en proceso de optimización óptica...")
