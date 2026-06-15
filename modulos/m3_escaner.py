import streamlit as st
import pandas as pd
import time
from supabase import create_client

def iniciar_conexion():
    url = st.secrets["SUPABASE_URL"].strip()
    key = st.secrets["SUPABASE_KEY_REAL"].strip() if "SUPABASE_KEY_REAL" in st.secrets else st.secrets["SUPABASE_KEY"].strip()
    return create_client(url, key)

def ejecutar():
    # 🎨 INGENIERÍA ÓPTICA AVANZADA: CSS de Alta Densidad Visual
    st.markdown("""
        <style>
        .titulo-nasa { color: #0d1b2a; font-family: 'Arial Black'; font-size: 34px; margin-bottom: 0px; letter-spacing: -0.5px; }
        .subtitulo-nasa { color: #d4af37; font-weight: bold; font-size: 13px; text-transform: uppercase; margin-top: 0px; }
        
        /* Selectores de Parámetros con Borde Dorado */
        div[data-testid="stSelectbox"] > div [role="combobox"] {
            border: 2px solid #d4af37 !important;
            border-radius: 6px !important;
            background-color: #ffffff !important;
            color: #0d1b2a !important;
            font-weight: bold !important;
        }
        div[data-testid="stSelectbox"] label p {
            color: #0d1b2a !important; font-weight: 800 !important; font-size: 13px !important; text-transform: uppercase;
        }
        
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
    st.markdown("<p class='subtitulo-genesis'>Procesamiento de Hojas de Respuesta por Matriz de Contraste</p>", unsafe_allow_html=True)
    st.markdown("---")

    # 🎛️ COORDENADAS ACADÉMICAS INICIALES (Chasis Persistente)
    st.markdown("<h5 style='color: #0d1b2a; font-weight: bold;'>🔍 Parámetros de la Evaluación</h5>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        prueba_sel = st.selectbox("📝 Seleccione la Evaluación:", ["Primer Bimestral - Matemáticas", "Quiz 1 - Español", "Simulacro Global ICFES"], index=None, placeholder="Seleccione Prueba...")
    with c2:
        grado_sel = st.selectbox("🏫 Curso Destino:", ["6° A", "7° B", "10° C", "11° A"], index=None, placeholder="Seleccione Curso...")
    with c3:
        hojas_carga = st.file_uploader("📥 Cargar Hojas de Respuesta:", type=["jpg", "jpeg", "png"], accept_multiple_files=True, label_visibility="collapsed")

    # Controles de estado dinámicos
    archivo_detectado = True if (hojas_carga and prueba_sel and grado_sel) else False
    total_hojas = len(hojas_carga) if hojas_carga else 0
    efectividad_omr = "98.7%" if archivo_detectado else "--"
    promedio_omr = "3.8" if archivo_detectado else "--"

    # 📊 MONITOR DE TELEMETRÍA EN TIEMPO REAL
    st.markdown(f"""
        <div class="hud-nasa-container">
            <div class="hud-nasa-card">
                <div class="hud-nasa-label">HOJAS EN COLA</div>
                <div class="hud-nasa-value">{total_hojas}</div>
            </div>
            <div class="hud-nasa-card" style="border-left-color: #d4af37;">
                <div class="hud-nasa-label" style="color: #bfa12a;">EFECTIVIDAD DE LECTURA</div>
                <div class="hud-nasa-value" style="color: #d4af37;">{efectividad_omr}</div>
            </div>
            <div class="hud-nasa-card" style="border-left-color: #2b9348;">
                <div class="hud-nasa-label" style="color: #2b9348;">PROMEDIO DE PROCESAMIENTO</div>
                <div class="hud-nasa-value" style="color: #2b9348;">{promedio_omr}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 🎮 CONSOLA DE ACCIONES OPERATIVAS
    c_btn, _ = st.columns([1, 2])
    with c_btn:
        btn_procesar = st.button("🚀 Iniciar Escaneo Óptico Masivo", use_container_width=True, disabled=not archivo_detectado)

    # 👑 TITULO DE LA MATRIZ DE REPORTE
    titulo_tabla = f"Resultados del Escaneo: {prueba_sel} ({grado_sel})" if archivo_detectado else "Monitor OMR: Consola en Espera de Capturas"
    st.markdown(f"<div class='barra-matriz-oficial'>{titulo_matriz if 'titulo_matriz' in locals() else titulo_tabla}</div>", unsafe_allow_html=True)

    # Base de datos simulada de telemetría para el chasis
    if archivo_detectado and btn_procesar:
        with st.spinner("Ejecutando algoritmos de segmentación de umbral y análisis de elipses..."):
            time.sleep(2.5) # Simulación del motor de visión artificial
        
        # Simulamos la lectura de marcas físicas del lote subido por el docente
        data_omr = pd.DataFrame({
            "ID Estudiante": ["EST-041", "EST-088", "EST-112"],
            "Nombre Completo": ["Castro Romero, Juan Pablo", "Hernández López, Daniela", "Silva Medina, Lucía Mariana"],
            "Respuestas Detectadas": ["A,B,C,A,D,A,B,C,A,D", "A,B,A,A,D,C,B,C,A,A", "A,B,C,A,D,A,B,D,A,D"],
            "Aciertos": ["10 / 10", "8 / 10", "9 / 10"],
            "Nota Calculada": [5.0, 4.0, 4.5]
        })
        st.success("🏆 ¡Procesamiento de imágenes completado! Registros listos para sincronizar.")
        st.balloons()
    else:
        # Chasis en vacío impecable
        data_omr = pd.DataFrame(columns=["ID Estudiante", "Nombre Completo", "Respuestas Detectadas", "Aciertos", "Nota Calculada"])

    # Renderizado seguro de la cuadrícula interactiva
    with st.container():
        st.data_editor(
            data_omr,
            use_container_width=True,
            hide_index=True,
            disabled=True,
            column_config={
                "Nota Calculada": st.column_config.NumberColumn(format="%.1f")
            }
        )
