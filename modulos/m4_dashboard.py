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
# 👑 INTERFAZ CENTRAL: DASHBOARD DE CONTROL ANALÍTICO
# =================================================================
def ejecutar():
    st.markdown("""
        <style>
        .titulo-dash { color: #0d1b2a; font-family: 'Arial Black'; font-size: 34px; margin-bottom: 0px; }
        .subtitulo-dash { color: #d4af37; font-weight: bold; font-size: 13px; text-transform: uppercase; margin-top: 0px; }
        
        /* Contenedor HUD de Métricas VIP */
        .hud-dash {
            background: linear-gradient(135deg, #0d1b2a 0%, #1a365d 100%);
            border-left: 5px solid #d4af37; padding: 15px; border-radius: 8px; color: white;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.15); margin-bottom: 25px; display: flex;
            justify-content: space-between; align-items: center;
        }
        .hud-item { text-align: center; flex: 1; }
        .hud-title { font-size: 11px; font-weight: bold; color: #d4af37; text-transform: uppercase; margin:0; letter-spacing: 1px; }
        .hud-value { font-size: 24px; font-family: 'Arial Black'; margin: 5px 0 0 0; }
        
        /* Tablas e Inputs de Alto Contraste */
        .stSelectbox label p { color: #0d1b2a !important; font-weight: bold !important; text-transform: uppercase; }
        div[data-baseweb="select"] { color: #0d1b2a !important; font-weight: bold !important; }
        div[data-testid="stDataFrame"] { border: 2px solid #0d1b2a !important; border-radius: 6px; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<p class='titulo-dash'>📊 Centro de Control e Inteligencia Analítica</p>", unsafe_allow_html=True)
    st.markdown("<p class='subtitulo-dash'>Métricas Globales de Rendimiento, Sábanas Consolidadas y Curvas Estadísticas en Vivo</p>", unsafe_allow_html=True)
    st.markdown("---")

    try:
        supabase = iniciar_conexion()
    except Exception:
        st.error("🚨 Enlace satelital caído con el búnker de Supabase.")
        return

    # 📥 DESCARGA DE SÁBANAS CONFIGURADAS (Exámenes y Notas)
    with st.spinner("Sincronizando registros del búnker central..."):
        try:
            res_pruebas = supabase.table("pruebas_maestras").select("*").execute()
            pruebas = res_pruebas.data
            
            res_notas = supabase.table("respuestas_estudiantes").select("*").execute()
            notas_totales = res_notas.data
        except Exception as e:
            st.error(f"🚨 Falla en la extracción perimetral de datos: {e}")
            return

    if not pruebas:
        st.info("📭 No hay evaluaciones registradas en el sistema. Vaya al Módulo 2 para crear la primera.")
        return

    # Indexar exámenes por nombre comercial
    diccionario_pruebas = {f"{p.get('nombre', 'SIN NOMBRE')} - {p.get('materia', 'SIN MATERIA')}".upper(): p for p in pruebas}
    
    with st.container(border=True):
        st.markdown("### 🎯 Perímetro de Inspección")
        prueba_sel = st.selectbox("SELECCIONE LA EVALUACIÓN MÁSTER A AUDITAR:", list(diccionario_pruebas.keys()))
        datos_examen = diccionario_pruebas[prueba_sel]

    # Filtrar notas pertenecientes exclusivamente a este examen
    id_prueba_actual = datos_examen.get("id_prueba") or datos_examen.get("id")
    notas_filtradas = [n for n in notas_totales if str(n.get('id_prueba')) == str(id_prueba_actual)]

    if not notas_filtradas:
        st.warning("⚠️ Perímetro sin impactos: Ningún estudiante ha sido calificado aún para este examen (utilice el Escáner u OMR o Digitación Manual).")
        return

    # 📊 PROCESAMIENTO MATEMÁTICO DE DATOS (Pandas Core)
    df_notas = pd.DataFrame(notas_filtradas)
    df_notas['puntaje_obtenido'] = pd.to_numeric(df_notas['puntaje_obtenido'], errors='coerce')
    df_notas['porcentaje'] = pd.to_numeric(df_notas['porcentaje'], errors='coerce')
    df_notas['estudiante'] = df_notas['estudiante'].str.upper().str.strip()

    # Variables Estadísticas de Combate
    total_alumnos = len(df_notas)
    nota_maxima_examen = float(datos_examen.get('puntaje_maximo', 5.0))
    promedio_curso = df_notas['puntaje_obtenido'].mean()
    nota_mas_alta = df_notas['puntaje_obtenido'].max()
    
    # Cálculo de tasa de aprobación (Alumnos con rendimiento >= 60%)
    alumnos_aprobados = len(df_notas[df_notas['porcentaje'] >= 60.0])
    tasa_aprobacion = (alumnos_aprobados / total_alumnos) * 100 if total_alumnos > 0 else 0

    # =================================================================
    # 🏛️ DESPLIEGUE DEL HUD DE INTELIGENCIA MILITAR
    # =================================================================
    st.markdown(f"""
        <div class="hud-dash">
            <div class="hud-item">
                <p class="hud-title">Alumnos Evaluados</p>
                <p class="hud-value">📝 {total_alumnos} Alumnos</p>
            </div>
            <div class="hud-item" style="border-left: 2px solid rgba(255,255,255,0.1); border-right: 2px solid rgba(255,255,255,0.1);">
                <p class="hud-title">Promedio del Curso</p>
                <p class="hud-value">📉 {promedio_curso:.2f} / {nota_maxima_examen:.1f}</p>
            </div>
            <div class="hud-item" style="border-right: 2px solid rgba(255,255,255,0.1);">
                <p class="hud-title">Nota Más Alta</p>
                <p class="hud-value">🏆 {nota_mas_alta:.2f}</p>
            </div>
            <div class="hud-item">
                <p class="hud-title">Tasa de Aprobación</p>
                <p class="hud-value" style="color: {'#00ff66' if tasa_aprobacion >= 60 else '#ff3333'};">🔥 {tasa_aprobacion:.1f}%</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 🗂️ DIVISION DEL REPORTE EN PLATAFORMAS (TABS)
    t1, t2 = st.tabs(["📋 Sábana Consolidada de Notas", "📈 Curva de Distribución de Niveles"])

    # -----------------------------------------------------------------
    # TAB 1: SÁBANA CONSOLIDADA Y EXPORTACIÓN
    # -----------------------------------------------------------------
    with t1:
        st.markdown("#### 📋 Planilla Oficial de Calificaciones")
        st.info("💡 La siguiente tabla contiene los datos limpios indexados directamente desde el búnker de datos.")
        
        # Preparación de DataFrame Ejecutivo para visualización humana
        df_ejecutivo = df_notas[['estudiante', 'puntaje_obtenido', 'porcentaje']].copy()
        df_ejecutivo.columns = ['ESTUDIANTE / ALUMNO', 'NOTA OBTENIDA', 'RENDIMIENTO (%)']
        df_ejecutivo = df_ejecutivo.sort_values(by='ESTUDIANTE / ALUMNO').reset_index(drop=True)
        df_ejecutivo.index += 1 # Indexación amigable de 1 en adelante
        
        # Visor de Datos
        st.dataframe(df_ejecutivo, use_container_width=True)
        
        # ⚡ BOTÓN MAESTRO DE DESCARGA: Conversión a CSV compatible directo con Excel
        csv_buffer = df_ejecutivo.to_csv(index=False).encode('utf-8-sig') # utf-8-sig para que Excel respete tildes y Ñs
        
        st.download_button(
            label="📥 EXPORTAR PLANILLA MAESTRA A EXCEL (.CSV)",
            data=csv_buffer,
            file_name=f"NOTAS_{datos_examen.get('nombre','EXAMEN').replace(' ','_')}.csv",
            mime="text/csv",
            use_container_width=True
        )

    # -----------------------------------------------------------------
    # TAB 2: RENDIMIENTO ESTADÍSTICO VECTORIAL
    # -----------------------------------------------------------------
    with t2:
        st.markdown("#### 📈 Histograma de Densidad y Calificaciones")
        st.info("🤖 Esta gráfica clasifica a los estudiantes por rangos de rendimiento para identificar rápidamente baches de aprendizaje en el grupo.")
        
        try:
            # Segmentar los rendimientos en contenedores tácticos (Rangos de notas)
            intervalos = [0, 20, 40, 60, 80, 100]
            etiquetas = ['Crítico (0-20%)', 'Bajo (21-40%)', 'Aceptable (41-60%)', 'Sobresaliente (61-80%)', 'Excelente (81-100%)']
            
            df_notas['Rango'] = pd.cut(df_notas['porcentaje'], bins=intervalos, labels=etiquetas, include_lowest=True)
            distribucion = df_notas['Rango'].value_counts().reindex(etiquetas).fillna(0)
            
            # Gráfico de barras nativo Streamlit de alta velocidad
            df_grafico = pd.DataFrame({'Cantidad de Alumnos': distribucion})
            st.bar_chart(df_grafico, use_container_width=True)
            
            # Alerta analítica automatizada para el docente
            if tasa_aprobacion < 50.0:
                st.error(f"⚠️ **Alerta de Refuerzo:** Más de la mitad del curso se encuentra por debajo del umbral óptimo de aprobación. Se sugiere reprogramar competencias clave.")
            else:
                st.success(f"🎉 **Control de Perímetro Seguro:** El curso demuestra un ritmo de avance óptimo y dominancia temática.")
        except Exception as e:
            st.warning(f"Generando curva de nivel...: {e}")

if __name__ == "__main__":
    pass
