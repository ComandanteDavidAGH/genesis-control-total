import streamlit as st
from estilos_globales import inyectar_estilos_omega
import pandas as pd
from supabase import create_client
import math
from fpdf import FPDF

# =================================================================
# 🔒 CONEXIÓN AL BÚNKER DE DATOS INSTITUCIONAL
# =================================================================
def iniciar_conexion():
    url = st.secrets["SUPABASE_URL"].strip()
    key = st.secrets["SUPABASE_KEY"].strip()
    return create_client(url, key)

# =================================================================
# 🖨️ MOTOR GENERADOR DE PLANTILLAS OMR (fpdf2)
# =================================================================

def generar_pdf_omr(titulo, materia, grado, num_preguntas):
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    
    # ==========================================
    # 1. MARCADORES FIDUCIARIOS (El ancla)
    # ==========================================
    tam_marcador = 8 
    margen = 12
    ancho_pagina, alto_pagina = 210, 297
    
    pdf.set_fill_color(0, 0, 0)
    pdf.rect(margen, margen, tam_marcador, tam_marcador, 'F')
    pdf.rect(ancho_pagina - margen - tam_marcador, margen, tam_marcador, tam_marcador, 'F')
    pdf.rect(margen, alto_pagina - margen - tam_marcador, tam_marcador, tam_marcador, 'F')
    pdf.rect(ancho_pagina - margen - tam_marcador, alto_pagina - margen - tam_marcador, tam_marcador, tam_marcador, 'F')

    pdf.set_fill_color(255, 255, 255)

    # ==========================================
    # 2. CABECERA INSTITUCIONAL
    # ==========================================
    pdf.set_y(18) # Bajamos el bloque entero un poquito respecto al borde superior
    pdf.set_font('helvetica', 'B', 14)
    pdf.cell(0, 8, 'SISTEMA GÉNESIS - HOJA DE RESPUESTAS OMR', border=0, align='C', new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font('helvetica', '', 10)
    titulo_mostrar = titulo if titulo else "EVALUACIÓN GENERAL"
    pdf.cell(0, 6, f'Prueba: {titulo_mostrar} | Área: {materia} | Grado: {grado}', border=0, align='C', new_x="LMARGIN", new_y="NEXT")
    
    # ⬇️ CALIBRACIÓN FLECHA 1: Oxígeno entre los títulos y el nombre del estudiante
    pdf.ln(15) # Antes estaba en 4. ¡Ahora tiene un buen espacio!
    
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(130, 8, 'Nombre del Estudiante: _________________________________________', border=0)
    pdf.cell(50, 8, 'Fecha: ______________', border=0, new_x="LMARGIN", new_y="NEXT")
    
    # Línea divisoria principal
    y_linea_actual = pdf.get_y() + 2 # Bajamos la línea 2mm para que no raye las letras
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(0.5)
    pdf.line(margen, y_linea_actual, ancho_pagina - margen, y_linea_actual)

    # ==========================================
    # 📐 DISTRIBUCIÓN MATEMÁTICA DEL ESPACIO
    # ==========================================
    # ⬇️ CALIBRACIÓN FLECHA 2: Aumentamos a 30 mm para equilibrar con el espacio superior
    inicio_y_cajas = y_linea_actual + 30 
    alto_cajas = 95 
    
    radio = 2.5
    diametro = radio * 2

    # ==========================================
    # 3. ZONA: CÓDIGO DE ESTUDIANTE (4 Dígitos)
    # ==========================================
    inicio_id_x = 20
    
    pdf.set_draw_color(180, 180, 180) 
    pdf.set_line_width(0.5)
    pdf.rect(inicio_id_x - 5, inicio_y_cajas, 55, alto_cajas, 'D')
    
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(0.2)
    
    pdf.set_xy(inicio_id_x, inicio_y_cajas + 2)
    pdf.set_font('helvetica', 'B', 9)
    pdf.cell(45, 5, 'ID ESTUDIANTE', border=0, align='C')
    
    x_cols_id = [inicio_id_x + 6, inicio_id_x + 16, inicio_id_x + 26, inicio_id_x + 36]
    y_inicio_burbujas_id = inicio_y_cajas + 15
    
    pdf.set_font('helvetica', '', 8)
    
    for idx, x_col in enumerate(x_cols_id):
        pdf.set_xy(x_col, y_inicio_burbujas_id - 5)
        pdf.cell(diametro, diametro, f'0{idx+1}', align='C')

    for fila in range(10):
        y_burbuja = y_inicio_burbujas_id + (fila * 7.5) 
        for x_col in x_cols_id:
            pdf.ellipse(x_col, y_burbuja, diametro, diametro, 'DF')
            pdf.set_xy(x_col, y_burbuja)
            pdf.cell(diametro, diametro, str(fila), align='C')

    # ==========================================
    # 4. ZONA: RESPUESTAS (2 Columnas)
    # ==========================================
    inicio_resp_x = 80
    
    pdf.set_draw_color(180, 180, 180)
    pdf.set_line_width(0.5)
    pdf.rect(inicio_resp_x - 5, inicio_y_cajas, 120, alto_cajas, 'D') 
    
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(0.2)
    
    pdf.set_xy(inicio_resp_x, inicio_y_cajas + 2)
    pdf.set_font('helvetica', 'B', 9)
    pdf.cell(110, 5, 'ZONA DE RESPUESTAS', border=0, align='C')
    
    opciones = ['A', 'B', 'C', 'D', 'E']
    y_inicio_burbujas_resp = inicio_y_cajas + 15
    espacio_entre_opciones = 7
    
    for i in range(1, num_preguntas + 1):
        columna_actual = 1 if i % 2 != 0 else 2
        fila_actual = math.ceil(i / 2) - 1
        
        x_pregunta = inicio_resp_x + 5 if columna_actual == 1 else inicio_resp_x + 60
        y_pregunta = y_inicio_burbujas_resp + (fila_actual * 7.5) 
        
        pdf.set_xy(x_pregunta, y_pregunta)
        pdf.set_font('helvetica', 'B', 8)
        pdf.cell(8, diametro, f'P{i:02d}', align='R')
        
        pdf.set_font('helvetica', '', 7)
        for idx_opc, letra in enumerate(opciones):
            x_burbuja = x_pregunta + 10 + (idx_opc * espacio_entre_opciones)
            pdf.ellipse(x_burbuja, y_pregunta, diametro, diametro, 'DF')
            pdf.set_xy(x_burbuja, y_pregunta)
            pdf.cell(diametro, diametro, letra, align='C')

    return pdf.output()
# =================================================================
# 🚀 FUNCIÓN PRINCIPAL DE EJECUCIÓN
# =================================================================
def ejecutar():
    # ⚡ Inyección visual unificada Génesis Omega Pro (Prioridad Alta)
    inyectar_estilos_omega()
    
    # ==========================================
    # 📊 ENCABEZADO PRINCIPAL DE ALTO IMPACTO
    # ==========================================
    st.markdown("<h1 style='text-align: center; color: #0F172A; font-size: 3rem;'>📝 Creador y Diseñador de Pruebas</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2rem; color: #D97706; font-weight: bold; letter-spacing: 1px;'>DISEÑO, ALMACENAMIENTO DE CLAVES Y GENERACIÓN DE MATRICES</p>", unsafe_allow_html=True)
    st.markdown("---")

    try:
        supabase = iniciar_conexion()
    except Exception:
        st.error("🚨 Falla en el enlace con el búnker de Supabase.")
        return

    # 📥 BARRIDO TÁCTICO EN SEGUNDO PLANO
    with st.spinner("Sincronizando catálogo oficial..."):
        try:
            res_consolidado = supabase.table("notas_consolidadas").select("ASIGNATURA").execute()
            materias_raw = res_consolidado.data if res_consolidado.data else []
            
            estudiantes_base = []
            offset, chunk_size = 0, 1000
            while True:
                resultado = supabase.table("data_estudiantes").select('Grado').range(offset, offset + chunk_size - 1).execute()
                if not resultado.data: break
                estudiantes_base.extend(resultado.data)
                if len(resultado.data) < chunk_size: break
                offset += chunk_size
        except Exception as e:
            st.error(f"🚨 Error de sincronización perimetral: {e}")
            return

    # 🧮 Procesamiento de listas
    lista_materias = sorted(pd.DataFrame(materias_raw)["ASIGNATURA"].dropna().unique().tolist()) if materias_raw else ["MATEMÁTICAS", "CIENCIAS", "LENGUAJE"]
    lista_grados = sorted(pd.DataFrame(estudiantes_base)["Grado"].dropna().unique().tolist()) if estudiantes_base else ["SEXTO A", "SÉPTIMO A"]

    # =================================================================
    # 🏛️ PASO 1: CONSOLA CENTRAL DE CONFIGURACIÓN
    # =================================================================
    st.markdown("### ⚙️ PASO 1: Configuración de la Evaluación")
    with st.container(border=True):
        r1_c1, r1_c2 = st.columns(2)
        with r1_c1: nombre_evaluacion = st.text_input("🎯 NOMBRE DE LA EVALUACIÓN:", placeholder="Ej: Lectura Crítica Segundo Periodo").strip().upper()
        with r1_c2: grado_objetivo = st.selectbox("👥 CURSO / GRADO OBJETIVO:", lista_grados)

        r2_c1, r2_c2 = st.columns(2)
        with r2_c1: asignatura = st.selectbox("🎨 ASIGNATURA / MATERIA:", lista_materias)
        with r2_c2: nota_maxima = st.number_input("💯 NOTA MÁXIMA:", min_value=1.0, max_value=10.0, value=5.0, step=0.1)

        r3_c1, r3_c2 = st.columns(2)
        with r3_c1: tipo_evaluacion = st.selectbox("📝 TIPO:", ["QUIZ", "TALLER", "EXPOSICIÓN", "EVALUACIÓN FINAL PERIODO"])
        with r3_c2: periodo_academico = st.selectbox("📂 PERIODO:", ["PRIMER PERIODO", "SEGUNDO PERIODO", "TERCER PERIODO", "CUARTO PERIODO"])

    # =================================================================
    # 🔑 PASO 2: MATRIZ DE RESPUESTAS
    # =================================================================
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🔑 PASO 2: Matriz Clave de Respuestas (Hasta 20 Ítems)")
    st.info("💡 Marque la opción correcta para cada pregunta. Deje en 'N/A' las preguntas no utilizadas para que el sistema las ignore automáticamente.")

    claves_seleccionadas = {}
    with st.container(border=True):
        for i in range(1, 21):
            if (i - 1) % 4 == 0: cols_matriz = st.columns(4)
            with cols_matriz[(i - 1) % 4]:
                claves_seleccionadas[f"p{i}"] = st.selectbox(f"PREGUNTA {i:02d}:", ["A", "B", "C", "D", "E", "N/A"], key=f"key_p_{i}")

    # Pre-cálculo de preguntas activas para retroalimentación visual
    preguntas_activas = len([v for v in claves_seleccionadas.values() if v != "N/A"])

    # =================================================================
    # 💾 PASO 3: SALVAGUARDA EN LA BASE DE DATOS
    # =================================================================
    st.markdown("---")
    st.markdown("### 💾 PASO 3: Indexación")
    
    if st.button(f"🚀 SALVAGUARDAR EVALUACIÓN EN EL BÚNKER ({preguntas_activas} Preguntas)", use_container_width=True, type="primary"):
        if not nombre_evaluacion:
            st.error("❌ Debe asignar un nombre válido a la evaluación antes de continuar.")
        elif preguntas_activas == 0:
            st.error("❌ No puede crear una evaluación con 0 preguntas válidas.")
        else:
            payload = {
                "nombre": f"{tipo_evaluacion} - {nombre_evaluacion} ({periodo_academico})",
                "materia": asignatura, 
                "grado": grado_objetivo,
                "puntaje_maximo": nota_maxima, 
                "total_preguntas": preguntas_activas,
                "clave_respuestas": claves_seleccionadas
            }
            try:
                supabase.table("pruebas_maestras").insert(payload).execute()
                st.success(f"🎉 ¡ÉXITO TOTAL! Examen indexado con {preguntas_activas} preguntas activas.")
                st.balloons()
            except Exception as e:
                st.error(f"🚨 Falla en el búnker transaccional: {e}")

    # =================================================================
    # 🖨️ PASO 4: GENERACIÓN DE PLANTILLA OMR (MODO UNIVERSAL)
    # =================================================================
    st.markdown("---")
    st.markdown("### 🖨️ PASO 4: Impresión de Operaciones Físicas")
    st.info("Despliegue la plantilla maestra con los marcadores fiduciarios y la matriz de ID. Solo se generarán las filas de las preguntas activas.")
    
    if preguntas_activas > 0:
        # Generar el PDF en memoria utilizando las variables actuales del formulario
        pdf_bytes = generar_pdf_omr(nombre_evaluacion, asignatura, grado_objetivo, preguntas_activas)
        
        st.download_button(
            label=f"📄 DESCARGAR PLANTILLA OMR - {grado_objetivo} ({preguntas_activas} PREGUNTAS)",
            data=bytes(pdf_bytes),
            file_name=f"OMR_{asignatura.replace(' ', '_')}_{grado_objetivo}.pdf",
            mime="application/pdf",
            type="secondary"
        )
    else:
        st.warning("⚠️ Debe configurar al menos 1 pregunta en el Paso 2 para habilitar la descarga de la plantilla.")

if __name__ == "__main__":
    ejecutar()
