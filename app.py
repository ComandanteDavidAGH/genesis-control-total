import streamlit as st
import os

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
    base_dir = os.path.dirname(__file__)
    ruta_logo = os.path.join(base_dir, "assets", "logo.png")
    
    # 🛡️ ESCUDO ANTI-CORRUPCIÓN: Si la imagen falla internamente, pasamos al texto de respaldo
    mostrar_titulo_fallback = True
    
    if os.path.exists(ruta_logo):
        try:
            st.image(ruta_logo, use_container_width=True)
            mostrar_titulo_fallback = False  # Logrado. No duplicamos el título en texto
        except Exception:
            # Si el archivo está dañado en GitHub, la app lo ignora de forma segura y continúa
            pass
            
    if mostrar_titulo_fallback:
        st.title("🛡️ Panel de Mando")
    else:
        st.markdown("<h2 style='color: white; margin-top: -10px; margin-bottom: 15px;'>🛡️ Panel de Mando</h2>", unsafe_allow_html=True)
        
    seleccion = st.radio("SELECCIONE EL MÓDULO:", [
        "0. Gestión de Estudiantes",
        "1. Portal de Evaluación Estudiantil",
        "2. Creador de Pruebas",
        "3. Digitar Notas",
        "4. Escáner OMR",
        "5. Dashboard Analítico"
    ])

# 🧭 ENRUTADOR INTELIGENTE DEL BÚNKER (¡CONEXIONES INTACTAS!)
if seleccion == "0. Gestión de Estudiantes":
    from modulos import m0_gestion
    m0_gestion.ejecutar()

elif seleccion == "1. Portal de Evaluación Estudiantil":  
    from modulos import m5_estudiante
    m5_estudiante.ejecutar()

elif seleccion == "2. Creador de Pruebas":
    from modulos import m1_creador
    m1_creador.ejecutar()

elif seleccion == "3. Digitar Notas":
    from modulos import m2_digitar
    m2_digitar.ejecutar()

elif seleccion == "4. Escáner OMR":  
    from modulos import m3_escaner
    m3_escaner.ejecutar()

elif seleccion == "5. Dashboard Analítico":
    from modulos import m4_dashboard
    m4_dashboard.ejecutar()
