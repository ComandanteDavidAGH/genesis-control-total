import streamlit as st
import pandas as pd
from supabase import create_client, Client

# =================================================================
# 🔒 CONEXIÓN SEGURA CON EL BÚNKER DE PRODUCCIÓN
# =================================================================
def iniciar_conexion():
    url = st.secrets["SUPABASE_URL"].replace('"', '').replace("'", "").strip()
    key = st.secrets["SUPABASE_KEY_REAL"].strip() if "SUPABASE_KEY_REAL" in st.secrets else st.secrets["SUPABASE_KEY"].strip()
    return create_client(url, key)

def ejecutar():
    # 🎨 INYECCIÓN DE CONTRASTE QUIRÚRGICO (GÉNESIS DESIGN SYSTEM)
    st.markdown("""
        <style>
        .titulo-creador { color: #0d1b2a; border-bottom: 3px solid #d4af37; padding-bottom: 5px; font-family: 'Arial Black'; }
        
        /* Forzar alto contraste en textos de etiquetas y selectores */
        div[data-testid="stMainBlockContainer"] div[data-testid="stSelectbox"] label p,
        div[data-testid="stMainBlockContainer"] div[data-testid="stNumberInput"] label p,
        div[data-testid="stMainBlockContainer"] div[data-testid="stTextInput"] label p {
            color: #0d1b2a !important; font-weight: 800 !important; text-transform: uppercase; font-size: 13px !important;
        }
        div[data-testid="stMainBlockContainer"] div[data-baseweb="select"], 
        div[data-testid="stMainBlockContainer"] input {
            color: #0d1b2a !important; font-weight: bold !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 class='titulo-creador'>📝 Diseñador de Pruebas y Plantillas Maestras</h1>", unsafe_allow_html=True)
    st.caption("Central de configuración de claves de respuestas (Llave Maestra) y pesos académicos.")

    try:
        supabase = iniciar_conexion()
    except Exception:
        st.error("⚠️ Falla de comunicación con el centro de datos.")
        return

    # =================================================================
    # 📋 FORMULARIO DE PARÁMETROS BÁSICOS DE LA EVALUACIÓN
    # =================================================================
    with st.container(border=True):
        st.markdown("<p style='color:#0d1b2a; font-weight:bold; margin-bottom:10px;'>🎯 CONFIGURACIÓN GENERAL DEL EXAMEN</p>", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            nombre_prueba = st.text_input("📝 Nombre de la Evaluación:", placeholder="Ej: Simulacro Final, Bimestral Uno...")
            materia = st.text_input("📚 Asignatura / Área:", placeholder="Ej: Matemáticas, Lenguaje, Ciencias...")
        with c2:
            total_preguntas = st.number_input("🔢 Número Total de Preguntas (Ítems):", min_value=1, max_value=100, value=10, step=1)
            puntaje_maximo = st.number_input("🎖️ Nota / Puntaje Máximo Posible:", min_value=1.0, max_value=100.0, value=5.0, step=0.5)

    # =================================================================
    # 🗃️ MATRIZ INTERACTIVA PREMIUM PARA LA LLAVE MAESTRA
    # =================================================================
    if nombre_prueba.strip() and materia.strip():
        st.markdown("---")
        st.markdown("### 🔑 Estructuración de la Llave Maestra")
        st.write("Configure la opción correcta, el peso de la nota y el tema para cada ítem en la grilla interactiva:")

        # Cálculo automático del peso por pregunta para facilitarle la vida al docente
        peso_automatico = round(float(puntaje_maximo) / int(total_preguntas), 2)

        # Construcción del DataFrame base para el Editor de Datos
        data_inicial = {
            "Pregunta": [f"Pregunta {i+1}" for i in range(total_preguntas)],
            "Respuesta Correcta": ["A"] * total_preguntas,
            "Puntaje (Peso)": [peso_automatico] * total_preguntas,
            "Tema": ["Concepto General"] * total_preguntas
        }
        df_base_llave = pd.DataFrame(data_inicial)

        # Despliegue de la rejilla interactiva de alta gama (Estilo Excel)
        df_editado = st.data_editor(
            df_base_llave,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Pregunta": st.column_config.TextColumn("Ítem Evaluado", disabled=True),
                "Respuesta Correcta": st.column_config.SelectboxColumn(
                    "Opción Correcta",
                    options=["A", "B", "C", "D", "E", "V", "F"],
                    required=True
                ),
                "Puntaje (Peso)": st.column_config.NumberColumn("Valor de la Nota", min_value=0.0, max_value=50.0, format="%.2f", required=True),
                "Tema": st.column_config.TextColumn("Componente / Tema de Estudio", placeholder="Ej: Álgebra, Sintaxis, Célula...")
            }
        )

        st.markdown("<br>", unsafe_allow_html=True)
        
        # Botón de guardado masivo en Supabase
        if st.button("💾 GUARDAR CONFIGURACIÓN Y CREAR PLANTILLA MAESTRA", type="primary", use_container_width=True):
            with st.spinner("Almacenando matriz criptográfica en el búnker..."):
                
                # Convertimos las filas del Excel interactivo en una lista de diccionarios JSON
                llave_maestra_json = df_editado.to_dict(orient="records")
                
                # Paquete unificado libre de la columna vieja 'tipo_evaluacion' para evitar el error PGRST204
                paquete_db = {
                    "nombre": nombre_prueba.strip(),
                    "materia": materia.strip(),
                    "total_preguntas": int(total_preguntas),
                    "puntaje_maximo": float(puntaje_maximo),
                    "llave_maestra": llave_maestra_json
                }
                
                try:
                    supabase.table("pruebas_maestras").insert(paquete_db).execute()
                    st.success(f"🎉 ¡Misión cumplida! La prueba '{nombre_prueba.upper()}' ha sido inyectada con éxito en el banco de datos.")
                    st.balloons()
                except Exception as e_db:
                    st.error(f"💥 Error al guardar en la base institucional: {e_db}")
    else:
        st.info("💡 **Central en Espera:** Complete el Nombre de la Evaluación y el Área arriba para desplegar la matriz de respuestas correctas.")
