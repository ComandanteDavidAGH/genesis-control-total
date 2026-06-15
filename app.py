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

# =================================================================
# 🔒 CONFIGURACIÓN DE SEGURIDAD (LA LLAVE MAESTRA INSTITUCONAL)
# =================================================================
# Por defecto la clave es GENESIS2026. Puedes cambiarla aquí directamente entre las comillas.
CLAVE_MAESTRA = st.secrets["ADMIN_PIN"] if "ADMIN_PIN" in st.secrets else "GENESIS2026"

# Menú Lateral Institucional con Control de Acceso Perimetral
with st.sidebar:
    base_dir = os.path.dirname(__file__)
    ruta_logo = os.path.join(base_dir, "assets", "logo.png")
    
    # Escudo anti-corrupción del logo
    if os.path.exists(ruta_logo):
        try:
            st.image(ruta_logo, use_container_width=True)
        except Exception:
            pass
            
    st.title("🛡️ Sistema GÉNESIS")
    st.markdown("---")
    
    # 🚨 FILTRO CIBERNÉTICO: Casilla de contraseña enmascarada
    pin_ingresado = st.text_input("🔑 LLAVE DE MANDO (DOCENTE):", type="password", help="Ingrese la contraseña para liberar las herramientas administrativas.")
    st.markdown("---")
    
    # Evaluación del cortafuegos en tiempo real
    if pin_ingresado == CLAVE_MAESTRA:
        st.success("🔓 MANDO DESBLOQUEADO")
        seleccion = st.sidebar.radio("SELECCIONE EL MÓDULO:", [
            "0. Gestión de Estudiantes",
            "1. Portal de Evaluación Estudiantil",
            "2. Creador de Pruebas",
            "3. Digitar Notas",
            "4. Escáner OMR",
            "5. Dashboard Analítico"
        ], index=1) # Enfocado por defecto en el portal para comodidad
    else:
        if pin_ingresado:
            st.error("❌ LLAVE INCORRECTA")
        st.info("📱 MODO ESTUDIANTE ACTIVO")
        # Forzado militar: Si no hay clave correcta, el usuario es un alumno y solo ve el portal
        seleccion = "1. Portal de Evaluación Estudiantil"

# 🧭 ENRUTADOR INTELIGENTE DEL BÚNKER (Cables blindados con doble pared de verificación)
if seleccion == "0. Gestión de Estudiantes" and pin_ingresado == CLAVE_MAESTRA:
    from modulos import m0_gestion
    m0_gestion.ejecutar()

elif seleccion == "1. Portal de Evaluación Estudiantil":  
    from modulos import m5_estudiante
    m5_estudiante.ejecutar()

elif seleccion == "2. Creador de Pruebas" and pin_ingresado == CLAVE_MAESTRA:
    from modulos import m1_creador
    m1_creador.ejecutar()

elif seleccion == "3. Digitar Notas" and pin_ingresado == CLAVE_MAESTRA:
    from modulos import m2_digitar
    m2_digitar.ejecutar()

elif seleccion == "4. Escáner OMR" and pin_ingresado == CLAVE_MAESTRA:
    from modulos import m3_escaner
    m3_escaner.ejecutar()

elif seleccion == "5. Dashboard Analítico" and pin_ingresado == CLAVE_MAESTRA:
    from modulos import m4_dashboard
    m4_dashboard.ejecutar()

elif pin_ingresado != CLAVE_MAESTRA and seleccion != "1. Portal de Evaluación Estudiantil":
    # Paracaídas de eyección por si intentan violar el enrutamiento inyectando variables en la URL
    st.warning("🚨 Intento de violación de perímetro detectado. Retornando a zona segura...")
    from modulos import m5_estudiante
    m5_estudiante.ejecutar()
