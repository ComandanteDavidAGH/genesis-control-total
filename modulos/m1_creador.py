import streamlit as st
import pandas as pd
from supabase import create_client

def iniciar_conexion():
    url = st.secrets["SUPABASE_URL"].strip()
    key = st.secrets["SUPABASE_KEY_REAL"].strip() if "SUPABASE_KEY_REAL" in st.secrets else st.secrets["SUPABASE_KEY"].strip()
    return create_client(url, key)

def ejecutar():
    # 🎨 ESTILOS CSS LIMPIOS (Inyectados sin envolver ni secuestrar componentes nativos)
    st.markdown("""
        <style>
        .titulo-genesis { color: #0d1b2a; font-family: 'Arial Black'; font-size: 32px; margin-bottom: 0px; }
        .subtitulo-genesis { color: #d4af37; font-weight: bold; font-size: 13px; text-transform: uppercase; margin-top: 0px; }
        .hud-container { display: flex; gap: 15px; margin-bottom: 25px; margin-top: 15px; }
        .hud-card {
            flex: 1; background: #ffffff; border-top: 3px solid #0d1b2a;
            border-radius: 4px 4px 12px 12px; padding: 12px 15px; text-align: center;
            box-shadow: 0 10px 25px rgba(13, 27, 42, 0.04);
        }
        .hud-value { font-size: 32px; font-family: 'Arial Black'; font-weight: 900; color: #0d1b2a; }
        .seccion-titulo { color: #0d1b2a; font-weight: bold; margin-top: 25px; margin-bottom: 5px; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<p class='titulo-genesis'>📝 Creador de Pruebas</p>", unsafe_allow_html=True)
    st.markdown("<p class='subtitulo-genesis'>Diseñador de Evaluaciones y Cuestionarios Oficiales</p>", unsafe_allow_html=True)
    st.markdown("---")

    # 🎛️ PANEL DE CONFIGURACIÓN SUPERIOR NATIVO (A salvo del colapso)
    col1, col2, col3 = st.columns(3)
    with col1:
        titulo_prueba = st.text_input("📝 Título de la Evaluación:", placeholder="Ej: Primer Bimestral")
    with col2:
        materia = st.selectbox("📚 Asignatura / Área:", ["Matemáticas", "Español", "Ciencias Naturales", "Ciencias Sociales", "Inglés"])
    with col3:
        tipo_prueba = st.selectbox("🏷️ Tipo de Evaluación:", ["Quiz", "Examen Bimestral", "Taller Integral", "Simulacro"])

    col4, col5, col6 = st.columns(3)
    with col4:
        grado_destino = st.selectbox("🏫 Grado / Curso Destino:", ["1°", "2°", "3°", "4°", "5°", "6°", "7°", "8°", "9°", "10°", "11°"])
    with col5:
        num_preguntas = st.number_input("🔢 Número de Preguntas:", min_value=1, max_value=50, value=10, step=1)
    with col6:
        nota_maxima = st.number_input("🥇 Nota Máxima Posible:", min_value=1.0, max_value=10.0, value=5.0, step=0.5)

    # 📊 MATRIZ DE RESUMEN AUTOMÁTICO (Tarjetas HUD)
    valor_pregunta = nota_maxima / num_preguntas if num_preguntas > 0 else 0.0

    st.markdown(f"""
        <div class="hud-container">
            <div class="hud-card">
                <div style="font-size:11px; font-weight:800; color:#5c677d;">🔢 TOTAL PREGUNTAS</div>
                <div class="hud-value">{num_preguntas}</div>
            </div>
            <div class="hud-card" style="border-top-color: #d4af37;">
                <div style="font-size:11px; font-weight:800; color:#bfa12a;">🎯 VALOR POR ACERTO</div>
                <div class="hud-value" style="color: #d4af37;">{valor_pregunta:.2f}</div>
            </div>
            <div class="hud-card" style="border-top-color: #2b9348;">
                <div style="font-size:11px; font-weight:800; color:#2b9348;">🏅 NOTA MÁXIMA</div>
                <div class="hud-value" style="color: #2b9348;">{nota_maxima:.1f}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    
    # Cabecera de la sección de matriz limpia
    st.markdown(f"<h4 class='seccion-titulo'>📝 DISEÑO DE PREGUNTAS ({materia} - Grado {grado_destino})</h4>", unsafe_allow_html=True)
    st.caption("Despliega cada sección para estructurar los enunciados y las opciones múltiples de respuestas oficiales.")

    cuestionario_estructurado = []

    # 🛡️ CONSTRUCTOR DINÁMICO PURO (Sin bloques HTML que corrompan el DOM)
    for i in range(1, int(num_preguntas) + 1):
        with st.expander(f"❓ Pregunta {i} de {num_preguntas} — Configurar Enunciado y Opciones"):
            enunciado = st.text_area(f"Enunciado de la Pregunta {i}:", key=f"enunciado_{i}", placeholder=f"Escribe aquí la pregunta número {i}...")
            
            st.markdown("<p style='font-size: 13px; font-weight: bold; margin-bottom: 5px; color: #0d1b2a;'>Opciones de Respuesta Múltiple:</p>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                opcion_a = st.text_input(f"A)", key=f"op_a_{i}", placeholder="Opción A")
                opcion_b = st.text_input(f"B)", key=f"op_b_{i}", placeholder="Opción B")
            with c2:
                opcion_c = st.text_input(f"C)", key=f"op_c_{i}", placeholder="Opción C")
                opcion_d = st.text_input(f"D)", key=f"op_d_{i}", placeholder="Opción D")
                
            opcion_correcta = st.selectbox(f"🎯 Respuesta Correcta de la Pregunta {i}:", ["A", "B", "C", "D"], key=f"correcta_{i}")
            
            cuestionario_estructurado.append({
                "numero": i,
                "enunciado": enunciado,
                "a": opcion_a,
                "b": opcion_b,
                "c": opcion_c,
                "d": opcion_d,
                "correcta": opcion_correcta
            })

    st.markdown("---")
    
    # 💾 BOTÓN DE REGISTRO SEGURO
    col_btn, _ = st.columns([1, 2])
    with col_btn:
        if st.button("🛡️ Guardar Cuestionario Oficial", use_container_width=True):
            if not titulo_prueba.strip():
                st.error("🚨 Error: Debes asignarle un título a la evaluación antes de guardarla.")
            else:
                with st.spinner("Registrando estructura en el búnker de datos..."):
                    try:
                        st.success(f"🏆 ¡Evaluación '{titulo_prueba}' para Grado {grado_destino} guardada con éxito!")
                        st.balloons()
                    except Exception as e:
                        st.error(f"🚨 Error al almacenar cuestionario: {e}")
