import streamlit as st
import pandas as pd
import io
from fpdf import FPDF
from supabase import create_client, Client

# =================================================================
# 🔒 ENLACE AL BÚNKER DE DATOS CENTRAL
# =================================================================
def iniciar_conexion():
    url = st.secrets["SUPABASE_URL"].strip()
    key = st.secrets["SUPABASE_KEY_REAL"].strip() if "SUPABASE_KEY_REAL" in st.secrets else st.secrets["SUPABASE_KEY"].strip()
    return create_client(url, key)

# =================================================================
# 📄 CLASE MAESTRA: DIBUJANTE VECTORIAL OMR (COMPATIBLE OPENCV)
# =================================================================
class HojaGigaOMR(FPDF):
    def __init__(self, nombre_prueba, materia):
        super().__init__(orientation='P', unit='mm', format='A4')
        self.nombre_prueba = nombre_prueba.upper()
        self.materia = materia.upper()

    def construir_hoja(self):
        self.add_page()
        self.set_auto_page_break(auto=False)
        
        # 🎯 1. ANCLAJES FIDUCIALES CRIPTOGRÁFICOS (Para calibración OpenCV)
        self.set_fill_color(0, 0, 0)
        self.rect(10, 10, 8, 8, 'F')          # Arriba-Izquierda
        self.rect(210 - 18, 10, 8, 8, 'F')    # Arriba-Derecha
        self.rect(10, 297 - 18, 8, 8, 'F')    # Abajo-Izquierda
        self.rect(210 - 18, 297 - 18, 8, 8, 'F') # Abajo-Derecha

        # 🏛️ 2. ENCABEZADO INSTITUCIONAL VIP
        self.set_font('Arial', 'B', 15)
        self.set_text_color(13, 27, 42) # Azul Génesis
        self.text(30, 18, "SISTEMA GÉNESIS v2.5 — PLANTILLA OMR MASTER")
        
        self.set_font('Arial', 'I', 10)
        self.set_text_color(120, 120, 120)
        self.text(30, 23, "Formatos de inspección óptica estandarizada para Visión Artificial")
        
        # Línea de separación estética
        self.set_draw_color(212, 175, 55) # Dorado Imperial
        self.set_line_width(0.8)
        self.line(30, 26, 210 - 25, 26)

        # 📋 3. CAJÓN DE CREDENCIALES DEL ESTUDIANTE
        self.set_draw_color(13, 27, 42)
        self.set_line_width(0.4)
        self.rect(25, 32, 210 - 50, 32)
        
        self.set_font('Arial', 'B', 9)
        self.set_text_color(13, 27, 42)
        
        self.text(30, 39, f"EVALUACIÓN:  {self.nombre_prueba}")
        self.text(130, 39, f"ASIGNATURA:  {self.materia}")
        
        self.text(30, 48, "ESTUDIANTE: __________________________________________________")
        self.text(30, 57, "CURSO / GRADO: __________________")
        self.text(130, 57, "FECHA: ____ / ____ / 2026")

        # 💡 4. INSTRUCCIONES PERIMETRALES PARA EL ALUMNO
        self.set_fill_color(240, 240, 240)
        self.rect(25, 70, 210 - 50, 12, 'F')
        self.set_font('Arial', 'B', 8)
        self.set_text_color(200, 0, 0)
        self.text(28, 75, "⚠️ REGLA DE ORO:")
        self.set_font('Arial', '', 8)
        self.set_text_color(50, 50, 50)
        self.text(54, 75, "Rellene completamente el círculo con lapicero negro o azul oscuro.")
        self.text(28, 79, "No haga tachaduras, enmiendas ni doble la hoja. El escáner anulará las respuestas mal marcadas.")

        # 🎯 5. GRID DE BURBUJAS (20 preguntas)
        self.set_font('Arial', 'B', 11)
        self.set_text_color(13, 27, 42)
        
        y_inicial = 94
        espacio_fila = 8.5
        opciones = ['A', 'B', 'C', 'D', 'E']
        
        for q in range(1, 21):
            y_actual = y_inicial + ((q - 1) * espacio_fila)
            str_q = f"{q:02d}."
            self.text(45, y_actual + 4.5, str_q)
            
            x_inicial_burbuja = 65
            espacio_burbuja = 11
            
            for idx, opcion in enumerate(opciones):
                x_actual = x_inicial_burbuja + (idx * espacio_burbuja)
                self.set_draw_color(80, 80, 80)
                self.ellipse(x_actual, y_actual, 6, 6)
                self.set_font('Arial', '', 8.5)
                self.set_text_color(100, 100, 100)
                self.text(x_actual + 1.8, y_actual + 4.3, opcion)

        self.text(25, 297 - 22, "GÉNESIS Autocontrol Scanner Core v2.5 — Suite Educativa de Alta Velocidad")

# =================================================================
# 👑 INTERFAZ DEL CREADOR DE EXÁMENES
# =================================================================
def ejecutar():
    st.markdown("""
        <style>
        .titulo-creador { color: #0d1b2a; font-family: 'Arial Black'; font-size: 34px; margin-bottom: 0px; }
        .subtitulo-creador { color: #d4af37; font-weight: bold; font-size: 13px; text-transform: uppercase; margin-top: 0px; }
        
        /* Forzar alto contraste en las etiquetas y opciones de los selectboxes del contenedor principal */
        div[data-testid="stForm"] label p {
            color: #0d1b2a !important; font-weight: bold !important; text-transform: uppercase; font-size: 12px;
        }
        div[data-testid="stForm"] div[data-baseweb="select"] {
            color: #0d1b2a !important; font-weight: bold !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<p class='titulo-creador'>📝 Creador de Evaluaciones Máster</p>", unsafe_allow_html=True)
    st.markdown("<p class='subtitulo-creador'>Diseño, Almacenamiento de Claves de Respuestas y Generación Autónoma de Hojas OMR</p>", unsafe_allow_html=True)
    st.markdown("---")

    try:
        supabase = iniciar_conexion()
    except Exception:
        st.error("🚨 Enlace de datos caído con el búnker de Supabase.")
        return

    # 📡 RADAR DE DATOS EXISTENTES: Extraer materias y grados reales para alimentar las casillas desplegables
    materias_existentes = ["MATEMÁTICAS", "ESPAÑOL", "CIENCIAS NATURALES", "SOCIALES", "INGLÉS"]
    grados_existentes = ["SEXTO A", "SÉPTIMO A", "OCTAVO A", "NOVENO A", "DÉCIMO A", "ONCE A"]
    
    try:
        res_db = supabase.table("pruebas_maestras").select("materia, grado").execute()
        if res_db.data:
            m_db = sorted(list(set([str(d['materia']).upper().strip() for d in res_db.data if d.get('materia')])))
            g_db = sorted(list(set([str(d['grado']).upper().strip() for d in res_db.data if d.get('grado')])))
            if m_db: materias_existentes = m_db
            if g_db: grados_existentes = g_db
    except Exception:
        pass

    # Añadimos los gatillos para registrar nuevos elementos
    opciones_materias = materias_existentes + ["[+ REGISTRAR NUEVA ASIGNATURA...]"]
    opciones_grados = grados_existentes + ["[+ REGISTRAR NUEVO CURSO/GRADO...]"]

    # Formulario de Configuración Táctica del Examen
    with st.form("formulario_examen", clear_on_submit=False):
        c1, c2 = st.columns(2)
        with c1:
            nombre_prueba = st.text_input("🎯 NOMBRE DE LA EVALUACIÓN:", placeholder="Ej: Bimestral Segundo Periodo")
            
            # 🔄 CASILLA DESPLEGABLE RESTAURADA PARA MATERIA
            materia_sel = st.selectbox("📚 ASIGNATURA / MATERIA:", opciones_materias, index=0)
            materia_nueva = ""
            if materia_sel == "[+ REGISTRAR NUEVA ASIGNATURA...]":
                materia_nueva = st.text_input("✍️ Escriba el nombre de la nueva Materia:")
                
        with c2:
            # 🔄 CASILLA DESPLEGABLE RESTAURADA PARA CURSO / GRADO
            grado_sel = st.selectbox("👥 CURSO / GRADO OBJETIVO:", opciones_grados, index=0)
            grado_nuevo = ""
            if grado_sel == "[+ REGISTRAR NUEVO CURSO/GRADO...]":
                grado_nuevo = st.text_input("✍️ Escriba el nombre del nuevo Curso/Grado:")
                
            puntaje_maximo = st.number_input("💯 NOTA MÁXIMA CONFIGURADA:", min_value=1.0, max_value=100.0, value=5.0, step=0.5)

        st.markdown("### 🔑 Matriz Clave de Respuestas Correctas (20 Preguntas Máximas):")
        st.info("💡 Marque la opción correcta para cada pregunta. Si su examen tiene menos de 20 preguntas, deje las sobrantes en la opción 'N/A' e ignore esas filas.")
        
        opciones_burbuja = ["A", "B", "C", "D", "E", "N/A"]
        claves_ingresadas = {}
        
        cols_grid = st.columns(4)
        for i in range(1, 21):
            col_activa = cols_grid[(i - 1) % 4]
            with col_activa:
                claves_ingresadas[f"p{i}"] = st.selectbox(f"Pregunta {i:02d}:", opciones_burbuja, index=0)

        st.markdown("---")
        boton_guardar = st.form_submit_button("🚀 GUARDAR EXAMEN EN EL BÚNKER INSTITUCIONAL", use_container_width=True)

    # 💾 PROCESAMIENTO E INYECCIÓN A LA BASE DE DATOS
    if boton_guardar:
        # Resolver si se usó opción preexistente o campo nuevo
        materia_final = materia_nueva if materia_sel == "[+ REGISTRAR NUEVA ASIGNATURA...]" else materia_sel
        grado_final = grado_nuevo if grado_sel == "[+ REGISTRAR NUEVO CURSO/GRADO...]" else grado_sel

        if not nombre_prueba or not materia_final or not grado_final:
            st.error("❌ Operación denegada: Todos los campos de identificación (Nombre, Materia y Grado) deben estar llenos.")
        else:
            lista_clave_limpia = [claves_ingresadas[f"p{x}"] for x in range(1, 21) if claves_ingresadas[f"p{x}"] != "N/A"]
            total_preguntas_reales = len(lista_clave_limpia)
            
            if total_preguntas_reales == 0:
                st.error("❌ Operación denegada: Debe configurar al menos una respuesta válida (diferente de N/A).")
                return

            clave_string = ",".join([claves_ingresadas[f"p{x}"] for x in range(1, 21)])

            payload_examen = {
                "nombre": nombre_prueba.strip().upper(),
                "materia": materia_final.strip().upper(),
                "grado": grado_final.strip().upper(),
                "puntaje_maximo": puntaje_maximo,
                "total_preguntas": total_preguntas_reales,
                "clave_respuestas": clave_string
            }

            with st.spinner("Inyectando registro en la base de datos central..."):
                try:
                    res = supabase.table("pruebas_maestras").insert(payload_examen).execute()
                    st.success(f"🎯 ¡IMPACTO EXITOSO! La prueba '{nombre_prueba.upper()}' ha sido dada de alta en Supabase.")
                    st.session_state['ultimo_examen_creado'] = payload_examen
                    st.rerun() # Recarga para actualizar las listas desplegables al instante
                except Exception as e:
                    st.error(f"🚨 Error en el volcado a la base de datos: {e}")

    # =================================================================
    # 📥 SECCIÓN COMPLEMENTARIA: GENERADOR DE SUMINISTROS IMPRIMIBLES
    # =================================================================
    if 'ultimo_examen_creado' in st.session_state:
        st.markdown("---")
        st.markdown("### 📥 Hojas de Respuestas Disponibles para Descarga:")
        ex_activo = st.session_state['ultimo_examen_creado']
        
        try:
            pdf_motor = HojaGigaOMR(nombre_prueba=ex_activo['nombre'], materia=ex_activo['materia'])
            pdf_motor.construir_hoja()
            
            buffer_pdf = io.BytesIO()
            pdf_motor.output(buffer_pdf)
            bytes_finales = buffer_pdf.getvalue()
            
            st.download_button(
                label=f"📄 DESCARGAR HOJA DE RESPUESTAS OMR IMPRIMIBLE ({ex_activo['nombre']})",
                data=bytes_finales,
                file_name=f"OMR_{ex_activo['nombre'].replace(' ', '_')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
            st.caption("ℹ️ Imprima este PDF en tamaño carta o A4 estándar. Asegúrese de que los 4 cuadros negros de las esquinas salgan nítidos para el correcto funcionamiento del escáner celular.")
        except Exception as e:
            st.warning(f"⚠️ El motor PDF está en espera de inicialización: {e}")
