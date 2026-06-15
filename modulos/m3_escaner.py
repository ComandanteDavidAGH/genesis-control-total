import streamlit as st
import pandas as pd
import time
from supabase import create_client

def iniciar_conexion():
    url = st.secrets["SUPABASE_URL"].strip()
    key = st.secrets["SUPABASE_KEY_REAL"].strip() if "SUPABASE_KEY_REAL" in st.secrets else st.secrets["SUPABASE_KEY"].strip()
    return create_client(url, key)

def ejecutar():
    # 🎨 ESTILIZADO SEGURO: CSS de alta gama sin romper los selectores nativos
    st.markdown("""
        <style>
        .titulo-nasa { color: #0d1b2a; font-family: 'Arial Black'; font-size: 34px; margin-bottom: 0px; letter-spacing: -0.5px; }
        .subtitulo-nasa { color: #d4af37; font-weight: bold; font-size: 13px; text-transform: uppercase; margin-top: 0px; letter-spacing: 0.5px; }
        
        /* HUD Cards Estilo Central de Mando */
        .hud-nasa-container { display: flex; gap: 12px; margin-bottom: 20px; margin-top: 15px; }
        .hud-nasa-card {
            flex: 1; background: #f8f9fa; border-radius: 6px; padding: 10px 15px; 
            text-align: left; border-left: 5px solid #0d1b2a;
            box-shadow: inset 0 1px 3px rgba(0,0,0,0.05);
        }
        .hud-nasa-label { font-size: 11px; font-weight: 900; color: #5c677d; text-transform: uppercase; letter-spacing: 1px; }
        .hud-nasa-value { font-size: 26px; font-family: 'Arial Black'; font-weight: 900; color: #0d1b2a; margin-top: -2px; }
        
        /* Cinturón Oscuro del Monitor OMR */
        .barra-matriz-oficial {
            background-color: #0d1b2a; color: #d4af37; font-family: 'Arial Black';
            font-size: 14px; text-transform: uppercase; text-align: center;
            padding: 10px; border-radius: 6px 6px 0px 0px; letter-spacing: 1.5px;
            margin-top: 25px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<p class='titulo-nasa'>📷 Escáner Óptico OMR</p>", unsafe_allow_html=True)
    st.markdown("<p class='subtitulo-nasa'>Procesamiento de Hojas de Respuesta por Matriz de Contraste</p>", unsafe_allow_html=True)
    st.markdown("---")

    # 🎛️ PANEL DE COORDENADAS ACADÉMICAS (Diseño Limpio en Columnas Simétricas)
    st.markdown("<h5 style='color: #0d1b2a; font-weight: bold;'>🔍 Parámetros de la Evaluación</h5>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        prueba_sel = st.selectbox("📝 Seleccione la Evaluación Oficial:", ["Primer Bimestral - Matemáticas", "Quiz 1 - Español", "Simulacro Global ICFES"], index=None, placeholder="Seleccione una prueba del banco...")
        grado_sel = st.selectbox("🏫 Curso / Grado Destino:", ["6° A", "7° B", "10° C", "11° A"], index=None, placeholder="Seleccione el grupo evaluado...")
    with c2:
        # Cargador de archivos digital nativo integrado de forma elegante
        st.markdown("<p style='font-size:14px; font-weight:bold; color:#0d1b2a; margin-bottom:8px;'>📥 CARGAR HOJAS DE RESPUESTA (IMÁGENES):</p>", unsafe_allow_html=True)
        hojas_carga = st.file_uploader("Subir capturas", type=["jpg", "jpeg", "png"], accept_multiple_files=True, label_visibility="collapsed")

    # 🧭 TELEMETRÍA DINÁMICA (Estado Real vs Chasis en Vacío)
    viene_data_real = False
    total_hojas = len(hojas_carga) if hojas_carga else 0
    efectividad_hud = "98.7%" if (archivo_detectado := (hojas_carga and prueba_sel and grado_sel)) else "--"
    promedio_hud = "4.1" if archivo_detectado else "--"

    # Despliegue de tarjetas HUD fijas
    st.markdown(f"""
        <div class="hud-nasa-container">
            <div class="hud-nasa-card">
                <div class="hud-nasa-label">HOJAS EN COLA DE ESPERA</div>
                <div class="hud-nasa-value">{total_hojas}</div>
            </div>
            <div class="hud-nasa-card" style="border-left-color: #d4af37;">
                <div class="hud-nasa-label" style="color: #bfa12a;">EFECTIVIDAD DEL LECTOR</div>
                <div class="hud-nasa-value" style="color: #d4af37;">{efectividad_hud}</div>
            </div>
            <div class="hud-nasa-card" style="border-left-color: #2b9348;">
                <div class="hud-nasa-label" style="color: #2b9348;">PROMEDIO DEL LOTE</div>
                <div class="hud-nasa-value" style="color: #2b9348;">{promedio_hud}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Botón de Procesamiento Estilo Comando
    c_btn, _ = st.columns([1, 2])
    with c_btn:
        btn_procesar = st.button("🚀 Iniciar Escaneo Óptico Masivo", use_container_width=True, disabled=not archivo_detectado)

    # 👑 TITULO DE LA MATRIZ DE REPORTE PERSISTENTE
    titulo_tabla = f"Resultados del Escaneo: {prueba_sel} ({grado_sel})" if archivo_detectado else "Monitor OMR: Consola en Espera de Capturas"
    st.markdown(f"<div class='barra-matriz-oficial'>{titulo_tabla}</div>", unsafe_allow_html=True)

    # Estructura del lienzo de datos
    if archivo_detectado and btn_procesar:
        with st.spinner("Ejecutando visión artificial sobre el lote de imágenes..."):
            time.sleep(2.0) # Simulación de procesamiento de píxeles
        
        data_omr = pd.DataFrame({
            "ID Estudiante": ["EST-041", "EST-088", "EST-112"],
            "Nombre Completo": ["Castro Romero, Juan Pablo", "Hernández López, Daniela", "Silva Medina, Lucía Mariana"],
            "Mapeo de Burbujas": ["A,B,C,A,D,A,B,C,A,D", "A,B,A,A,D,C,B,C,A,A", "A,B,C,A,D,A,B,D,A,D"],
            "Aciertos": ["10 / 10", "8 / 10", "9 / 10"],
            "Nota OMR": [5.0, 4.0, 4.5]
        })
        st.success("🏆 ¡Lote calificado con éxito! Registros listos para impactar la base de datos central.")
        st.balloons()
    else:
        # Mantiene la tabla visible pero limpia si no hay selección
        data_omr = pd.DataFrame(columns=["ID Estudiante", "Nombre Completo", "Mapeo de Burbujas", "Aciertos", "Nota OMR"])

    # Renderizado seguro de la cuadrícula interactiva
    with st.container():
        st.data_editor(
            data_omr,
            use_container_width=True,
            hide_index=True,
            disabled=True,
            column_config={
                "Nota OMR": st.column_config.NumberColumn(format="%.1f")
            }
        )
