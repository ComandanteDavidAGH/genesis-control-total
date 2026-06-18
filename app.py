import streamlit as st
import os

# ⚙️ REGLA DE ORO: La configuración de página DEBE SER siempre la primera orden
st.set_page_config(page_title="GÉNESIS v4.0", layout="wide", page_icon="🛡️")

# 🎨 INYECCIÓN VISUAL QUIRÚRGICA PARA LA BARRA LATERAL
st.markdown("""
    <style>
    /* Fondo oscuro militar para la barra lateral */
    [data-testid="stSidebar"] { 
        background-color: #0d1b2a; 
    }
    
    /* Texto blanco estricto solo para títulos, etiquetas y marcas de texto */
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3, 
    [data-testid="stSidebar"] label { 
        color: #ffffff !important; 
    }
    
    # 🎯 FIX DE VISIBILIDAD: Forzar letras negras y legibles dentro de la casilla de texto
    [data-testid="stSidebar"] input {
        color: #0d1b2a !important;
        background-color: #ffffff !important;
        font-weight: bold !important;
    }
    
    /* 👁️ CONTROL ÓPTICO: Forzar que el botón del ojo de la contraseña sea visible y oscuro */
    [data-testid="stSidebar"] button svg {
        fill: #0d1b2a !important;
        color: #0d1b2a !important;
    }
    </style>
""", unsafe_allow_html=True)

# =================================================================
# 🔒 CONFIGURACIÓN DE SEGURIDAD (LA LLAVE MAESTRA INSTITUCIONAL)
# =================================================================
CLAVE_MAESTRA = st.secrets["ADMIN_PIN"] if "ADMIN_PIN" in st.secrets else "GENESIS2026"

# Definición de la ruta absoluta del Emblema Oficial
base_dir = os.path.dirname(__file__)
ruta_logo = os.path.join(base_dir, "assets", "logo.png")

# =================================================================
# 🛡️ DESPLIEGUE EN EL MENÚ LATERAL (SIDEBAR)
# =================================================================
with st.sidebar:
    # 1. Cargamos el escudo en la parte superior del menú lateral
    if os.path.exists(ruta_logo):
        try:
            st.image(ruta_logo, use_container_width=True)
        except Exception:
            pass
            
    st.title("🛡️ Sistema GÉNESIS")
    st.markdown("---")
    
    # Casilla de contraseña enmascarada
    pin_ingresado = st.text_input("🔑 LLAVE DE MANDO (DOCENTE):", type="password", help="Ingrese la contraseña para liberar las herramientas administrativas.")
    st.markdown("---")
    
    if pin_ingresado == CLAVE_MAESTRA:
        st.success("🔓 MANDO DESBLOQUEADO")
        seleccion = st.sidebar.radio("SELECCIONE EL MÓDULO:", [
            "0. Gestión de Estudiantes",
            "1. Portal de Evaluación Estudiantil",
            "2. Creador de Pruebas",
            "3. Digitar Notas",
            "4. Escáner OMR",
            "5. Dashboard Analítico"
        ], index=1)
    else:
        if pin_ingresado:
            st.error("❌ LLAVE INCORRECTA")
        st.info("📱 MODO ESTUDIANTE ACTIVO")
        seleccion = "1. Portal de Evaluación Estudiantil"

# =================================================================
# 🏛️ PANTALLA DE INICIO (BIENVENIDA / LOGIN PRINCIPAL)
# =================================================================
# Si el usuario no ha ingresado la clave, mostramos el escudo gigante en el centro
if pin_ingresado != CLAVE_MAESTRA:
    st.markdown("<br><br>", unsafe_allow_html=True) # Espaciado superior
    col1, col2, col3 = st.columns([1, 1.5, 1]) 
    with col2:
        if os.path.exists(ruta_logo):
            st.image(ruta_logo, use_container_width=True)
    
    st.markdown("<h2 style='text-align: center; color: #0d1b2a; margin-top: 15px;'>SISTEMA GÉNESIS CONTROL TOTAL</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.1rem; color: #555;'>Ingrese la <b>Llave de Mando</b> en el menú lateral para inicializar los módulos tácticos.</p>", unsafe_allow_html=True)
    st.markdown("---")

# =================================================================
# 🧭 ENRUTADOR INTELIGENTE DEL BÚNKER (Doble pared de verificación)
# =================================================================
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
