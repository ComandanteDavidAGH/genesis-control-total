import streamlit as st
from estilos_globales import inyectar_estilos_omega
import pandas as pd
from supabase import create_client
import math
from fpdf import FPDF
from datetime import datetime

# =================================================================
# 🔒 CONEXIÓN AL BÚNKER DE DATOS INSTITUCIONAL
# =================================================================
def iniciar_conexion():
    url = st.secrets["SUPABASE_URL"].strip()
    key = st.secrets["SUPABASE_KEY"].strip()
    return create_client(url, key)

# =================================================================
# 🖨️ MOTOR GENERADOR DE PLANTILLAS OMR (VERSIÓN DORADA - UNA HOJA)
# =================================================================
def generar_pdf_omr(titulo, materia, grado, num_preguntas):
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    
    # ==========================================
    # 🌟 MARCA DE AGUA DEL ESCUDO (15% OPACIDAD)
    # ==========================================
    # El escudo se dibuja DE PRIMERO para que todo lo demás quede impreso encima.
    ruta_emblema = 'assets/logo.png' 
    import os
    if os.path.exists(ruta_emblema):
        # Dimensiones para centrar un escudo de 80mm de ancho en una hoja A4 (210mm x 297mm)
        ancho_escudo = 80
        alto_escudo = 90  # Proporción aproximada del escudo B
        x_centro = (210 - ancho_escudo) / 2
        y_centro = (297 - alto_escudo) / 2
        
        # Bloque de precisión para opacidad en fpdf2
        with pdf.local_context(fill_opacity=0.15):
            pdf.image(ruta_emblema, x=x_centro, y=y_centro, w=ancho_escudo)
            
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
    pdf.set_y(18) 
    pdf.set_font('helvetica', 'B', 14)
    pdf.cell(0, 8, 'SISTEMA GÉNESIS - HOJA DE RESPUESTAS OMR', border=0, align='C', new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font('helvetica', '', 10)
    titulo_mostrar = titulo if titulo else "EVALUACIÓN GENERAL"
    pdf.cell(0, 6, f'Prueba: {titulo_mostrar} | Área: {materia} | Grado: {grado}', border=0, align='C', new_x="LMARGIN", new_y="NEXT")
    
    pdf.ln(15) 
    
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(130, 8, 'Nombre del Estudiante: _________________________________________', border=0)
    pdf.cell(50, 8, 'Fecha: ______________', border=0, new_x="LMARGIN", new_y="NEXT")
    
    # Línea divisoria principal
    y_linea_actual = pdf.get_y() + 2 
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(0.5)
    pdf.line(margen, y_linea_actual, ancho_pagina - margen, y_linea_actual)

    # ==========================================
    # 📐 DISTRIBUCIÓN MATEMÁTICA DEL ESPACIO
    # ==========================================
    inicio_y_cajas = y_linea_actual + 30 
    alto_cajas = 95 
    
    radio = 2.5
    diametro = radio * 2

    # ==========================================
    # 3. ZONA: CÓDIGO DE ESTUDIANTE (4 Dígitos con Casillas)
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
    
    # Dibujamos 4 cajas cuadradas para escribir los dígitos a mano
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(0.3)
    for x_col in x_cols_id:
        pdf.rect(x_col, y_inicio_burbujas_id - 7, diametro, diametro, 'D')

    # Volvemos al grosor de línea estándar para las burbujas
    pdf.set_line_width(0.2)
    pdf.set_font('helvetica', '', 8)

    # Generación de la matriz numérica (0-9)
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
    
    # 🪤 EL CEBO DE DETECCIÓN DE RADAR
    st.error("🚨 CRÍTICO: SI ESTÁS VIENDO ESTE MENSAJE ROJO, EL CÓDIGO NUEVO SÍ SE ACTUALIZÓ EN LA NUBE.")
    st.toast("📡 SEÑAL DE VIDA CAPTURADA V4.1", icon="🦅")
    
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

    # 📥 BARRIDO TÁCTICO EN SEGUNDO PLANO (CONEXIÓN DIRECTA A HORARIOS)
    with st.spinner("Sincronizando catálogo oficial..."):
        try:
            res_consolidado = supabase.table("notas_consolidadas").select("ASIGNATURA").execute()
            materias_raw = res_consolidado.data if res_consolidado.data else []
            
            # 👨‍🏫 EXTRACCIÓN DIRECTA DESDE LA TABLA DE HORARIOS REAL
            res_docentes = supabase.table("db_horarios").select("DOCENTE").execute()
            docentes_raw = res_docentes.data if res_docentes.data else []
            
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

    # 🧮 Procesamiento de listas con Limpieza y Ordenamiento
    lista_materias = sorted(pd.DataFrame(materias_raw)["ASIGNATURA"].dropna().unique().tolist()) if materias_raw else ["MATEMÁTICAS", "CIENCIAS", "LENGUAJE"]
    lista_grados = sorted(pd.DataFrame(estudiantes_base)["Grado"].dropna().unique().tolist()) if estudiantes_base else ["SEXTO A", "SÉPTIMO A"]
    
    # 🧠 EL FILTRO "EXCEL ÚNICOS": Convierte la columna DOCENTE en una lista sin repeticiones y ordenada
    if docentes_raw:
        df_docentes = pd.DataFrame(docentes_raw)
        lista_docentes = sorted(df_docentes["DOCENTE"].dropna().unique().tolist())
    else:
        lista_docentes = ["DR. DAVID AGH"]  # Respaldo táctico si la base de datos falla
    # =================================================================
    # 🏛️ PASO 1: CONSOLA CENTRAL DE CONFIGURACIÓN
    # =================================================================
    st.markdown("### ⚙️ PASO 1: Configuración de la Evaluación")
    
    lista_docentes = ["DR. DAVID AGH", "ING. ALEJANDRO M.", "DRA. ELENA R."]

    with st.container(border=True):
        # FILA 0: IDENTIFICACIÓN DE MANDO
        r0_c1, r0_c2 = st.columns(2)
        with r0_c1: docente_responsable = st.selectbox("👨‍🏫 DOCENTE RESPONSABLE (TRAZABILIDAD):", lista_docentes)
        with r0_c2: periodo_academico = st.selectbox("📂 PERIODO ACADÉMICO:", ["PRIMER PERIODO", "SEGUNDO PERIODO", "TERCER PERIODO", "CUARTO PERIODO"])

        # FILA 1: COORDENADAS DE LA EVALUACIÓN
        r1_c1, r1_c2 = st.columns(2)
        with r1_c1: nombre_evaluacion = st.text_input("🎯 NOMBRE DE LA EVALUACIÓN:", placeholder="Ej: Lectura Crítica Segundo Periodo").strip().upper()
        with r1_c2: grado_objetivo = st.selectbox("👥 CURSO / GRADO OBJETIVO:", lista_grados)

        # FILA 2: PARÁMETROS ACADÉMICOS
        r2_c1, r2_c2 = st.columns(2)
        with r2_c1: asignatura = st.selectbox("🎨 ASIGNATURA / MATERIA:", lista_materias)
        with r2_c2: tipo_evaluacion = st.selectbox("📝 TIPO DE EVALUACIÓN:", ["QUIZ", "TALLER", "EXPOSICIÓN", "EVALUACIÓN FINAL PERIODO"])

        # FILA 3: CÁLCULO DE LÍMITES ÓPTICOS Y COMPENSACIÓN AUTOMÁTICA
        r3_c1, r3_c2 = st.columns(2)
        with r3_c1: nota_maxima = st.number_input("💯 NOTA MÁXIMA:", min_value=1.0, max_value=10.0, value=5.0, step=0.1)
        with r3_c2:
            try:
                nombre_filtro_periodo = f"({periodo_academico})"
                res_pesos = supabase.table("pruebas_maestras").select("peso").eq("materia", asignatura).eq("grado", grado_objetivo).like("nombre", f"%{nombre_filtro_periodo}%").execute()
                pesos_existentes = [float(p.get('peso', 0)) for p in res_pesos.data] if res_pesos.data else []
                porcentaje_usado = sum(pesos_existentes) * 100
            except Exception:
                porcentaje_usado = 0.0

            porcentaje_disponible = max(0.0, 100.0 - porcentaje_usado)

            if tipo_evaluacion == "EVALUACIÓN FINAL PERIODO":
                peso_porcentaje = porcentaje_disponible
                st.markdown(f"<div style='background-color:#0d1b2a; padding:8px; border-radius:5px; border-left:4px solid #00ff66; color:white; font-weight:bold; margin-top:25px;'>⚖️ PESO AUTOMÁTICO ABSORBIDO: {peso_porcentaje:.0f}%</div>", unsafe_allow_html=True)
            else:
                valor_sugerido = min(20.0, porcentaje_disponible)
                peso_porcentaje = st.number_input(f"⚖️ PESO DE VALORACIÓN (Disponible: {porcentaje_disponible:.0f}%):", min_value=0.0, max_value=porcentaje_disponible, value=valor_sugerido, step=5.0)

            if porcentaje_disponible <= 0:
                st.error("🚨 Alerta: Este periodo ya completó el 100% de su peso académico.")
# ⚖️ FILA 4: ENTRADA CRÍTICA DE PONDERACIÓN INSTITUIONAL
        r4_c1, r4_c2 = st.columns(2)
        with r4_c1:
            peso_porcentaje = st.number_input(
                "⚖️ PESO / PORCENTAJE DE VALORACIÓN (%):", 
                min_value=5, 
                max_value=100, 
                value=20, 
                step=5,
                help="Defina cuánto vale esta nota dentro del periodo (Ej: 20 para 20%)"
            )
        with r4_c2:
            st.markdown("<br>", unsafe_allow_html=True)
            st.caption(f"💡 Configuración activa: Esta prueba representará el **{peso_porcentaje}%** de la nota definitiva.")

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
                "clave_respuestas": claves_seleccionadas,
                "peso": peso_porcentaje / 100.0,  # Guardamos como decimal (Ej: 0.20)
                "docente": docente_responsable     # Guardamos el nombre del maestro
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
