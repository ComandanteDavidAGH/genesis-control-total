import streamlit as st
import pandas as pd
import plotly.express as px
import io
from supabase import create_client, Client

# =================================================================
# 🔒 CONEXIÓN AL BÚNKER DE DATOS INSTITUCIONAL
# =================================================================
def iniciar_conexion():
    url = st.secrets["SUPABASE_URL"].strip()
    key = st.secrets["SUPABASE_KEY_REAL"].strip() if "SUPABASE_KEY_REAL" in st.secrets else st.secrets["SUPABASE_KEY"].strip()
    return create_client(url, key)

def ejecutar():
    # 🎨 INYECCIÓN VISUAL QUIRÚRGICA (GÉNESIS HIGH-CONTRAST DESIGN) - Respetada
    st.markdown("""
        <style>
        .titulo-dash { color: #0d1b2a; font-family: 'Arial Black'; font-size: 34px; margin-bottom: 0px; }
        .subtitulo-dash { color: #d4af37; font-weight: bold; font-size: 13px; text-transform: uppercase; margin-top: 0px; }
        
        div[data-testid="stMainBlockContainer"] div[data-testid="stSelectbox"] label p {
            color: #0d1b2a !important; font-weight: 800 !important; font-size: 13px !important; text-transform: uppercase;
        }
        div[data-testid="stMainBlockContainer"] div[data-baseweb="select"] {
            color: #0d1b2a !important; font-weight: bold !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<p class='titulo-dash'>📊 Dashboard Analítico e Informes</p>", unsafe_allow_html=True)
    st.markdown("<p class='subtitulo-dash'>Consola Central de Rendimiento y Exportación de Matrices de Calificación</p>", unsafe_allow_html=True)
    st.markdown("---")

    try:
        supabase = iniciar_conexion()
    except Exception:
        st.error("⚠️ Falla de enlace con la base de datos central.")
        return

    # 📥 DESCARGA DE COMPONENTES CRIPTOGRÁFICOS
    with st.spinner("Sincronizando registros analíticos..."):
        try:
            res_pruebas = supabase.table("pruebas_maestras").select("*").execute()
            pruebas = res_pruebas.data
            
            res_notas = supabase.table("respuestas_estudiantes").select("*").execute()
            notas_raw = res_notas.data
        except Exception as e:
            st.error(f"Error de lectura en el búnker: {e}")
            return

    if not pruebas:
        st.info("📭 No se registran evaluaciones maestras en el banco de datos para analizar.")
        return

    # 🎛️ SELECTOR GENERAL DE PRUEBAS
    diccionario_pruebas = {f"{p['nombre']} - {p['materia']}".strip().upper(): p for p in pruebas}
    prueba_sel = st.selectbox("🎯 SELECCIONE LA EVALUACIÓN MÁSTER PARA AUDITAR:", list(diccionario_pruebas.keys()))

    # Filtrado dinámico de calificaciones
    datos_prueba_activa = diccionario_pruebas[prueba_sel]
    id_prueba_activa = datos_prueba_activa.get("id", datos_prueba_activa.get("id_prueba"))
    
    df_notas = pd.DataFrame(notas_raw) if notas_raw else pd.DataFrame()
    
    if not df_notas.empty:
        # Asegurar compatibilidad de columnas en minúsculas
        df_notas.columns = [c.lower() for c in df_notas.columns]
        df_notas = df_notas[df_notas['id_prueba'] == id_prueba_activa]

    # =================================================================
    # 🗃️ PROCESAMIENTO Y LIMPIEZA DE COLUMNAS PARA EL PUENTE DE NOTAS
    # =================================================================
    df_informe_limpio = pd.DataFrame()
    conteo_niveles = {"Bajo (<60%)": 0, "Básico (60-79%)": 0, "Alto (80-89%)": 0, "Superior (≥90%)": 0}

    if not df_notas.empty:
        filas_limpias = []
        for _, fila in df_notas.iterrows():
            estudiante_str = str(fila.get('estudiante', 'ALUMNO ANÓNIMO'))
            
            # Algoritmo de extracción para separar "Nombre Alumno" y "Curso" - Respetado
            nombre_final = estudiante_str
            curso_final = "SIN CURSO"
            if "(" in estudiante_str and ")" in estudiante_str:
                parts = estudiante_str.split("(")
                nombre_final = parts[0].strip()
                curso_final = parts[1].replace(")", "").strip()

            # =================================================================
            # 💉 CIRUGÍA LÁSER APLICADA AQUÍ (Sustitución de las 3 líneas críticas)
            # =================================================================
            # Instalamos paracaídas para evitar float(None).
            
            # 1. Porcentaje Blindado
            raw_pct = fila.get('porcentaje')
            pct = float(raw_pct) if raw_pct is not None else 0.0
            
            # 2. Nota Lograda Blindada
            raw_nota = fila.get('puntaje_obtenido')
            nota = float(raw_nota) if raw_nota is not None else 0.0
            
            # 3. Nota Máxima Blindada
            raw_max_p = fila.get('puntaje_maximo')
            max_p = float(raw_max_p) if raw_max_p is not None else 5.0
            
            # =================================================================
            # 🚫 FIN DE LA CIRUGÍA LÁSER
            # =================================================================
            
            # Clasificación de rangos oficiales - Respetada
            if pct < 60.0:
                nivel = "Bajo (<60%)"
                estado = "REPROBADO ❌"
                conteo_niveles["Bajo (<60%)"] += 1
            elif 60.0 <= pct < 80.0:
                nivel = "Básico (60-79%)"
                estado = "APROBADO ✅"
                conteo_niveles["Básico (60-79%)"] += 1
            elif 80.0 <= pct < 90.0:
                nivel = "Alto (80-89%)"
                estado = "APROBADO ✅"
                conteo_niveles["Alto (80-89%)"] += 1
            else:
                nivel = "Superior (≥90%)"
                estado = "APROBADO ✅"
                conteo_niveles["Superior (≥90%)"] += 1

            filas_limpias.append({
                "ESTUDIANTE MATRÍCULA": nombre_final.upper(),
                "CURSO / GRADO": curso_final.upper(),
                "NOTA LOGRADA": round(nota, 2),
                "NOTA MÁXIMA": round(max_p, 2),
                "EFECTIVIDAD %": f"{pct:.1f}%",
                "RANGO COGNITIVO": nivel,
                "ESTADO ACADÉMICO": estado
            })
        
        df_informe_limpio = pd.DataFrame(filas_limpias).sort_values(by="ESTUDIANTE MATRÍCULA")

    # =================================================================
    # 📐 DISTRIBUCIÓN GRÁFICA Y BLOQUES DE DETALLE (UX SIMÉTRICA) - Respetado
    # =================================================================
    c1, c2 = st.columns([1, 1.2])
    
    with c1:
        st.markdown("### 📝 Detalles de Operación")
        tabla_detalles = pd.DataFrame({
            "Especificación": ["Examen Activo", "Asignatura", "Preguntas Totales", "Puntaje Máximo", "Último Escaneo"],
            "Detalle": [
                str(datos_prueba_activa.get("nombre")).upper(),
                str(datos_prueba_activa.get("materia")).upper(),
                f"{datos_prueba_activa.get('total_preguntas', 10)} Ítems",
                f"{datos_prueba_activa.get('puntaje_maximo', 5.0)} Pts",
                "2026-06-15"
            ]
        })
        st.dataframe(tabla_detalles, use_container_width=True, hide_index=True)
        
        # 📊 SECCIÓN DE DESCARGAS ANALÍTICAS
        st.markdown("### 📥 Descargar Reportes Masivos:")
        
        if not df_informe_limpio.empty:
            buffer_excel = io.BytesIO()
            with pd.ExcelWriter(buffer_excel, engine='xlsxwriter') as writer:
                df_informe_limpio.to_excel(writer, sheet_name='Calificaciones', index=False)
                workbook = writer.book
                worksheet = writer.sheets['Calificaciones']
                worksheet.set_column('A:G', 22)
            
            buffer_csv = df_informe_limpio.to_csv(index=False).encode('utf-8')
            
            cx1, cx2, cx3 = st.columns(3)
            cx1.download_button("🟢 Excel", data=buffer_excel.getvalue(), file_name=f"REPORTE_{datos_prueba_activa['nombre']}.xlsx", mime="application/vnd.ms-excel", use_container_width=True)
            cx2.download_button("📄 CSV", data=buffer_csv, file_name=f"REPORTE_{datos_prueba_activa['nombre']}.csv", mime="text/csv", use_container_width=True)
            cx3.button("🚀 Migrar", type="secondary", disabled=True, use_container_width=True, help="Conducto directo API automatizado.")
        else:
            st.warning("⚠️ Sin datos consolidados para exportar en esta prueba.")

    with c2:
        st.markdown("### 📊 Distribución de Puntuaciones")
        df_grafico = pd.DataFrame({
            "Nivel": list(conteo_niveles.keys()),
            "Hojas": list(conteo_niveles.values())
        })
        
        fig = px.bar(
            df_grafico, x="Nivel", y="Hojas",
            color="Nivel",
            color_discrete_map={
                "Bajo (<60%)": "#ff4b4b",
                "Básico (60-79%)": "#ffaa00",
                "Alto (80-89%)": "#38b000",
                "Superior (≥90%)": "#007200"
            },
            text_auto=True,
            height=320
        )
        fig.update_layout(showlegend=False, margin=dict(l=10, r=10, t=10, b=10), xaxis_title=None)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    # =================================================================
    # 📋 SECCIÓN INFERIOR: TABLERO GENERAL DE ASISTENCIA - Respetado
    # =================================================================
    st.markdown("---")
    st.markdown("### 📋 Control de Asistencia y Sabana Escaneada")
    
    if not df_informe_limpio.empty:
        st.data_editor(df_informe_limpio, use_container_width=True, hide_index=True, disabled=True)
    else:
        st.info("💡 Consola Vacía: No se registran exámenes presentados para esta evaluación aún.")
