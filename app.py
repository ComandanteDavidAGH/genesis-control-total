import streamlit as st
import os

# ⚙️ REGLA DE ORO: La configuración de página DEBE SER siempre la primera orden
st.set_page_config(page_title="GÉNESIS v4.0", layout="wide", page_icon="🛡️")

# =================================================================
# 🧠 MEMORIA DE SEGURIDAD (Inicialización del Estado de Autenticación)
# =================================================================
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

# =================================================================
# 🔒 CREDENCIALES DE ACCESO AUTORIZADO
# =================================================================
USUARIO_MAESTRO = "admin"  # Puedes cambiar este usuario por el que desees
CLAVE_MAESTRA = st.secrets["ADMIN_PIN"] if "ADMIN_PIN" in st.secrets else "GENESIS2026"

# Definición de la ruta absoluta del Emblema Oficial
base_dir = os.path.dirname(__file__)
ruta_logo = os.path.join(base_dir, "assets", "logo.png")

# 🎨 INYECCIÓN VISUAL QUIRÚRGICA PARA LA BARRA LATERAL (Solo si está autenticado)
st.markdown("""
    <style>
    /* Fondo oscuro militar para la barra lateral */
    [data-testid="stSidebar"] { 
        background-color: #0d1b2a; 
    }
    
    /* Texto blanco estricto para la barra lateral */
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3, 
    [data-testid="stSidebar"] label { 
        color: #ffffff !important; 
    }
    
    /* 👁️ CONTROL ÓPTICO: Forzar que el botón del ojo de la contraseña sea visible y oscuro */
    [data-testid="stSidebar"] input {
        color: #0d1b2a !important;
        background-color: #ffffff !important;
        font-weight: bold !important;
    }
    [data-testid="stSidebar"] button svg {
        fill: #0d1b2a !important;
        color: #0d1b2a !important;
    }

    /* ========================================================= */
    /* 🚀 NUEVOS AJUSTES TÁCTICOS 🚀 */
    /* ========================================================= */

    /* 🚫 1. ERRADICACIÓN TOTAL DEL GATO, ESTRELLA Y COMPARTIR */
    /* Oculta el botón principal de 'Deploy' si lo hay */
    .stAppDeployButton {
        display: none !important;
    }
    
    /* Oculta todos los enlaces (Share, GitHub) de la barra superior */
    [data-testid="stHeaderActionElements"] a {
        display: none !important;
    }
    
    /* Oculta todos los botones (Estrella, Lápiz) EXCEPTO la Hamburguesa (tres puntos) */
    [data-testid="stHeaderActionElements"] button:not([aria-label="Main menu"]) {
        display: none !important;
    }

    /* 🛑 2. ESTILO TÁCTICO PARA EL BOTÓN DE CERRAR SESIÓN (BOTÓN DE EYECCIÓN) */
    [data-testid="stSidebar"] .stButton > button {
        background-color: #ef4444 !important; /* Color Rojo Alerta */
        border: 2px solid #b91c1c !important;
        border-radius: 8px !important;
    }
    [data-testid="stSidebar"] .stButton > button p {
        color: #ffffff !important; /* Texto blanco brillante */
        font-weight: bold !important;
    }
    [data-testid="stSidebar"] .stButton > button:hover {
        background-color: #dc2626 !important; /* Rojo más oscuro al pasar el cursor */
    }
    </style>
""", unsafe_allow_html=True)

# =================================================================
# 🏛️ FASE 1: PANTALLA DE INICIO DE SESIÓN (LOGIN CENTRAL)
# =================================================================
if not st.session_state.autenticado:
    # Ocultamos la barra lateral usando CSS mientras no esté autenticado
    st.markdown("<style>[data-testid='stSidebar'] {display: none;}</style>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Contenedor centrado asimétrico para el formulario de Login
    col1, col2, col3 = st.columns([1.1, 1.2, 1.1])
    
    with col2:
        # Despliegue del Escudo B en el centro del Login
        if os.path.exists(ruta_logo):
            st.image(ruta_logo, use_container_width=True)
            
        st.markdown("<h2 style='text-align: center; color: #0d1b2a; margin-top: 10px; font-weight: bold;'>GÉNESIS CONTROL TOTAL</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #555; font-size: 1rem; margin-top: -10px;'>AUTENTICACIÓN DE MANDO INSTITUTIONAL</p>", unsafe_allow_html=True)
        
        # Cuadro de credenciales tácticas
        with st.form("formulario_login"):
            usuario_ingresado = st.text_input("👤 USUARIO DE MANDO:", placeholder="Ingrese su usuario")
            clave_ingresada = st.text_input("🔑 CONTRASEÑA DE ACCESO:", type="password", placeholder="Ingrese su contraseña")
            
            # Botón de ejecución
            boton_acceso = st.form_submit_button("🔓 INITIALIZAR MÓDULOS")
            
            if boton_acceso:
                if usuario_ingresado == USUARIO_MAESTRO and clave_ingresada == CLAVE_MAESTRA:
                    st.session_state.autenticado = True
                    st.success("✅ ACCESO CONCEDIDO. Cargando sistemas...")
                    st.rerun() # Reinicia la app para aplicar el desbloqueo
                else:
                    st.error("❌ CREDENCIALES RECHAZADAS: Verifique usuario o contraseña.")

# =================================================================
# 🏛️ FASE 2: ENTORNO DE OPERACIONES DESTRABADO (USUARIO LOGUEADO)
# =================================================================
else:
    # Menú Lateral Institucional (Se activa solo al pasar el Login)
    with st.sidebar:
        if os.path.exists(ruta_logo):
            try:
                st.image(ruta_logo, use_container_width=True)
            except Exception:
                pass
                
        st.title("🛡️ Sistema GÉNESIS")
        st.markdown(f"<p style='color: #4ade80; font-weight: bold;'>👤 Operador: {USUARIO_MAESTRO.upper()}</p>", unsafe_allow_html=True)
        st.markdown("---")
        
        # Selector de Módulos Operacionales
        seleccion = st.radio("SELECCIONE EL MÓDULO:", [
            "0. Gestión de Estudiantes",
            "1. Portal de Evaluación Estudiantil",
            "2. Creador de Pruebas",
            "3. Digitar Notas",
            "4. Escáner OMR",
            "5. Dashboard Analítico"
        ], index=2) # Por defecto abre el creador de pruebas
        
        st.markdown("---")
        # Sistema de eyección segura (Cerrar Sesión)
        if st.button("🔒 CERRAR SESIÓN"):
            st.session_state.autenticado = False
            st.rerun()

    # =================================================================
    # 🧭 ENRUTADOR INTELIGENTE DEL BÚNKER (Doble pared de verificación)
    # =================================================================
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
