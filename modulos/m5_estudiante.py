import streamlit as st
from supabase import create_client, Client

# =================================================================
# 🔌 CONEXIÓN AL BÚNKER (REGLA DE ORO: PROTECCIÓN DE CREDENCIALES)
# =================================================================
def iniciar_conexion():
    url = st.secrets["SUPABASE_URL"].replace('"', '').replace("'", "").strip()
    key = st.secrets["SUPABASE_KEY_REAL"].strip() if "SUPABASE_KEY_REAL" in st.secrets else st.secrets["SUPABASE_KEY"].strip()
    return create_client(url, key)

def ejecutar():
    # 🎨 INYECCIÓN VISUAL QUIRÚRGICA: Evita alterar la barra de navegación lateral
    st.markdown("""
        <style>
        .titulo-estudiante { color: #0d1b2a; border-bottom: 3px solid #d4af37; padding-bottom: 5px; font-family: 'Arial Black'; }
        
        /* Alto contraste solo para los elementos de entrada del cuerpo central */
        div[data-testid="stMainBlockContainer"] div[data-testid="stSelectbox"] label p,
        div[data-testid="stMainBlockContainer"] div[data-testid="stTextInput"] label p {
            color: #0d1b2a !important; font-weight: 800 !important; text-transform: uppercase; font-size: 13px !important;
        }
        div[data-testid="stMainBlockContainer"] div[data-baseweb="select"], 
        div[data-testid="stMainBlockContainer"] input {
            color: #0d1b2a !important; font-weight: bold !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 class='titulo-estudiante'>📱 Portal de Evaluación Estudiantil</h1>", unsafe_allow_html=True)

    try:
        supabase = iniciar_conexion()
    except Exception:
        st.error("⚠️ Error de conexión con la central de datos. Llame al docente.")
        return

    # 1. Extraer las pruebas disponibles de la Base de Datos
    try:
        respuesta = supabase.table("pruebas_maestras").select("*").execute()
        pruebas = respuesta.data
    except Exception as e:
        st.error(f"Error al descargar las pruebas: {e}")
        return

    if not pruebas:
        st.info("📭 No hay simulacros activos en este momento.")
        return

    # 2. Interfaz de Selección
    opciones_pruebas = {f"{p['nombre']} - {p['materia']}".strip(): p for p in pruebas}
    prueba_seleccionada = st.selectbox("📚 Selecciona la prueba a presentar:", ["--- Selecciona la evaluación ---"] + list(opciones_pruebas.keys()))

    if prueba_seleccionada != "--- Selecciona la evaluación ---":
        datos_prueba = opciones_pruebas[prueba_seleccionada]
        llave_maestra = datos_prueba["llave_maestra"]
        total_preguntas = int(datos_prueba.get("total_preguntas", 10))

        # Decodificador tolerante para la Llave Maestra (String vs Estructura JSON)
        claves_lista = []
        if isinstance(llave_maestra, str):
            puntaje_base = float(datos_prueba.get("puntaje_maximo") if datos_prueba.get("puntaje_maximo") is not None else 5.0) / total_preguntas
            claves_lista = [{"Pregunta": f"Pregunta {i+1}", "Respuesta Correcta": v.strip(), "Puntaje (Peso)": puntaje_base} for i, v in enumerate(llave_maestra.split(","))]
        else:
            claves_lista = llave_maestra

        with st.container(border=True):
            st.markdown("### 👤 Datos del Estudiante")
            estudiante = st.text_input("Escribe tu Nombre Completo y Grado (Ej: Juan Pérez - 10A):", placeholder="Nombre Apellido - Curso")

        if estudiante.strip():
            st.markdown("---")
            st.markdown(f"### 📝 Simulacro Activo: {datos_prueba['nombre']}")
            
            respuestas_estudiante = {}
            
            # 3. Construir el Cuestionario Dinámico Institucional
            with st.form("form_examen"):
                for idx, item in enumerate(claves_lista):
                    if idx >= total_preguntas: break
                    pregunta = item.get("Pregunta", f"Pregunta {idx+1}")
                    correcta_val = item.get("Respuesta Correcta", "A").strip()
                    
                    # Deducir opciones dinámicas basándonos en la respuesta esperada
                    if correcta_val in ["V", "F"]: 
                        opciones = ["V", "F"]
                    elif correcta_val == "E": 
                        opciones = ["A", "B", "C", "D", "E"]
                    else: 
                        opciones = ["A", "B", "C", "D"]

                    respuestas_estudiante[pregunta] = st.radio(f"**{pregunta}:**", opciones, horizontal=True, key=f"quest_{idx}")

                st.markdown("---")
                submit = st.form_submit_button("✅ Finalizar y Calificar Prueba", type="primary", use_container_width=True)

            # 4. Motor de Calificación Automática en Tiempo Real
            if submit:
                with st.spinner("Procesando respuestas del formulario digital..."):
                    puntaje_total = 0.0
                    maximo_posible = float(datos_prueba.get("puntaje_maximo") if datos_prueba.get("puntaje_maximo") is not None else 5.0)

                    for idx, item in enumerate(claves_lista):
                        if idx >= total_preguntas: break
                        pregunta = item.get("Pregunta", f"Pregunta {idx+1}")
                        peso = float(item.get("Puntaje (Peso)", maximo_posible / total_preguntas))
                        
                        if respuestas_estudiante.get(pregunta) == item.get("Respuesta Correcta", "").strip():
                            puntaje_total += peso

                    porcentaje = (puntaje_total / maximo_posible) * 100 if maximo_posible > 0 else 0

                    # 5. Registrar el paquete académico en la base institucional
                    paquete_nota = {
                        "id_prueba": datos_prueba.get("id", datos_prueba.get("id_prueba")),
                        "nombre_prueba": datos_prueba["nombre"],
                        "estudiante": estudiante.strip(),
                        "puntaje_obtenido": round(puntaje_total, 2),
                        "puntaje_maximo": maximo_posible,
                        "porcentaje": round(porcentaje, 1),
                        "respuestas_json": respuestas_estudiante
                    }
                    
                    try:
                        supabase.table("respuestas_estudiantes").insert(paquete_nota).execute()
                        st.balloons()
                        st.success("🎉 ¡Misión cumplida! Tu prueba ha sido enviada y registrada con éxito.")
                        
                        # Despliegue de Calificación Inmediata para el alumno
                        st.markdown("#### 📋 Resultados Obtenidos")
                        c1, c2, c3 = st.columns(3)
                        c1.metric("Puntaje Logrado", f"{puntaje_total:.2f} / {maximo_posible:.1f}")
                        c2.metric("Tasa de Efectividad", f"{porcentaje:.1f}%")
                        
                        if porcentaje >= 60: 
                            c3.success("ESTADO: APROBADO ✅")
                        else: 
                            c3.error("ESTADO: REPROBADO ❌")
                    except Exception as e:
                        st.error(f"💥 Error crítico al asegurar la calificación en el búnker: {e}")
