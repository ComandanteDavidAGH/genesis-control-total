import streamlit as st
from supabase import create_client

def iniciar_conexion():
    url = st.secrets["SUPABASE_URL"].strip()
    key = st.secrets["SUPABASE_KEY"].strip()
    return create_client(url, key)

def ejecutar():
    st.markdown("""
        <style>
        .titulo-genesis { color: #0d1b2a; font-family: 'Arial Black'; font-size: 32px; }
        .subtitulo-genesis { color: #d4af37; font-weight: bold; font-size: 14px; text-transform: uppercase; }
        
        /* Contornos Dorados de Precisión */
        div[data-baseweb="input"], div[data-baseweb="select"] {
            border: 2px solid #d4af37 !important; border-radius: 8px !important;
            background-color: #ffffff !important;
        }
        .casilla-telemetria {
            background: #fff; border-radius: 12px; padding: 15px; text-align: center;
            box-shadow: 0 4px 10px rgba(0,0,0,0.04); border: 2px solid #0d1b2a;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<p class='titulo-genesis'>⚙️ Creador de Plantillas Maestras</p>", unsafe_allow_html=True)
    st.markdown("<p class='subtitulo-genesis'>Configuración Óptica Avanzada v2.5</p>", unsafe_allow_html=True)
    st.markdown("---")

    # 🏢 Formulario Seguro en Cuadrícula Estricta 2x3 (6 cajas doradas)
    st.markdown("<h4 style='color: #0d1b2a; font-weight: bold; margin-bottom: 10px;'>📝 Datos Generales del Examen</h4>", unsafe_allow_html=True)
    with st.container(border=True):
        # Fila 1
        f1c1, f1c2, f1c3 = st.columns(3)
        with f1c1: st.text_input("🎯 Nombre de la Evaluación:", placeholder="Ej: Primer Bimestral")
        with f1c2: st.selectbox("📚 Asignatura / Materia:", ["Matemáticas", "Lenguaje", "Ciencias Naturales", "Sociales", "Inglés"])
        with f1c3: st.selectbox("📋 Tipo de Evaluación:", ["Quiz", "Evaluación Primer Periodo", "Evaluación Segundo Periodo", "Prepruebas Saber Pro"])
        
        # Fila 2
        f2c1, f2c2, f2c3 = st.columns(3)
        with f2c1: st.selectbox("🏫 Grado / Curso Destino:", ["1°", "2°", "3°", "4°", "5°", "6°", "7°", "8°", "9°", "10°", "11°"])
        with f2c2: total_preguntas = st.number_input("🔢 Número de Preguntas:", 1, 100, 10)
        with f2c3: puntaje_maximo = st.number_input("🎖️ Nota Máxima Posible:", 1.0, 100.0, 5.0)

    # Telemetría matemática
    peso_por_pregunta = puntaje_maximo / total_preguntas if total_preguntas > 0 else 0

    # 📊 Cuadros de Mando del Resumen Inferior
    st.markdown("<br><h3 style='color: #0d1b2a; font-weight: bold;'>📊 Resumen de Configuración</h3>", unsafe_allow_html=True)
    col_card1, col_card2, col_card3 = st.columns(3)
    with col_card1:
        st.markdown(f'<div class="casilla-telemetria"><b>🔢 TOTAL PREGUNTAS</b><br><span style="font-size:28px; font-weight:900;">{total_preguntas}</span></div>', unsafe_allow_html=True)
    with col_card2:
        st.markdown(f'<div class="casilla-telemetria" style="border-color:#d4af37; color:#bfa12a;"><b>🎯 VALOR POR ACERTO</b><br><span style="font-size:28px; font-weight:900; color:#d4af37;">{peso_por_pregunta:.2f}</span></div>', unsafe_allow_html=True)
    with col_card3:
        st.markdown(f'<div class="casilla-telemetria" style="border-color:#2b9348; color:#2b9348;"><b>🎖️ NOTA MÁXIMA</b><br><span style="font-size:28px; font-weight:900; color:#2b9348;">{puntaje_maximo:.1f}</span></div>', unsafe_allow_html=True)
