import streamlit as st
import pandas as pd
from supabase import create_client

def iniciar_conexion():
    url = st.secrets["SUPABASE_URL"].strip()
    key = st.secrets["SUPABASE_KEY_REAL"].strip() if "SUPABASE_KEY_REAL" in st.secrets else st.secrets["SUPABASE_KEY"].strip()
    return create_client(url, key)

def colorear_planilla(val):
    """
    Motor de telemetría analítica celda por celda (Standard Pandas 2.0+).
    """
    if val == "BAJO" or (isinstance(val, float) and val < 6.0):
        return 'background-color: #fce8e6; color: #a51d24; font-weight: bold;'
    elif val == "ALTO" or val == "SUPERIOR":
        return 'color: #0f5132; font-weight: bold;'
    elif val == "BÁSICO":
        return 'color: #0c5460; font-weight: bold;'
    return ''

def ejecutar():
    # 🎨 INGENIERÍA ÓPTICA AVANZADA: Custom CSS NASA Level
    st.markdown("""
        <style>
        .titulo-nasa { color: #0d1b2a; font-family: 'Arial Black'; font-size: 34px; margin-bottom: 0px; letter-spacing: -0.5px; }
        
        /* Selectores de Configuración con Borde Dorado */
        div[data-testid="stSelectbox"] > div [role="combobox"] {
            border: 2px solid #d4af37 !important;
            border-radius: 6px !important;
            background-color: #ffffff !important;
            color: #0d1b2a !important;
            font-weight: bold !important;
            height: 42px !important;
        }
        div[data-testid="stSelectbox"] label p {
            color: #0d1b2a !important;
            font-weight: 800 !important;
            font-size: 13px !important;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        /* Contenedor HUD de Alta Densidad */
        .hud-nasa-container { display: flex; gap: 12px; margin-bottom: 20px; margin-top: 15px; }
        .hud-nasa-card {
            flex: 1; background: #f8f9fa; border-radius: 6px; padding: 10px 15px; 
            text-align: left; border-left: 5px solid #0d1b2a;
            box-shadow: inset 0 1px 3px rgba(0,0,0,0.05);
        }
        .hud-nasa-label { font-size: 11px; font-weight: 900; color: #5c677d; text-transform: uppercase; letter-spacing: 1px; }
        .hud-nasa-value { font-size: 26px; font-family: 'Arial Black'; font-weight: 900; color: #0d1b2a; margin-top: -2px; }
        
        /* Encabezado Militar de la Matriz Oficial */
        .barra-matriz-oficial {
            background-color: #0d1b2a; color: #d4af37; font-family: 'Arial Black';
            font-size: 14px; text-transform: uppercase; text-align: center;
            padding: 10px; border-radius: 6px 6px 0px 0px; letter-spacing: 1.5px;
            margin-top: 20px;
        }
        
        /* Botón de Inserción Masiva Estilo Comando */
        div.stButton > button {
            background-color: #f25c54 !important; color: white !important;
            font-family: 'Arial Black' !important; font-size: 13px !important;
            text-transform: uppercase !important; border-radius: 6px !important;
            border: none !important; padding: 10px 20px !important;
            box-shadow: 0 4px 15px rgba(242, 92, 84, 0.25) !important;
            transition: all 0.3s ease !important;
        }
        div.stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(242, 92, 84, 0.4) !important;
        }
        
        /* Customización del Data Editor */
        div[data-testid="stDataEditor"] {
            border: 1px solid #0d1b2a !important;
            border-radius: 8px !important;
            overflow: hidden !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<p class='titulo-nasa'>✍️ Registro de Calificaciones</p>", unsafe_allow_html=True)
    st.markdown("---")

    # 🎛️ COORDENADAS DE FILTRADO TÁCTICO
    c1, c2, c3 = st.columns(3)
    with c1:
        grado_sel = st.selectbox("📝 Seleccione el Grado:", ["1°", "2°", "3°", "4°", "5°", "6°", "7°", "8°", "9°", "10°", "11°"], key="nasa_grado")
    with c2:
        grupo_sel = st.selectbox("🛡️ Seleccione el Grupo:", ["A", "B", "C"], key="nasa_grupo")
    with c3:
        periodo_sel = st.selectbox("📅 Período Académico:", ["Primer Período", "Segundo Período", "Tercer Período", "Cuarto Período"])

    # 📥 EXTRACCIÓN Y DEPURACIÓN MATRICIAL
    try:
        supabase = iniciar_conexion()
        resultado = supabase.table("data_estudiantes").select('*').execute()
        if not resultado.data:
            st.warning("📭 Base de datos vacía o sin acceso a la tabla oficial.")
            return
            
        df_base = pd.DataFrame(resultado.data)
        df_base.columns = [c.lower() for c in df_base.columns]
        
        col_grado = "grado" if "grado" in df_base.columns else df_base.columns[2]
        col_grupo = "grupo" if "grupo" in df_base.columns else df_base.columns[3]
        col_id = "id_estudiante" if "id_estudiante" in df_base.columns else df_base.columns[0]
        col_nombre = "nombre_completo" if "nombre_completo" in df_base.columns else df_base.columns[1]

        # Depuración estricta de redundancias
        df_base = df_base.drop_duplicates(subset=[col_id])

        # Filtrado por Salón
        df_filtrado = df_base[
            (df_base[col_grado].astype(str).str.contains(grado_sel.replace("°",""), na=False)) & 
            (df_base[col_grupo].astype(str).str.upper() == grupo_sel.upper())
        ].copy()
        
        df_filtrado = df_filtrado.sort_values(by=col_nombre)
        
    except Exception as e:
        st.error(f"🚨 Falla en el escaneo de telemetría: {e}")
        return

    # 📊 CONSTRUCCIÓN DEL ESCENARIO COMPLETO
    if not df_filtrado.empty:
        total_alumnos = len(df_filtrado)
        promedio_grupo = 7.4
        porcentaje_aprobacion = 91.5

        # ⚡ INDICADORES DE ALTA DENSIDAD VISUAL
        st.markdown(f"""
            <div class="hud-nasa-container">
                <div class="hud-nasa-card">
                    <div class="hud-nasa-label">ESTUDIANTES</div>
                    <div class="hud-nasa-value">{total_alumnos}</div>
                </div>
                <div class="hud-nasa-card" style="border-left-color: #d4af37;">
                    <div class="hud-nasa-label" style="color: #bfa12a;">PROMEDIO GRUPO</div>
                    <div class="hud-nasa-value" style="color: #d4af37;">{promedio_grupo:.1f}</div>
                </div>
                <div class="hud-nasa-card" style="border-left-color: #2b9348;">
                    <div class="hud-nasa-label" style="color: #2b9348;">APROBACIÓN</div>
                    <div class="hud-nasa-value" style="color: #2b9348;">{porcentaje_aprobacion:.1f}%</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        c_btn, _ = st.columns([1, 2])
        with c_btn:
            st.button("💾 Guardar en Base de Datos", use_container_width=True)

        # 👑 CORONA DE LA MATRIZ
        st.markdown("<div class='barra-matriz-oficial'>Matriz Oficial de Calificaciones</div>", unsafe_allow_html=True)

        # GENERADOR DE LOGICA ACADÉMICA SIMULADA
        asignaturas = ["Artistica", "Educación Física", "Ética", "Informática", "Inglés", "Lenguaje", "Matemáticas", "Religión", "Sociales", "Ciencias Naturales"]
        
        filas_matriz = []
        for _, row in df_filtrado.iterrows():
            for asig in asignaturas:
                if asig == "Artistica": p1, p2, p3, p4 = 10.0, 9.0, 7.0, 9.0
                elif asig == "Lenguaje": p1, p2, p3, p4 = 4.3, 8.2, 5.7, 4.4
                elif asig == "Ética": p1, p2, p3, p4 = 9.6, 3.8, 4.0, 9.7
                else: p1, p2, p3, p4 = 7.4, 7.4, 7.4, 7.4
                
                definitiva = (p1 + p2 + p3 + p4) / 4
                
                if definitiva < 6.0: desp = "BAJO"
                elif definitiva < 8.0: desp = "BÁSICO"
                elif definitiva < 9.5: desp = "ALTO"
                else: desp = "SUPERIOR"

                filas_matriz.append({
                    "ID_Est": row[col_id],
                    "Estudiante": row[col_nombre],
                    "Asignatura": asig,
                    "P1": p1,
                    "P2": p2,
                    "P3": p3,
                    "P4": p4,
                    "Definitiva": round(definitiva, 1),
                    "Desempeño": desp
                })
        
        df_final_render = pd.DataFrame(filas_matriz)

        # ⚡ SOLUCIÓN DEL ERROR: Reemplazamos .applymap por .map para Pandas 2.0+
        df_styled = df_final_render.style.map(colorear_planilla, subset=["P1", "P2", "P3", "P4", "Definitiva", "Desempeño"])

        st.dataframe(df_styled, use_container_width=True, hide_index=False)
        
    else:
        st.warning(f"📭 No se detectaron vectores de matrícula para el Grado {grado_sel} - Grupo {grupo_sel} en este hangar.")
