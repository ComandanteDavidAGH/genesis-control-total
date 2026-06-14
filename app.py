import streamlit as st

# Configuración de página de alta definición
st.set_page_config(page_title="GÉNESIS v2.5", layout="wide", page_icon="⚙️")

# Inyección de Estilo para el Menú Lateral
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #0d1b2a; }
    [data-testid="stSidebar"] * { color: #ffffff; }
    </style>
""", unsafe_allow_html=True)

# Menú Lateral Institucional
with st.sidebar:
    st.image("https://raw.githubusercontent.com/ComandanteDavidAGH/genesis-control-total/main/logo_genesis.png", width=200) # Opcional: sube tu logo después
    st.title("🛡️ Panel de Mando")
    seleccion = st.radio("SELECCIONE EL MÓDULO:", [
        "0. Gestión de Estudiantes",
        "1. Creador de Pruebas",
        "2. Digitar Notas",
        "3. Escáner OMR",
        "4. Dashboard Analítico"
    ])

# Enrutador de Módulos
if seleccion == "1. Creador de Pruebas":
    from modulos import m1_creador
    m1_creador.ejecutar()
else:
    st.title(seleccion)
    st.info("Módulo en proceso de carga táctica...")
