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

    # 📡 EXTRACCIÓN INTELIGENTE DE ASIGNATURAS EXISTENTES EN EL BÚNKER
    with st.spinner("Escaneando asignaturas institucionales activas..."):
        try:
            res_materias = supabase.table("pruebas_maestras").select("materia").execute()
            # Extraemos valores únicos, limpiamos espacios y ordenamos alfabéticamente
            materias_banco = sorted(list(set([str(p["materia"]).upper().strip() for p in res_materias.data if p.get("materia")])))
        except Exception:
            materias_banco = []

    # =================================================================
    # 📋 FORMULARIO DE PARÁMETROS BÁSICOS DE LA EVALUACIÓN
    # =================================================================
    with st.container(border=True):
        st.markdown("<p style='color:#0d1b2a; font-weight:bold; margin-bottom:10px;'>🎯 CONFIGURACIÓN GENERAL DEL EXAMEN</p>", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            nombre_prueba = st.text_input("📝 Nombre de la Evaluación:", placeholder="Ej: Simulacro Final, Bimestral Uno...").upper().strip()
            
            # 🌟 SUGERENCIA IMPLEMENTADA: Selector dinámico premium en vez de campo de texto rígido
            opciones_desplegable = materias_banco + ["➕ REGISTRAR NUEVA ASIGNATURA..."]
            materia_seleccionada = st.selectbox("📚 Asignatura / Área (Menú Desplegable):", opciones_desplegable)
            
            # Si eligen crear una nueva, se despliega la casilla de escritura manual limpia
            if materia_seleccionada == "➕ REGISTRAR NUEVA ASIGNATURA...":
                materia_final = st.text_input("✍️ Escriba el nombre de la nueva Asignatura:", placeholder="Ej: BIOLOGÍA, FILOSOFÍA...").upper().strip()
            else:
                materia_final = materia_seleccionada

        with c2:
            total_preguntas = st.number_input("🔢 Número Total de Preguntas (Ítems):", min_value=1, max_value=100, value=10, step=1)
            puntaje_maximo = st.number_input("🎖️ Nota / Puntaje Máximo Posible:", min_value=1.0, max_value=100.0, value=5.0, step=0.5)

    # =================================================================
    # 🗃️ MATRIZ INTERACTIVA PREMIUM PARA LA LLAVE MAESTRA
    # =================================================================
    if nombre_prueba and materia_final:
        st.markdown("---")
        st.markdown("### 🔑 Estructuración de la Llave Maestra")
        st.write("Configure la opción correcta, el peso de la nota y el tema para cada ítem en la grilla interactiva:")

        # Cálculo automático de peso sugerido
        peso_automatico = round(float(puntaje_maximo) / int(total_preguntas), 2)

        data_inicial = {
            "Pregunta": [f"Pregunta {i+1}" for i in range(total_preguntas)],
            "Respuesta Correcta": ["A"] * total_preguntas,
            "Puntaje (Peso)": [peso_automatico] * total_preguntas,
            "Tema": ["Concepto General"] * total_preguntas
        }
        df_base_llave = pd.DataFrame(data_inicial)

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
        
        if st.button("💾 GUARDAR CONFIGURACIÓN Y CREAR PLANTILLA MAESTRA", type="primary", use_container_width=True):
            with st.spinner("Almacenando matriz criptográfica en el búnker..."):
                
                llave_maestra_json = df_editado.to_dict(orient="records")
                
                paquete_db = {
                    "nombre": nombre_prueba,
                    "materia": materia_final,
                    "total_preguntas": int(total_preguntas),
                    "puntaje_maximo": float(puntaje_maximo),
                    "llave_maestra": llave_maestra_json
                }
                
                try:
                    supabase.table("pruebas_maestras").insert(paquete_db).execute()
                    st.success(f"🎉 ¡Misión cumplida! La prueba '{nombre_prueba}' ha sido inyectada con éxito en la base de datos.")
                    st.balloons()
                    
                    # Forzar recarga limpia para actualizar la lista del selectbox en la próxima vuelta
                    st.rerun()
                except Exception as e_db:
                    st.error(f"💥 Error al guardar en la base institucional: {e_db}")
    else:
        st.info("💡 **Central en Espera:** Defina el Nombre del Examen y seleccione/registre la Asignatura arriba para liberar la matriz interactiva.")
