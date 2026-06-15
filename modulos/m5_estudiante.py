import streamlit as st
import pandas as pd
import re
import datetime
from supabase import create_client, Client

# =================================================================
# 🔒 CONEXIÓN AL BÚNKER (REGLA DE ORO: PROTECCIÓN DE CREDENCIALES)
# =================================================================
def iniciar_conexion():
    url = st.secrets["SUPABASE_URL"].replace('"', '').replace("'", "").strip()
    key = st.secrets["SUPABASE_KEY_REAL"].strip() if "SUPABASE_KEY_REAL" in st.secrets else st.secrets["SUPABASE_KEY"].strip()
    return create_client(url, key)

def ejecutar():
    # 🎨 INYECCIÓN VISUAL QUIRÚRGICA: Alto contraste sin alterar el panel izquierdo
    st.markdown("""
        <style>
        .titulo-estudiante { color: #0d1b2a; border-bottom: 3px solid #d4af37; padding-bottom: 5px; font-family: 'Arial Black'; }
        
        div[data-testid="stMainBlockContainer"] div[data-testid="stSelectbox"] label p {
            color: #0d1b2a !important; font-weight: 800 !important; text-transform: uppercase; font-size: 13px !important;
        }
        div[data-testid="stMainBlockContainer"] div[data-baseweb="select"] {
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

    with st.spinner("Sincronizando componentes del portal escolar..."):
        try:
            res_pruebas = supabase.table("pruebas_maestras").select("*").execute()
            pruebas = res_pruebas.data

            res_estudiantes = supabase.table("data_estudiantes").select("*").execute()
            datos_estudiantes = res_estudiantes.data
        except Exception as e:
            st.error(f"Error al descargar componentes: {e}")
            return

    if not pruebas:
        st.info("📭 No hay simulacros activos en este momento.")
        return

    # 📡 PROCESAMIENTO DE MATRÍCULA MASIVA PARA LOS DESPLEGABLES
    df_est = pd.DataFrame(datos_estudiantes) if datos_estudiantes else pd.DataFrame()
    lista_cursos = []
    
    if not df_est.empty:
        df_est.columns = [c.lower() for c in df_est.columns]
        df_est['grado'] = df_est['grado'].fillna('').astype(str).str.strip()
        df_est['grupo'] = df_est['grupo'].fillna('').astype(str).str.strip()
        df_est['curso_str'] = (df_est['grado'] + df_est['grupo']).str.strip()
        df_est['nombre_completo'] = df_est['nombre_completo'].fillna('').astype(str).str.strip()
        
        # Ordenamiento inteligente de cursos
        lista_cursos = sorted(list(df_est['curso_str'].unique()), key=lambda x: int(''.join(filter(str.isdigit, x))) if any(char.isdigit() for char in x) else 0)

    # =================================================================
    # 🎛️ SECUENCIA LÓGICA DE SELECTORES (UX MEJORADA)
    # =================================================================
    with st.container(border=True):
        st.markdown("<p style='color:#0d1b2a; font-weight:bold; margin-bottom:2px;'>👤 IDENTIFICACIÓN DEL ESTUDIANTE</p>", unsafe_allow_html=True)
        
        # 1. Selector de Curso / Grado
        curso_sel = st.selectbox("🏫 1. Selecciona tu Curso / Grado:", ["--- Elegir Curso ---"] + lista_cursos)
        
        # 2. Selector de Nombre (¡FIJADO EN EL SEGUNDO PUESTO!)
        nombres_filtrados = []
        if curso_sel != "--- Elegir Curso ---" and not df_est.empty:
            nombres_filtrados = sorted(df_est[df_est['curso_str'] == curso_sel]['nombre_completo'].tolist())
            
        estudiante_sel = st.selectbox("👤 2. Selecciona tu Nombre Completo:", ["--- Elegir Nombre ---"] + nombres_filtrados, disabled=(curso_sel == "--- Elegir Curso ---"))

    # 3. Selector de la Prueba a Presentar
    st.markdown("<br>", unsafe_allow_html=True)
    opciones_pruebas = {f"{p['nombre']} - {p['materia']}".strip(): p for p in pruebas}
    prueba_seleccionada = st.selectbox("📚 3. Selecciona la prueba que vas a presentar:", ["--- Selecciona la evaluación ---"] + list(opciones_pruebas.keys()), disabled=(estudiante_sel == "--- Elegir Nombre ---"))

    # =================================================================
    # 📝 CONSTRUCCIÓN DINÁMICA DEL FORMULARIO DE EXAMEN
    # =================================================================
    if (curso_sel != "--- Elegir Curso ---" and 
        estudiante_sel != "--- Elegir Nombre ---" and 
        prueba_seleccionada != "--- Selecciona la evaluación ---"):
        
        datos_prueba = opciones_pruebas[prueba_seleccionada]
        llave_maestra = datos_prueba["llave_maestra"]
        total_preguntas = int(datos_prueba.get("total_preguntas", 10))

        # Decodificador de seguridad para la Llave Maestra
        claves_lista = []
        if isinstance(llave_maestra, str):
            # 🌟 PARACAÍDAS INYECTADO: Evita la caída por float(None) al decodificar la llave en texto
            max_pts_seguro = float(datos_prueba.get("puntaje_maximo") if datos_prueba.get("puntaje_maximo") is not None else 5.0)
            puntaje_base = max_pts_seguro / total_preguntas
            claves_lista = [{"Pregunta": f"Pregunta {i+1}", "Respuesta Correcta": v.strip(), "Puntaje (Peso)": puntaje_base} for i, v in enumerate(llave_maestra.split(","))]
        else:
            claves_lista = llave_maestra

        st.markdown("---")
        st.markdown(f"### 📝 Simulacro Activo: {datos_prueba['nombre'].upper()}")
        st.info(f"👤 **Aspirante:** {estudiante_sel}  |  🏫 **Filiación:** Curso {curso_sel}")
        
        respuestas_estudiante = {}
        
        with st.form("form_examen"):
            for idx, item in enumerate(claves_lista):
                if idx >= total_preguntas: break
                pregunta = item.get("Pregunta", f"Pregunta {idx+1}")
                correcta_val = str(item.get("Respuesta Correcta", "A")).strip()
                
                if correcta_val in ["V", "F"]: opciones = ["V", "F"]
                elif correcta_val == "E": opciones = ["A", "B", "C", "D", "E"]
                else: opciones = ["A", "B", "C", "D"]

                respuestas_estudiante[pregunta] = st.radio(f"**{pregunta}:**", opciones, horizontal=True, key=f"quest_{idx}")

            st.markdown("---")
            submit = st.form_submit_button("✅ Finalizar y Calificar Prueba", type="primary", use_container_width=True)

        # =================================================================
        # 🚀 MOTOR DE CALIFICACIÓN Y ALMACENAMIENTO AUTOMÁTICO
        # =================================================================
        if submit:
            with st.spinner("Evaluando vectores de respuesta..."):
                puntaje_total = 0.0
                maximo_posible = float(datos_prueba.get("puntaje_maximo") if datos_prueba.get("puntaje_maximo") is not None else 5.0)

                for idx, item in enumerate(claves_lista):
                    if idx >= total_preguntas: break
                    pregunta = item.get("Pregunta", f"Pregunta {idx+1}")
                    peso = float(item.get("Puntaje (Peso)", maximo_posible / total_preguntas))
                    
                    if respuestas_estudiante.get(pregunta) == str(item.get("Respuesta Correcta", "")).strip():
                        puntaje_total += peso

                porcentaje = (puntaje_total / maximo_posible) * 100 if maximo_posible > 0 else 0
                identidad_maestra = f"{estudiante_sel} ({curso_sel})"

                paquete_nota = {
                    "id_prueba": datos_prueba.get("id", datos_prueba.get("id_prueba")),
                    "nombre_prueba": datos_prueba["nombre"],
                    "estudiante": identidad_maestra,
                    "puntaje_obtenido": round(puntaje_total, 2),
                    "puntaje_maximo": maximo_posible,
                    "porcentaje": round(porcentaje, 1),
                    "respuestas_json": respuestas_estudiante
                }
                
                try:
                    supabase.table("respuestas_estudiantes").insert(paquete_nota).execute()
                    st.balloons()
                    st.success("🎉 ¡Simulacro completado! Calificación resguardada en el búnker de datos.")
                    
                    st.markdown("#### 📋 Boletín de Resultados Inmediatos")
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Nota Lograda", f"{puntaje_total:.2f} / {maximo_posible:.1f}")
                    c2.metric("Efectividad", f"{porcentaje:.1f}%")
                    
                    if porcentaje >= 60: 
                        c3.success("ESTADO: APROBADO ✅")
                    else: 
                        c3.error("ESTADO: REPROBADO ❌")
                except Exception as e:
                    st.error(f"💥 Falla de comunicación al consolidar la nota: {e}")
