import streamlit as st
from estilos_globales import inyectar_estilos_omega  # <--- ESTA ES LA LÍNEA NUEVA
import pandas as pd
import plotly.express as px
import io
from supabase import create_client

# =================================================================
# 🔒 CONEXIÓN AL BÚNKER DE DATOS INSTITUCIONAL (Llave Única Unificada)
# =================================================================
def iniciar_conexion():
    url = st.secrets["SUPABASE_URL"].strip()
    key = st.secrets["SUPABASE_KEY"].strip()
    return create_client(url, key)

# =================================================================
# 🛡️ SENSOR DETECTOR INALÁMBRICO DE COLUMNAS (Versión Fail-Safe Pandas)
# =================================================================
def buscar_campo(diccionario, nombre_campo, predeterminado=""):
    if diccionario is None:
        return predeterminado
    
    # ⚡ FIX DEFENSIVO: Evita la ambigüedad si el objeto es una Serie de Pandas
    try:
        if hasattr(diccionario, 'empty') and diccionario.empty:
            return predeterminado
    except:
        pass

    # Búsqueda segura e insensible a mayúsculas/minúsculas
    try:
        for llave, valor in diccionario.items():
            if str(llave).lower() == nombre_campo.lower():
                if valor is not None and str(valor).strip().lower() not in ['none', 'null', '']:
                    return valor
    except:
        pass
    return predeterminado

def ejecutar():
    # 🎨 INYECCIÓN VISUAL QUIRÚRGICA (GÉNESIS HIGH-CONTRAST DESIGN) - Tu estilo intacto
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
    diccionario_pruebas = {}
    for idx, p in enumerate(pruebas):
        nombre_raw = str(buscar_campo(p, 'nombre', 'EXAMEN SIN NOMBRE')).strip().upper()
        materia_raw = str(buscar_campo(p, 'materia', 'MATERIA')).strip().upper()
        grado_raw = str(buscar_campo(p, 'grado', 'GENERAL')).strip().upper()
        
        etiqueta_selector = f"{nombre_raw} - {materia_raw} ({grado_raw})"
        if etiqueta_selector in diccionario_pruebas:
            id_seguro = p.get('id_prueba', p.get('id', idx))
            etiqueta_selector = f"{etiqueta_selector} (ID: {id_seguro})"
            
        diccionario_pruebas[etiqueta_selector] = p

    prueba_sel = st.selectbox("🎯 SELECCIONE LA EVALUACIÓN MÁSTER PARA AUDITAR:", list(diccionario_pruebas.keys()))

    # Filtrado dinámico de calificaciones
    datos_prueba_activa = diccionario_pruebas[prueba_sel]
    id_prueba_activa = datos_prueba_activa.get("id_prueba") or datos_prueba_activa.get("id")
    
    df_notas = pd.DataFrame(notas_raw) if notas_raw else pd.DataFrame()
    
    if not df_notas.empty:
        df_notas.columns = [c.lower() for c in df_notas.columns]
        df_notas = df_notas[df_notas['id_prueba'] == id_prueba_activa]

    # =================================================================
    # 🗃️ PROCESAMIENTO BIÓNICO Y LIMPIEZA DEL PUENTE DE NOTAS
    # =================================================================
    df_informe_limpio = pd.DataFrame()
    conteo_niveles = {"Bajo (<60%)": 0, "Básico (60-79%)": 0, "Alto (80-89%)": 0, "Superior (≥90%)": 0}

    if not df_notas.empty:
        filas_limpias = []
        for _, fila in df_notas.iterrows():
            estudiante_str = str(buscar_campo(fila, 'estudiante', 'ALUMNO ANÓNIMO'))
            
            nombre_final = estudiante_str
            curso_final = "SIN CURSO"
            if "(" in estudiante_str and ")" in estudiante_str:
                parts = estudiante_str.split("(")
                nombre_final = parts[0].strip()
                curso_final = parts[1].replace(")", "").strip()

            raw_pct = buscar_campo(fila, 'porcentaje', 0.0)
            try: pct = float(raw_pct)
            except: pct = 0.0

            raw_nota = buscar_campo(fila, 'puntaje_obtenido', 0.0)
            try: nota = float(raw_nota)
            except: nota = 0.0

            raw_max_p = buscar_campo(fila, 'puntaje_maximo', 5.0)
            try: max_p = float(raw_max_p)
            except: max_p = 5.0
            
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
        
        if filas_limpias:
            df_informe_limpio = pd.DataFrame(filas_limpias).sort_values(by="ESTUDIANTE MATRÍCULA")

    # =================================================================
    # 📐 DISTRIBUCIÓN GRÁFICA Y BLOQUES DE DETALLE
    # =================================================================
    c1, c2 = st.columns([1, 1.2])
    
    with c1:
        st.markdown("### 📝 Detalles de Operación")
        
        max_p_display = float(buscar_campo(datos_prueba_activa, 'puntaje_maximo', 5.0))
        items_display = int(buscar_campo(datos_prueba_activa, 'total_preguntas', 10))

        tabla_detalles = pd.DataFrame({
            "Especificación": ["Examen Activo", "Asignatura", "Preguntas Totales", "Puntaje Máximo", "Último Escaneo"],
            "Detalle": [
                str(buscar_campo(datos_prueba_activa, 'nombre', 'EXAMEN')).upper(),
                str(buscar_campo(datos_prueba_activa, 'materia', 'MATERIA')).upper(),
                f"{items_display} Ítems",
                f"{max_p_display:.1f} Pts",
                "2026-06-16"
            ]
        })
        st.dataframe(tabla_detalles, use_container_width=True, hide_index=True)
        
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
            cx1.download_button("🟢 Excel", data=buffer_excel.getvalue(), file_name=f"REPORTE_{buscar_campo(datos_prueba_activa, 'nombre')}.xlsx", mime="application/vnd.ms-excel", use_container_width=True)
            cx2.download_button("📄 CSV", data=buffer_csv, file_name=f"REPORTE_{buscar_campo(datos_prueba_activa, 'nombre')}.csv", mime="text/csv", use_container_width=True)
            cx3.button("🚀 Migrar", type="secondary", disabled=True, use_container_width=True)
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
    # 📋 SECCIÓN INFERIOR: SABANA GENERAL DE NOTAS
    # =================================================================
    st.markdown("---")
    st.markdown("### 📋 Control de Asistencia y Sabana Escaneada")
    
    if not df_informe_limpio.empty:
        st.data_editor(df_informe_limpio, use_container_width=True, hide_index=True, disabled=True)
    else:
        st.info("💡 Consola Vacía: No se registran exámenes presentados para esta evaluación aún.")

if __name__ == "__main__":
    pass
