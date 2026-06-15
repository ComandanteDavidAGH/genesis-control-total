import streamlit as st
import pandas as pd
from supabase import create_client, Client

# =================================================================
# 🔒 ENLACE AL BÚNKER DE DATOS CENTRAL
# =================================================================
def iniciar_conexion():
    url = st.secrets["SUPABASE_URL"].strip()
    key = st.secrets["SUPABASE_KEY_REAL"].strip() if "SUPABASE_KEY_REAL" in st.secrets else st.secrets["SUPABASE_KEY"].strip()
    return create_client(url, key)

# =================================================================
# 👑 INTERFAZ DE DIGITACIÓN MANUAL DE CALIFICACIONES
# =================================================================
def ejecutar():
    st.markdown("""
        <style>
        .titulo-digitar { color: #0d1b2a; font-family: 'Arial Black'; font-size: 34px; margin-bottom: 0px; }
        .subtitulo-digitar { color: #d4af37; font-weight: bold; font-size: 13px; text-transform: uppercase; margin-top: 0px; }
        .hud-digitar {
            background: linear-gradient(135deg, #0d1b2a 0%, #1e3a8a 100%);
            padding: 15px; border-radius: 8px; color: white; font-weight: bold;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.2); margin-bottom: 20px;
        }
        
        /* Ajuste visual de alto contraste para consistencia de marca */
        div[data-testid="stForm"] label p, .stSelectbox label p {
            color: #0d1b2a !important; font-weight: bold !important; text-transform: uppercase; font-size: 12px;
        }
        div[data-baseweb="select"] {
            color: #0d1b2a !important; font-weight: bold !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<p class='titulo-digitar'>✍️ Digitación Manual de Notas</p>", unsafe_allow_html=True)
    st.markdown("<p class='subtitulo-digitar'>Consola de Contingencia para el Registro y Carga Directa de Calificaciones</p>", unsafe_allow_html=True)
    st.markdown("---")

    try:
        supabase = iniciar_conexion()
    except Exception:
        st.error("🚨 Enlace de comunicaciones roto con el búnker de Supabase.")
        return

    # 📥 EXTRACCIÓN DE PRUEBAS ACTIVAS DESDE EL BÚNKER
    with st.spinner("Sincronizando registros de evaluaciones..."):
        try:
            res_pruebas = supabase.table("pruebas_maestras").select("*").execute()
            pruebas = res_pruebas.data
        except Exception as e:
            st.error(f"Error al leer sábanas de configuración: {e}")
            return

    if not pruebas:
        st.info("📭 No hay exámenes registrados en el sistema. Vaya al Módulo 2 para crear una prueba.")
        return

    # 📡 BANCO DE MEMORIA HISTÓRICA PARA DESPLEGABLES
    grados_existentes = ["SEXTO A", "SÉPTIMO A", "OCTAVO A", "NOVENO A", "DÉCIMO A", "ONCE A"]
    estudiantes_existentes = ["JUAN PÉREZ", "MARÍA RODRÍGUEZ", "CARLOS GÓMEZ"]

    try:
        if pruebas:
            g_list = sorted(list(set([str(p['grado']).upper().strip() for p in pruebas if p.get('grado') and str(p['grado']).strip() != 'None'])))
            if g_list: grados_existentes = g_list
            
        res_est = supabase.table("respuestas_estudiantes").select("estudiante").execute()
        if res_est.data:
            e_list = []
            for d in res_est.data:
                est = str(d.get('estudiante', '')).upper().strip()
                if "(" in est:  
                    est = est.split("(")[0].strip()
                if est and est != "NONE" and est != "NULL":
                    e_list.append(est)
            e_list = sorted(list(set(e_list)))
            if e_list: estudiantes_existentes = e_list
    except Exception:
        pass

    opciones_estudiantes = estudiantes_existentes + ["[+ REGISTRAR NUEVO ESTUDIANTE...]"]
    opciones_grados = grados_existentes + ["[+ REGISTRAR NUEVO CURSO/GRADO...]"]

    diccionario_pruebas = {f"{p.get('nombre', 'SIN NOMBRE')} - {p.get('materia', 'SIN MATERIA')}".upper(): p for p in pruebas}

    # =================================================================
    # 📝 FORMULARIO DE INYECCIÓN MANUAL
    # =================================================================
    with st.form("formulario_digitacion", clear_on_submit=False):
        st.markdown("### 📋 Formato de Carga Directa")
        
        c1, c2 = st.columns(2)
        with c1:
            prueba_sel = st.selectbox("🎯 EVALUACIÓN CORRESPONDIENTE:", list(diccionario_pruebas.keys()))
            datos_examen = diccionario_pruebas[prueba_sel]
            
            grado_predeterminado = str(datos_examen.get('grado', '')).upper().strip()
            idx_grado_auto = 0
            if grado_predeterminado in grados_existentes:
                idx_grado_auto = grados_existentes.index(grado_predeterminado)
                
            # Extraer nota tope y total preguntas permitidas
            raw_puntaje_maximo = datos_examen.get('puntaje_maximo')
            try:
                nota_maxima_posible = float(raw_puntaje_maximo) if raw_puntaje_maximo is not None else 5.0
            except (ValueError, TypeError):
                nota_maxima_posible = 5.0

            raw_total_preguntas = datos_examen.get('total_preguntas')
            try:
                total_preguntas = int(raw_total_preguntas) if raw_total_preguntas is not None else 20
            except (ValueError, TypeError):
                total_preguntas = 20

        with c2:
            estudiante_sel = st.selectbox("👤 NOMBRE DEL ESTUDIANTE:", opciones_estudiantes, index=0)
            nombre_alumno = ""
            if estudiante_sel == "[+ REGISTRAR NUEVO ESTUDIANTE...]":
                nombre_alumno = st.text_input("✍️ Escriba el nombre del nuevo Estudiante:").strip().upper()
            else:
                nombre_alumno = estudiante_sel

            grado_sel = st.selectbox("👥 CURSO / GRADO:", opciones_grados, index=idx_grado_auto)
            curso_alumno = ""
            if grado_sel == "[+ REGISTRAR NUEVO CURSO/GRADO...]":
                curso_alumno = st.text_input("✍️ Escriba el nombre del nuevo Curso/Grado:").strip().upper()
            else:
                curso_alumno = grado_sel

        st.markdown("---")
        st.markdown("### 🧮 Entrada de Aciertos Reales")
        
        cx1, cx2 = st.columns(2)
        with cx1:
            # 🔄 UPGRADE: Ahora el docente solo introduce cuántas preguntas buenas sacó el alumno
            aciertos_ingresados = st.number_input(f"✍️ CANTIDAD DE RESPUESTAS CORRECTAS (Máximo del Examen: {total_preguntas}):", min_value=0, max_value=total_preguntas, value=0, step=1)
        with cx2:
            # El sistema calcula de forma limpia la nota decimal y el rendimiento
            porcentaje_efectividad = (aciertos_ingresados / total_preguntas) * 100 if total_preguntas > 0 else 0
            nota_calculada = (aciertos_ingresados / total_preguntas) * nota_maxima_posible if total_preguntas > 0 else 0
            
            st.markdown(f"""
                <div class="hud-digitar">
                    <div style="display: flex; justify-content: space-around; align-items: center;">
                        <div>
                            <p style="margin:0; font-size:11px; color:#d4af37; text-transform:uppercase;">Rendimiento</p>
                            <p style="margin:2px 0 0 0; font-size:22px; color:#00ff66;">{porcentaje_efectividad:.1f}%</p>
                        </div>
                        <div style="border-left: 2px solid rgba(255,255,255,0.2); height: 35px;"></div>
                        <div>
                            <p style="margin:0; font-size:11px; color:#d4af37; text-transform:uppercase;">Nota Proyectada</p>
                            <p style="margin:2px 0 0 0; font-size:22px; color:#00ff66;">{nota_calculada:.2f} / {nota_maxima_posible}</p>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        boton_transmitir = st.form_submit_button("🚀 INYECTAR CALIFICACIÓN AL BÚNKER DE DATOS", use_container_width=True)

    # =================================================================
    # 💾 VOLCADO TRANSACCIONAL A SUPABASE
    # =================================================================
    if boton_transmitir:
        if not nombre_alumno or not curso_alumno:
            st.error("❌ Operación rechazada: La identidad del alumno y el curso son credenciales obligatorias.")
        else:
            cadena_estudiante_completa = f"{nombre_alumno} ({curso_alumno})"
            id_prueba_activa = datos_examen.get("id_prueba") or datos_examen.get("id")

            payload_nota = {
                "id_prueba": id_prueba_activa,
                "estudiante": cadena_estudiante_completa,
                "porcentaje": round(porcentaje_efectividad, 2),
                "puntaje_obtenido": round(nota_calculada, 2), # Se inyecta la nota limpia calculada por el software
                "puntaje_maximo": nota_maxima_posible
            }

            with st.spinner("Sincronizando paquete de datos con Supabase..."):
                try:
                    supabase.table("respuestas_estudiantes").insert(payload_nota).execute()
                    st.success(f"🎯 ¡REGISTRO EXITOSO! La calificación de '{nombre_alumno}' fue indexada de forma limpia. Sábana actualizada.")
                    st.balloons()
                    st.rerun()
                except Exception as e:
                    st.error(f"🚨 Falla en el volcado de transacciones manuales: {e}")

if __name__ == "__main__":
    pass
