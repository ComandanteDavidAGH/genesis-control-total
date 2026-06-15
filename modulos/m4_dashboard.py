import streamlit as st
import pandas as pd
from supabase import create_client

def iniciar_conexion():
    url = st.secrets["SUPABASE_URL"].strip()
    key = st.secrets["SUPABASE_KEY_REAL"].strip() if "SUPABASE_KEY_REAL" in st.secrets else st.secrets["SUPABASE_KEY"].strip()
    return create_client(url, key)

def ejecutar():
    # 🎨 INGENIERÍA ÓPTICA AVANZADA: CSS de Alto Impacto para Visualización de Datos
    st.markdown("""
        <style>
        .titulo-nasa { color: #0d1b2a; font-family: 'Arial Black'; font-size: 34px; margin-bottom: 0px; letter-spacing: -0.5px; }
        .subtitulo-nasa { color: #d4af37; font-weight: bold; font-size: 13px; text-transform: uppercase; margin-top: 0px; letter-spacing: 0.5px; }
        
        /* FIX DE ALTO CONTRASTE: Forzamos nitidez absoluta en las pestañas */
        button[data-baseweb="tab"] p {
            color: #0d1b2a !important; font-weight: 800 !important; text-transform: uppercase; font-size: 12px !important;
        }
        
        /* HUD Cards Estilo Central de Mando */
        .hud-nasa-container { display: flex; gap: 12px; margin-bottom: 25px; margin-top: 15px; }
        .hud-nasa-card {
            flex: 1; background: #f8f9fa; border-radius: 6px; padding: 10px 15px; 
            text-align: left; border-left: 5px solid #0d1b2a;
            box-shadow: inset 0 1px 3px rgba(0,0,0,0.05);
        }
        .hud-nasa-label { font-size: 11px; font-weight: 900; color: #5c677d; text-transform: uppercase; letter-spacing: 1px; }
        .hud-nasa-value { font-size: 26px; font-family: 'Arial Black'; font-weight: 900; color: #0d1b2a; margin-top: -2px; }
        
        /* Cinturones Oscuros Corporativos */
        .barra-matriz-oficial {
            background-color: #0d1b2a; color: #d4af37; font-family: 'Arial Black';
            font-size: 14px; text-transform: uppercase; text-align: center;
            padding: 10px; border-radius: 6px 6px 0px 0px; letter-spacing: 1.5px;
            margin-top: 20px; margin-bottom: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<p class='titulo-nasa'>📊 Panel del Cuestionario y Analítica</p>", unsafe_allow_html=True)
    st.markdown("<p class='subtitulo-nasa'>Ecosistema de Inteligencia Académica Institucional</p>", unsafe_allow_html=True)
    st.markdown("---")

    # 📥 EXTRACCIÓN MAESTRA DE DATOS DE AMBAS TABLAS (ANTI-TRUNCAMIENTO)
    estudiantes_base = []
    pruebas_disponibles = []
    
    try:
        supabase = iniciar_conexion()
        
        # Paginación masiva de matrícula
        offset, chunk_size = 0, 1000
        while True:
            resultado_est = supabase.table("data_estudiantes").select('*').range(offset, offset + chunk_size - 1).execute()
            if not resultado_est.data: break
            estudiantes_base.extend(resultado_est.data)
            if len(resultado_est.data) < chunk_size: break
            offset += chunk_size

        # Carga del banco de pruebas
        resultado_pruebas = supabase.table("pruebas_maestras").select("*").execute()
        pruebas_disponibles = resultado_pruebas.data
    except Exception as e:
        st.error(f"🚨 Falla en la sincronización de analítica con Supabase: {e}")
        return

    # Proceso lógico de dataframes limpios
    df_est = pd.DataFrame(estudiantes_base) if estudiantes_base else pd.DataFrame()
    df_pru = pd.DataFrame(pruebas_disponibles) if pruebas_disponibles else pd.DataFrame()

    if not df_est.empty:
        df_est.columns = [c.lower() for c in df_est.columns]
        col_id = "id_estudiante" if "id_estudiante" in df_est.columns else df_est.columns[0]
        col_grado = "grado" if "grado" in df_est.columns else df_est.columns[2]
        col_grupo = "grupo" if "grupo" in df_est.columns else df_est.columns[3]
        df_est_limpio = df_est.drop_duplicates(subset=[col_id])
        total_alumnos = len(df_est_limpio)
    else:
        total_alumnos = 0

    total_pruebas = len(df_pru)

    # 🗺️ DIVISION ESTRUCTURAL POR PESTAÑAS (TABS OFICIALES)
    tab_general, tab_periodo = st.tabs(["📁 Analítica General", "📅 Consolidación por Período"])

    with tab_general:
        # 📊 MONITOR DE TELEMETRÍA DINÁMICO
        st.markdown(f"""
            <div class="hud-nasa-container">
                <div class="hud-nasa-card">
                    <div class="hud-nasa-label">👥 AUDITORÍA DE ALUMNOS</div>
                    <div class="hud-nasa-value">{total_alumnos}</div>
                </div>
                <div class="hud-nasa-card" style="border-left-color: #d4af37;">
                    <div class="hud-nasa-label" style="color: #bfa12a;">📝 EVALUACIONES PROCESADAS</div>
                    <div class="hud-nasa-value" style="color: #d4af37;">{total_pruebas}</div>
                </div>
                <div class="hud-nasa-card" style="border-left-color: #2b9348;">
                    <div class="hud-nasa-label" style="color: #2b9348;">📈 EFECTIVIDAD INSTITUCIONAL</div>
                    <div class="hud-nasa-value" style="color: #2b9348;">100%</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # 📊 SECCIÓN 1: GRÁFICO DE DISTRIBUCIÓN ESCOLAR
        st.markdown("<div class='barra-matriz-oficial'>📊 Distribución Masiva de Matrícula por Grado</div>", unsafe_allow_html=True)
        
        if not df_est.empty:
            # Conteo de alumnos reales agrupados por Grado
            df_chart = df_est_limpio[col_grado].value_counts().reset_index()
            df_chart.columns = ["Grado Académico", "Número de Alumnos"]
            df_chart = df_chart.set_index("Grado Académico")
            
            # Despliegue del gráfico de barras nativo de alta gama
            st.bar_chart(df_chart, use_container_width=True)
        else:
            st.info("📌 En espera de vectores de matrícula escolar para graficar.")

        # 📋 SECCIÓN 2: INVENTARIO DEL BANCO DE PRUEBAS
        st.markdown("<div class='barra-matriz-oficial'>🗃️ Inventario de Evaluaciones Activas en el Banco</div>", unsafe_allow_html=True)
        if not df_pru.empty:
            df_pru_visual = df_pru.copy()
            # Mapeo limpio para visualización ejecutiva
            mapeo_pru = {"id": "ID", "nombre": "Nombre de la Prueba", "materia": "Asignatura", "total_preguntas": "Ítems Evaluados", "llave_maestra": "Llave de Respuestas"}
            df_pru_visual = df_pru_visual.rename(columns=mapeo_pru)
            cols_pru = [c for c in mapeo_pru.values() if c in df_pru_visual.columns]
            
            st.dataframe(df_pru_visual[cols_pru], use_container_width=True, hide_index=True)
        else:
            st.info("💡 No se detectan evaluaciones guardadas. Crea tu primera prueba en el Módulo 1 para poblar este inventario.")

    with tab_periodo:
        # 📊 MONITOR DE TELEMETRÍA SECUNDARIO
        st.markdown(f"""
            <div class="hud-nasa-container">
                <div class="hud-nasa-card">
                    <div class="hud-nasa-label">📅 PERÍODO ACADÉMICO ACTIVO</div>
                    <div class="hud-nasa-value" style="font-size:20px; margin-top:5px; font-family:'Arial';">PRIMER PERÍODO</div>
                </div>
                <div class="hud-nasa-card" style="border-left-color: #d4af37;">
                    <div class="hud-nasa-label" style="color: #bfa12a;">🎯 PROYECCIÓN DE COBERTURA</div>
                    <div class="hud-nasa-value" style="color: #d4af37;">95.0%</div>
                </div>
                <div class="hud-nasa-card" style="border-left-color: #2b9348;">
                    <div class="hud-nasa-label" style="color: #2b9348;">🚀 ESTADO DEL PROCESAMIENTO</div>
                    <div class="hud-nasa-value" style="color: #2b9348; font-size:20px; margin-top:5px; font-family:'Arial';">ÓPTIMO ✔️</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<div class='barra-matriz-oficial'>📈 Consolidado Histórico Institucional y Metas Académicas</div>", unsafe_allow_html=True)
        
        # Estructura simulada de KPIs institucionales para auditoría ejecutiva de rectores
        data_periodos = pd.DataFrame({
            "Período Evaluativo": ["Primer Período", "Segundo Período", "Tercer Período", "Cuarto Período"],
            "Meta Promedio Esperada": [3.8, 4.0, 4.0, 4.2],
            "Tasa de Aprobación Objetivo": ["85.0%", "90.0%", "92.0%", "95.0%"],
            "Estado de Almacenamiento": ["Procesando...", "Bloqueado", "Bloqueado", "Bloqueado"]
        })
        
        st.dataframe(data_periodos, use_container_width=True, hide_index=True)
