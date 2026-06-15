import streamlit as st
import pandas as pd
from supabase import create_client, Client

# =================================================================
# 🔒 CONEXIÓN SEGURA CON EL BÚNKER DE PRODUCCIÓN
# =================================================================
def iniciar_conexion():
    url = st.secrets["SUPABASE_URL"].strip()
    key = st.secrets["SUPABASE_KEY"].strip()
    return create_client(url, key)

def ejecutar():
    # 🎨 INYECCIÓN DE ALTA INGENIERÍA VISUAL (GÉNESIS ANALYTICS HUD) - Respetado al 100%
    st.markdown("""
        <style>
        .titulo-genesis {
            color: #0d1b2a;
            font-family: 'Arial Black', sans-serif;
            font-size: 32px;
            margin-bottom: 0px;
        }
        .subtitulo-genesis {
            color: #d4af37;
            font-weight: bold;
            font-size: 13px;
            margin-top: -5px;
            letter-spacing: 1.5px;
            text-transform: uppercase;
        }
        
        .hud-container {
            display: flex;
            gap: 15px;
            margin-bottom: 25px;
            margin-top: 15px;
        }
        .hud-card {
            flex: 1;
            background: #ffffff;
            border-top: 3px solid #0d1b2a;
            border-radius: 4px 4px 12px 12px;
            padding: 12px 15px;
            text-align: center;
            box-shadow: 0 10px 25px rgba(13, 27, 42, 0.04);
            transition: all 0.2s ease;
        }
        .hud-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 12px 30px rgba(212, 175, 55, 0.12);
        }
        .hud-label {
            font-size: 11px;
            font-weight: 800;
            color: #5c677d;
            letter-spacing: 1px;
            text-transform: uppercase;
            margin-bottom: 4px;
        }
        .hud-value {
            font-size: 32px;
            font-family: 'Arial Black', sans-serif;
            font-weight: 900;
            line-height: 1;
            color: #0d1b2a;
        }
        
        .contenedor-matriz {
            background-color: #ffffff;
            border-radius: 12px;
            border: 1px solid #e5e5e5;
            border-top: 4px solid #0d1b2a;
            padding: 20px;
            box-shadow: 0 8px 30px rgba(0,0,0,0.02);
            margin-top: 20px;
        }
        /* Estilos adicionales para los componentes funcionales */
        div[data-baseweb="select"] {
            border-radius: 8px !important;
            border: 1px solid #d4af37 !important;
        }
        div[data-testid="stDataFrame"] {
            border: 1px solid #e5e5e5;
            border-radius: 8px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<p class='titulo-genesis'>📊 Panel del Cuestionario y Analítica</p>", unsafe_allow_html=True)
    st.markdown("<p class='subtitulo-genesis'>Ecosistema Centralizado de Control de Evaluaciones e Inteligencia Académica</p>", unsafe_allow_html=True)
    st.markdown("---")

    # Pestañas institucionales limpias - Respetadas
    tab1, tab2 = st.tabs(["📊 Analítica General", "📂 Consolidación por Período (Migrar)"])

    with tab1:
        try:
            supabase = iniciar_conexion()
            
            with st.spinner("Sincronizando telemetría de alto nivel..."):
                # =================================================================
                # 📡 LÓGICA DE DATOS INYECTADA (Invisible y Segura)
                # =================================================================
                
                # 1. Alumnos: Se mantiene la lógica del extractor corregido del original
                estudiantes_base = []
                offset = 0
                chunk_size = 1000  
                while True:
                    # Usamos 'data_estudiantes' como en tu original corregido
                    resultado = supabase.table("data_estudiantes").select('ID_Estudiante').range(offset, offset + chunk_size - 1).execute()
                    if not resultado.data: break
                    estudiantes_base.extend(resultado.data)
                    if len(resultado.data) < chunk_size: break
                    offset += chunk_size  

                total_alumnos = len(pd.DataFrame(estudiantes_base).drop_duplicates(subset=["ID_Estudiante"])) if estudiantes_base else 0

                # 2. Exámenes: Traemos las pruebas máster
                res_pruebas = supabase.table("pruebas_maestras").select("*").execute()
                pruebas = res_pruebas.data

                # 3. Notas: Traemos las calificaciones consolidadas
                res_notas = supabase.table("respuestas_estudiantes").select("*").execute()
                notas_totales = res_notas.data

            if pruebas and notas_totales:
                # Perímetro de selección funcional insertado discretamente
                diccionario_pruebas = {f"{p.get('nombre', 'SIN NOMBRE')} - {p.get('materia', 'SIN MATERIA')}".upper(): p for p in pruebas}
                
                st.markdown("### 📋 Selección de Evaluación")
                prueba_sel = st.selectbox("Elija la evaluación para proyectar la analítica:", list(diccionario_pruebas.keys()), label_visibility="collapsed")
                datos_examen = diccionario_pruebas[prueba_sel]

                # =================================================================
                # 🏥 CIRUGÍA LÁSER: BLINDAJE ANTI-NONETYPE (null en Supabase)
                # =================================================================
                # Donde tu app se estallaba: float(None).
                # Ahora usamos Try/Except para capturar celdas vacías y asignar 5.0 por defecto.
                raw_puntaje_maximo = datos_examen.get('puntaje_maximo')
                try:
                    nota_maxima_examen = float(raw_puntaje_maximo) if raw_puntaje_maximo is not None else 5.0
                except (ValueError, TypeError):
                    nota_maxima_examen = 5.0

                # Filtrar notas para alimentar los valores fijos del HUD
                id_prueba_actual = datos_examen.get("id_prueba") or datos_examen.get("id")
                notas_filtradas = [n for n in notas_totales if str(n.get('id_prueba')) == str(id_prueba_actual)]
                
                evaluaciones_procesadas = len(notas_filtradas)

                # Calcular Efectividad Institucional real (Alumnos >= 60%)
                if evaluaciones_procesadas > 0:
                    df_filtrado = pd.DataFrame(notas_filtradas)
                    # Conversión segura a numérico de porcentajes
                    df_filtrado['porcentaje'] = pd.to_numeric(df_filtrado['porcentaje'], errors='coerce').fillna(0)
                    alumnos_aprobados = len(df_filtrado[df_filtrado['porcentaje'] >= 60.0])
                    efectividad_real = (alumnos_aprobados / evaluaciones_procesadas) * 100
                else:
                    efectividad_real = 0

                # =================================================================
                # 🏗️ RESTAURACIÓN DEL HUD ORIGINAL CON DATOS EN VIVO
                # =================================================================
                st.markdown(f"""
                    <div class="hud-container">
                        <div class="hud-card" style="border-top-color: #0d1b2a;">
                            <div class="hud-label">👥 AUDITORÍA DE ALUMNOS</div>
                            <div class="hud-value" style="color: #0d1b2a;">{total_alumnos}</div>
                        </div>
                        <div class="hud-card" style="border-top-color: #d4af37;">
                            <div class="hud-label" style="color: #bfa12a;">📝 EVALUACIONES PROCESADAS</div>
                            <div class="hud-value" style="color: #d4af37;">{evaluaciones_procesadas}</div>
                        </div>
                        <div class="hud-card" style="border-top-color: #2b9348;">
                            <div class="hud-label" style="color: #2b9348;">📈 EFECTIVIDAD INSTITUCIONAL</div>
                            <div class="hud-value" style="color: #2b9348;">{efectividad_real:.0f}%</div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

                # Cápsula de despliegue informativo - Respetada
                st.markdown("""
                    <div class="contenedor-matriz">
                        <h4 style="color: #0d1b2a; font-weight: bold; margin-top: 0px; margin-bottom: 10px;">📊 Distribución del Rendimiento del Cuestionario</h4>
                        <p style="color: #666; font-size: 13px; margin-bottom: 15px;">Métricas consolidadas listas para el procesamiento de promedios.</p>
                    </div>
                """, unsafe_allow_html=True)
                
                # Sábana Consolidada Funcional insertada al final para la exportación
                with st.expander("📊 Ver Planilla Consolidada y Exportar a Excel"):
                    if evaluaciones_procesadas > 0:
                        df_ejecutivo = pd.DataFrame(notas_filtradas)[['estudiante', 'puntaje_obtenido', 'porcentaje']]
                        df_ejecutivo.columns = ['ALUMNO', 'NOTA', 'RENDIMIENTO (%)']
                        st.dataframe(df_ejecutivo.sort_values(by='ALUMNO'), use_container_width=True, hide_index=True)
                        
                        csv_buffer = df_ejecutivo.to_csv(index=False).encode('utf-8-sig')
                        st.download_button(label="📥 Descargar Planilla Mástra a Excel", data=csv_buffer, file_name=f"Notas_{datos_examen.get('nombre','Examen').replace(' ','_')}.csv", mime="text/csv", use_container_width=True)
                    else:
                        st.caption("No hay calificaciones registradas para esta prueba.")

            else:
                st.warning("⚠️ No se detectaron evaluaciones o notas suficientes para estructurar las analíticas.")
        
        except Exception as e:
            st.error(f"🚨 Error general en tab1: {e}")

if __name__ == "__main__":
    pass
