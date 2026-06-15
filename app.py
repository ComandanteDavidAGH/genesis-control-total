import streamlit as st

# ⚙️ REGLA DE ORO: La configuración de página DEBE SER siempre la primera orden
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

# 🧭 ENRUTADOR INTELIGENTE DEL BÚNKER (¡CABLES RECONECTADOS!)
if seleccion == "0. Gestión de Estudiantes":
    from modulos import m0_gestion
    m0_gestion.ejecutar()

elif seleccion == "1. Creador de Pruebas":
    from modulos import m1_creador
    m1_creador.ejecutar()

elif seleccion == "2. Digitar Notas":
    from modulos import m2_digitar
    m2_digitar.ejecutar()

elif seleccion == "3. Escáner OMR":  # 🌟 ¡EL CABLE CONECTADO AQUÍ!
    from modulos import m3_escaner
    m3_escaner.ejecutar()

elif seleccion == "4. Dashboard Analítico":
    from modulos import m4_dashboard
    m4_dashboard.ejecutar()
else:
    st.title(seleccion)
    st.info("Módulo en proceso de optimización óptica...")
