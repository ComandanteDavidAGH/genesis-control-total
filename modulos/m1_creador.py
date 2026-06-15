import streamlit as st
import pandas as pd
from supabase import create_client

def iniciar_conexion():
    url = st.secrets["SUPABASE_URL"].strip()
    key = st.secrets["SUPABASE_KEY_REAL"].strip() if "SUPABASE_KEY_REAL" in st.secrets else st.secrets["SUPABASE_KEY"].strip()
    return create_client(url, key)

def ejecutar():
    # 🎨 INTERFAZ PREMIUM COMPONENTES CASILLAS DORADAS
    st.markdown("""
        <style>
        .titulo-nasa { color: #0d1b2a; font-family: 'Arial Black'; font-size: 34px; margin-bottom: 0px; letter-spacing: -0.5px; }
        .subtitulo-nasa { color: #d4af37; font-weight: bold; font-size: 13px; text-transform: uppercase; margin-top: 0px; letter-spacing: 0.5px; }
        
        /* Selectores Superiores Estilo Creador de Pruebas con Borde Dorado */
        div[data-testid="stSelectbox"] > div [role="combobox"], div[data-testid="stNumberInput"] i, input {
            border: 2px solid #d4af37 !important;
            border-radius: 6px !important;
            color: #0d1b2a !important;
            font-weight: bold !important;
        }
        div[data-testid="stSelectbox"] label p, div[data-testid="stTextInput"] label p, div[data-testid="stNumberInput"] label p {
            color: #0d1b2a !important; font-weight: 800 !important; font-size: 13px !important; text-transform: uppercase;
        }
        
        /* HUD Cards de Alta Densidad */
        .hud-nasa-container { display: flex; gap: 12px; margin-bottom: 20px; margin-top: 15px; }
        .hud-nasa-card {
            flex: 1; background: #f8f9fa; border-radius: 6px; padding: 10px 15px; 
            text-align: left; border-left: 5px solid #0d1b2a;
            box-shadow: inset 0 1px 3px rgba(0,0,0,0.05);
        }
        .hud-nasa-label { font-size: 11px; font-weight: 900; color: #5c677d; text-transform: uppercase; letter-spacing: 1px; }
        .hud-nasa-value { font-size: 26px; font-family: 'Arial Black'; font-weight: 900; color: #0d1b2a; margin-top: -2px; }
        
        /* Cinturón Oscuro del Monitor */
        .barra-matriz-oficial {
            background-color: #0d1b2a; color: #d4af37; font-family: 'Arial Black';
            font-size: 14px; text-transform: uppercase; text-align: center;
            padding: 10px; border-radius: 6px 6px 0px 0px; letter-spacing: 1.5px;
            margin-top: 25px;
        }
        
        /* Botón de Guardado Estilo Comando Red */
        div.stButton > button {
            background-color: #f25c54 !important; color: white !important;
            font-family: 'Arial Black' !important; font-size: 13px !important;
            text-transform: uppercase !important; border-radius: 6px !important;
            border: none !important; padding: 12px 24px !important;
            box-shadow: 0 4px 15px rgba(242, 92, 84, 0.25) !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<p class='titulo-nasa'>📝 Creador de Pruebas</p>", unsafe_allow_html=True)
    st.markdown("<p class='subtitulo-nasa'>Diseñador de Evaluaciones y Llaves Maestras Oficiales</p>", unsafe_allow_html=True)
    st.markdown("---")

    # 🎛️ COORDENADAS DE CONFIGURACIÓN GENERAL
    st.markdown("<h5 style='color: #0d1b2a; font-weight: bold;'>📋 Datos Generales del Examen</h5>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        titulo_prueba = st.text_input("📝 Nombre de la Evaluación:", placeholder="Ej: Bimestral Primer Periodo")
        grado_destino = st.selectbox("🏫 Grado / Curso Destino:", ["1°", "2°", "3°", "4°", "5°", "6°", "7°", "8°", "9°", "10°", "11°"])
    with c2:
        materia = st.selectbox("📚 Asignatura / Materia:", ["Matemáticas", "Español", "Ciencias Naturales", "Ciencias Sociales", "Inglés", "Filosofía", "Química", "Física"])
        num_preguntas = st.number_input("🔢 Número de Ítems / Preguntas:", min_value=1, max_value=100, value=10, step=1)
    with c3:
        tipo_prueba = st.selectbox("🏷️ Tipo de Evaluación:", ["Quiz", "Examen Bimestral", "Taller Integral", "Simulacro"])
        nota_maxima = st.number_input("🥇 Nota Máxima Posible (Escala):", min_value=1.0, max_value=10.0, value=5.0, step=0.5)

    # 📊 INDICADORES HUD DINÁMICOS
    valor_pregunta = nota_maxima / num_preguntas if num_preguntas > 0 else 0.0

    st.markdown(f"""
        <div class="hud-nasa-container">
            <div class="hud-nasa-card">
                <div class="hud-nasa-label">🔢 TOTAL PREGUNTAS</div>
                <div class="hud-nasa-value">{int(num_preguntas)}</div>
            </div>
            <div class="hud-nasa-card" style="border-left-color: #d4af37;">
                <div class="hud-nasa-label" style="color: #bfa12a;">🎯 VALOR POR ACERTO</div>
                <div class="hud-nasa-value" style="color: #d4af37;">{valor_pregunta:.2f}</div>
            </div>
            <div class="hud-nasa-card" style="border-left-color: #2b9348;">
                <div class="hud-nasa-label" style="color: #2b9348;">🏅 NOTA MÁXIMA</div>
                <div class="hud-nasa-value" style="color: #2b9348;">{nota_maxima:.1f}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 👑 CORONA DE LA LLAVE MAESTRA
    st.markdown("<div class='barra-matriz-oficial'>🛠️ Matriz de la Llave Maestra</div>", unsafe_allow_html=True)

    # Construcción interactiva de ítems en filas limpias y estéticas
    respuestas_maestras = []
    
    with st.container(border=True):
        for i in range(1, int(num_preguntas) + 1):
            r1, r2, r3 = st.columns([1, 2, 4])
            with r1:
                st.markdown(f"<p style='margin-top:10px; font-weight:bold; color:#0d1b2a;'>Ítem N° {i}</p>", unsafe_allow_html=True)
            with r2:
                opc_correcta = st.selectbox(f"Clave_{i}", ["A", "B", "C", "D"], label_visibility="collapsed", key=f"opc_{i}")
            with r3:
                st.text_input(f"Competencia_{i}", placeholder="Conceptos Clave / Competencia Evaluada", label_visibility="collapsed", key=f"comp_{i}")
            
            respuestas_maestras.append(opc_correcta)

    st.markdown("---")

    # 💾 BOTÓN DE ACCIÓN COMANDO
    c_btn, _ = st.columns([1, 2])
    with c_btn:
        if st.button("💾 Guardar Configuración y Crear Plantilla", use_container_width=True):
            if not titulo_prueba.strip():
                st.error("🚨 Error: Debe asignarle un nombre válido a la evaluación antes de guardarla.")
            else:
                with st.spinner("Sincronizando estructura con la tabla maestra..."):
                    try:
                        supabase = iniciar_conexion()
                        
                        # Compilamos las respuestas del docente en una sola cadena separada por comas
                        llave_string = ",".join(respuestas_maestras)
                        
                        # 🌟 SOLUCIÓN AL ERROR: Payload purificado con las columnas exactas de Supabase
                        payload = {
                            "nombre": titulo_prueba.strip(),
                            "materia": materia,
                            "total_preguntas": int(num_preguntas),
                            "llave_maestra": llave_string
                        }
                        
                        # Enviamos el cargamento limpio al búnker
                        supabase.table("pruebas_maestras").insert(payload).execute()
                        
                        st.success(f"🏆 ¡Evaluación '{titulo_prueba}' registrada con éxito en el banco de datos!")
                        st.balloons()
                    except Exception as e:
                        st.error(f"🚨 Error al guardar en la base de datos: {e}")
