import streamlit as st
import pandas as pd
from supabase import create_client

# =================================================================
# 🔒 CONEXIÓN AL BÚNKER DE DATOS INSTITUCIONAL
# =================================================================
def iniciar_conexion():
    url = st.secrets["SUPABASE_URL"].strip()
    key = st.secrets["SUPABASE_KEY_REAL"].strip() if "SUPABASE_KEY_REAL" in st.secrets else st.secrets["SUPABASE_KEY"].strip()
    return create_client(url, key)

def ejecutar():
    # 🎨 INJECTION VISUAL (GÉNESIS HIGH-CONTRAST DESIGN) - Conservado al 100%
    st.markdown("""
        <style>
        .titulo-nasa { color: #0d1b2a; font-family: 'Arial Black'; font-size: 34px; margin-bottom: 0px; }
        .subtitulo-nasa { color: #d4af37; font-weight: bold; font-size: 13px; text-transform: uppercase; margin-top: 0px; }
        
        /* Contenedores de Formulario Premium */
        div[data-testid="stMainBlockContainer"] label p {
            color: #0d1b2a !important; font-weight: 800 !important; font-size: 12px !important; text-transform: uppercase;
        }
        div[data-baseweb="select"] {
            color: #0d1b2a !important; font-weight: bold !important;
        }
        
        /* HUD de Rendimiento en Tiempo Real */
        .hud-digitar {
            background: linear-gradient(135deg, #0d1b2a 0%, #1a365d 100%);
            border-radius: 6px; padding: 15px; color: white; text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<p class='titulo-nasa'>📝 Formato de Carga Directa</p>", unsafe_allow_html=True)
    st.markdown("---")

    try:
        supabase = iniciar_conexion()
    except Exception:
        st.error("🚨 Falla en el enlace satelital con Supabase.")
        return

    # 📥 DESCARGA COMPLETA DE EXÁMENES Y MATRÍCULAS
    with st.spinner("Sincronizando banco de evaluaciones maestros..."):
        try:
            res_pruebas = supabase.table("pruebas_maestras").select("*").execute()
            pruebas = res_pruebas.data
            
            # Descarga de alumnos optimizada en ráfagas de 1000
            estudiantes_base = []
            offset, chunk_size = 0, 1000
            while True:
                resultado = supabase.table("data_estudiantes").select('nombre_completo, grado').range(offset, offset + chunk_size - 1).execute()
                if not resultado.data: break
                estudiantes_base.extend(resultado.data)
                if len(resultado.data) < chunk_size: break
                offset += chunk_size
        except Exception as e:
            st.error(f"🚨 Error de lectura en la base de datos: {e}")
            return

    if not pruebas:
        st.info("📭 No hay evaluaciones registradas en el sistema.")
        return

    # =================================================================
    # 🎯 FIX MAESTRO: LLAVES ÚNICAS PARA QUE APAREZCAN TODAS LAS MATERIAS
    # =================================================================
    # Agregamos el grado y un consecutivo invisible al nombre para romper cualquier colisión en el diccionario.
    diccionario_pruebas = {}
    for idx, p in enumerate(pruebas):
        nombre_raw = str(p.get('nombre', 'SIN NOMBRE')).strip().upper()
        materia_raw = str(p.get('materia', 'SIN MATERIA')).strip().upper()
        grado_raw = str(p.get('grado', 'GENERAL')).strip().upper()
        
        # Etiqueta única ultra-descriptiva para el Selector
        etiqueta_selector = f"{nombre_raw} ({grado_raw}) - {materia_raw}"
        
        # Si por alguna razón extrema se repite, le añadimos el índice de seguridad
        if etiqueta_selector in diccionario_pruebas:
            etiqueta_selector = f"{etiqueta_selector} #{idx+1}"
            
        diccionario_pruebas[etiqueta_selector] = p

    # Despliegue simétrico del formulario en contenedores limpios
    with st.container(border=True):
        c1, c2 = st.columns(2)
        
        with c1:
            prueba_sel = st.selectbox("🎯 EVALUACIÓN CORRESPONDIENTE:", list(diccionario_pruebas.keys()))
            datos_prueba = diccionario_pruebas[prueba_sel]
            
            # Extraer límites de la evaluación con paracaídas anti-nulls
            raw_max_preguntas = datos_prueba.get('total_preguntas', 10)
            try:
                max_preguntas = int(raw_max_preguntas) if raw_max_preguntas is not None else 10
            except:
                max_preguntas = 10

            raw_puntaje_max = datos_prueba.get('puntaje_maximo', 5.0)
            try:
                puntaje_maximo = float(raw_puntaje_max) if raw_puntaje_max is not None else 5.0
            except:
                puntaje_maximo = 5.0

        with c2:
            # Filtrar alumnos del grado objetivo de la prueba seleccionada automáticamente
            grado_objetivo_prueba = str(datos_prueba.get('grado', '')).strip().upper()
            
            if estudiantes_base:
                df_est = pd.DataFrame(estudiantes_base)
                df_est.columns = [col.lower() for col in df_est.columns]
                
                # Filtrado inteligente por el grado del examen
                df_filtrado = df_est[df_est['grado'].str.upper().str.strip() == grado_objetivo_prueba]
                if not df_filtrado.empty:
                    lista_alumnos = sorted(df_filtrado['nombre_completo'].str.upper().unique().tolist())
                else:
                    lista_alumnos = sorted(df_est['nombre_completo'].str.upper().unique().tolist())
            else:
                lista_alumnos = ["NO HAY ALUMNOS REGISTRADOS"]

            alumno_sel = st.selectbox("👤 NOMBRE DEL ESTUDIANTE:", lista_alumnos)
            st.selectbox("👥 CURSO / GRADO:", [grado_objetivo_prueba], disabled=True)

    # =================================================================
    # 🧮 PANEL DE CONTEO DE ACIERTOS Y CÓMPUTO AUTOMÁTICO
    # =================================================================
    st.markdown("### 🎮 Entrada de Aciertos Reales")
    
    cc1, cc2 = st.columns([1.5, 1])
    
    with cc1:
        aciertos = st.number_input(
            f"✍️ CANTIDAD DE RESPUESTAS CORRECTAS (MÁXIMO DEL EXAMEN: {max_preguntas}):",
            min_value=0,
            max_value=max_preguntas,
            value=0,
            step=1
        )
        
        # Fórmulas de conversión matemática directa de Génesis
        porcentaje_rendimiento = (aciertos / max_preguntas) * 100 if max_preguntas > 0 else 0.0
        nota_proyectada = (aciertos / max_preguntas) * puntaje_maximo if max_preguntas > 0 else 0.0

    with cc2:
        # HUD dinámico de alto contraste idéntico al de tu pantalla
        st.markdown(f"""
            <div class="hud-digitar">
                <div style="display: flex; justify-content: space-around;">
                    <div>
                        <p style="margin:0; font-size:11px; color:#d4af37; font-weight:bold;">RENDIMIENTO</p>
                        <p style="margin:5px 0 0 0; font-size:24px; font-family:'Arial Black';">{porcentaje_rendimiento:.1f}%</p>
                    </div>
                    <div style="border-left: 1px solid rgba(255,255,255,0.2); padding-left:15px;">
                        <p style="margin:0; font-size:11px; color:#d4af37; font-weight:bold;">NOTA PROYECTADA</p>
                        <p style="margin:5px 0 0 0; font-size:24px; font-family:'Arial Black'; color:#00ff66;">{nota_proyectada:.2f} / {puntaje_maximo:.1f}</p>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    boton_inyectar = st.button("🚀 INYECTAR CALIFICACIÓN AL BÚNKER DE DATOS", use_container_width=True, type="primary")

    if boton_inyectar:
        if alumno_sel == "NO HAY ALUMNOS REGISTRADOS":
            st.error("❌ Operación denegada: No se puede asignar notas a un registro de matrícula vacío.")
            return

        # Empaquetamos la firma unificada para las sábanas de notas: "NOMBRE (GRADO)"
        firma_estudiante = f"{alumno_sel} ({grado_objetivo_prueba})"
        id_prueba_master = datos_prueba.get("id_prueba") or datos_prueba.get("id")

        payload_nota = {
            "id_prueba": id_prueba_master,
            "estudiante": signature_estudiante if 'signature_estudiante' in locals() else firma_estudiante,
            "puntaje_obtenido": round(nota_proyectada, 2),
            "puntaje_maximo": puntaje_maximo,
            "porcentaje": round(porcentaje_rendimiento, 2)
        }

        with st.spinner("Inyectando registro de calificación en caliente..."):
            try:
                supabase.table("respuestas_estudiantes").insert(payload_nota).execute()
                st.success(f"🎯 ¡IMPACTO EXITOSO! Calificación registrada para {alumno_sel} en {prueba_sel}.")
                st.balloons()
            except Exception as error_db:
                st.error(f"🚨 Error en el volcado transaccional: {error_db}")

if __name__ == "__main__":
    pass
