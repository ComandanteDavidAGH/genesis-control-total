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

# =================================================================
# 🛡️ SENSOR DETECTOR INALÁMBRICO DE COLUMNAS (Anti-Case-Sensitivity)
# =================================================================
def buscar_campo(diccionario, nombre_campo, predeterminado=""):
    if not diccionario:
        return predeterminado
    for llave, valor in diccionario.items():
        if llave.lower() == nombre_campo.lower():
            if valor is not None and str(valor).strip().lower() not in ['none', 'null', '']:
                return valor
    return predeterminado

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
                resultado = supabase.table("data_estudiantes").select('*').range(offset, offset + chunk_size - 1).execute()
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
    # 🎯 FIX MAESTRO: EXTRACCIÓN INMUNE A MAYÚSCULAS/MINÚSCULAS
    # =================================================================
    diccionario_pruebas = {}
    for idx, p in enumerate(pruebas):
        nombre_raw = str(buscar_campo(p, 'nombre', 'EXAMEN SIN NOMBRE')).strip().upper()
        materia_raw = str(buscar_campo(p, 'materia', 'MATERIA')).strip().upper()
        grado_raw = str(buscar_campo(p, 'grado', 'GENERAL')).strip().upper()
        
        # Formato de etiqueta limpio y homogéneo para el selector
        etiqueta_selector = f"{nombre_raw} - {materia_raw} ({grado_raw})"
        
        # Rompe colisiones duplicadas inyectando el ID real de la fila
        if etiqueta_selector in diccionario_pruebas:
            id_seguro = p.get('id_prueba', p.get('id', idx))
            etiqueta_selector = f"{etiqueta_selector} (ID: {id_seguro})"
            
        diccionario_pruebas[etiqueta_selector] = p

    # Despliegue del formulario en contenedores limpios
    with st.container(border=True):
        c1, c2 = st.columns(2)
        
        with c1:
            prueba_sel = st.selectbox("🎯 EVALUACIÓN CORRESPONDIENTE:", list(diccionario_pruebas.keys()))
            datos_prueba = diccionario_pruebas[prueba_sel]
            
            # Límites numéricos blindados con el nuevo sensor
            raw_max_preguntas = buscar_campo(datos_prueba, 'total_preguntas', 10)
            try:
                max_preguntas = int(raw_max_preguntas)
            except:
                max_preguntas = 10

            raw_puntaje_max = buscar_campo(datos_prueba, 'puntaje_maximo', 5.0)
            try:
                puntaje_maximo = float(raw_puntaje_max)
            except:
                puntaje_maximo = 5.0

        with c2:
            grado_objetivo_prueba = str(buscar_campo(datos_prueba, 'grado', 'GENERAL')).strip().upper()
            
            # Filtrado inteligente de estudiantes utilizando el sensor inmune
            if estudiantes_base:
                lista_alumnos = []
                for est in estudiantes_base:
                    nom_alumno = str(buscar_campo(est, 'nombre_completo')).strip().upper()
                    grad_alumno = str(buscar_campo(est, 'grado')).strip().upper()
                    
                    if grad_alumno == grado_objetivo_prueba or grado_objetivo_prueba in ['GENERAL', 'TODOS', '']:
                        if nom_alumno:
                            lista_alumnos.append(nom_alumno)
                
                # Paracaídas si no hay alumnos en ese grado específico
                if not lista_alumnos:
                    lista_alumnos = sorted(list(set([str(buscar_campo(e, 'nombre_completo')).strip().upper() for e in estudiantes_base if buscar_campo(e, 'nombre_completo')])))
                else:
                    lista_alumnos = sorted(list(set(lista_alumnos)))
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
        
        porcentaje_rendimiento = (aciertos / max_preguntas) * 100 if max_preguntas > 0 else 0.0
        nota_proyectada = (aciertos / max_preguntas) * puntaje_maximo if max_preguntas > 0 else 0.0

    with cc2:
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

        firma_estudiante = f"{alumno_sel} ({grado_objetivo_prueba})"
        id_prueba_master = datos_prueba.get("id_prueba") or datos_prueba.get("id")

        payload_nota = {
            "id_prueba": id_prueba_master,
            "estudiante": firma_estudiante,
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
