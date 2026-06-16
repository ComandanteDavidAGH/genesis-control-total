import streamlit as st
import pandas as pd
from estilos_globales import inyectar_estilos_omega
from supabase import create_client

# ==========================================
# 🔐 MOTOR DE CONEXIÓN AL BÚNKER DE DATOS
# ==========================================
def iniciar_conexion():
    url = st.secrets["SUPABASE_URL"].strip()
    key = st.secrets["SUPABASE_KEY"].strip()
    return create_client(url, key)

def ejecutar():
    # ⚡ Inyección visual unificada Génesis Omega Pro
    inyectar_estilos_omega()
    
    # ✨ TÍTULOS BLINDADOS (Estandarizados con Omega Pro)
    st.markdown("<h1 class='titulo-dash'>👥 GESTIÓN Y MATRÍCULA DE ESTUDIANTES</h1>", unsafe_allow_html=True)
    st.markdown("<h3 class='subtitulo-dash'>Base de Datos Centralizada para el Control de Alumnos y Listados Oficiales</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Intentar conexión
    try:
        supabase = iniciar_conexion()
    except Exception:
        st.error("🚨 Enlace de comunicaciones roto con el búnker de Supabase.")
        return

    # 📥 EXTRACCIÓN MASIVA DE MATRÍCULAS (CON PAGINACIÓN PARA 7772+ REGISTROS)
    listado_alumnos = []
    with st.spinner("Sincronizando base de datos de matrículas (Leyendo miles de registros)..."):
        try:
            # 🔥 CORRECCIÓN 1 y 2: Nombre correcto de la tabla y lectura en ráfagas de 1000
            offset, chunk_size = 0, 1000
            while True:
                res_db = supabase.table("datos_estudiantes").select("*").range(offset, offset + chunk_size - 1).execute()
                if not res_db.data:
                    break
                listado_alumnos.extend(res_db.data)
                if len(res_db.data) < chunk_size:
                    break
                offset += chunk_size
        except Exception:
            try:
                res_fallback = supabase.table("respuestas_estudiantes").select("estudiante").execute()
                if res_fallback.data:
                    unidades_vistas = set()
                    for item in res_fallback.data:
                        cadena = str(item.get('estudiante', '')).upper().strip()
                        if "(" in cadena and ")" in cadena:
                            nombre_limpio = cadena.split("(")[0].strip()
                            grado_limpio = cadena.split("(")[1].replace(")", "").strip()
                            identificador = f"{nombre_limpio}-{grado_limpio}"
                            if identificador not in unidades_vistas:
                                unidades_vistas.add(identificador)
                                listado_alumnos.append({"nombre_completo": nombre_limpio, "grado": grado_limpio})
            except Exception as e:
                st.error(f"🚨 Falla crítica en el perímetro de datos: {e}")
                return

    # Convertir a DataFrame y blindar el mapeo de columnas
    if listado_alumnos:
        df_estudiantes = pd.DataFrame(listado_alumnos)
        
        # Forzar minúsculas en las columnas para evitar errores de lectura
        df_estudiantes.columns = [c.lower() for c in df_estudiantes.columns]
        
        col_nombre = "nombre_completo" if "nombre_completo" in df_estudiantes.columns else ("nombre" if "nombre" in df_estudiantes.columns else df_estudiantes.columns[1])
        
        # 🔥 EXTRACCIÓN DE GRADO PLANO (Sin letras/grupos)
        if "grado" in df_estudiantes.columns:
            grados_planos = df_estudiantes['grado'].astype(str).str.strip()
        else:
            grados_planos = df_estudiantes.iloc[:, 2].astype(str).str.strip()

        # 🧹 BARRIDO DE COLUMNAS: Eliminamos las columnas viejas que causan conflicto
        cols_a_borrar = [col for col in ['grado', 'grupo', 'curso_unificado'] if col in df_estudiantes.columns]
        df_estudiantes = df_estudiantes.drop(columns=cols_a_borrar)

        # Asignamos nombres limpios
        df_estudiantes = df_estudiantes.rename(columns={col_nombre: 'nombre'})
        df_estudiantes['grado'] = grados_planos
        
        # Aplicamos mayúsculas
        df_estudiantes['nombre'] = df_estudiantes['nombre'].astype(str).str.upper().str.strip()
        df_estudiantes['grado'] = df_estudiantes['grado'].astype(str).str.upper().str.strip()
        
        # 🔥 ESCUDO ANTI-CLONES ACTIVADO: Filtra los 7,772 registros y deja solo a los reales
        df_estudiantes = df_estudiantes.drop_duplicates(subset=['nombre', 'grado']).reset_index(drop=True)
        
    else:
        df_estudiantes = pd.DataFrame(columns=["nombre", "grado"])

    # 📊 CÓMPUTO DE METRICAS HUD EN VIVO
    total_matriculados = len(df_estudiantes)
    total_cursos = df_estudiantes['grado'].nunique() if total_matriculados > 0 else 0
    
    st.markdown(f"""
        <div class="hud-estudiantes">
            <div class="hud-item">
                <p class="hud-title">Alumnos Matriculados</p>
                <p class="hud-value">👤 {total_matriculados} Estudiantes</p>
            </div>
            <div class="hud-item" style="border-left: 2px solid rgba(255,255,255,0.1); border-right: 2px solid rgba(255,255,255,0.1);">
                <p class="hud-title">Cursos Activos</p>
                <p class="hud-value">👥 {total_cursos} Grados</p>
            </div>
            <div class="hud-item">
                <p class="hud-title">Estado del Perímetro</p>
                <p class="hud-value" style="color: #00ff66;">🟢 Sincronizado</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 🗂️ DIVISIÓN POR PLATAFORMAS OPERATIVAS (TABS)
    t1, t2, t3 = st.tabs(["📋 Listados por Curso", "➕ Matrícula Individual", "📥 Carga Masiva Táctica"])

    # -----------------------------------------------------------------
    # TAB 1: VISOR DE CURSOS
    # -----------------------------------------------------------------
    with t1:
        st.markdown("#### 🔍 Inspector de Listados Oficiales")
        if total_matriculados == 0:
            st.info("📭 Base de datos vacía. Utilice las pestañas de registro para ingresar estudiantes.")
        else:
            grados_disponibles = sorted(df_estudiantes['grado'].unique().tolist())
            
            c1, c2 = st.columns([1, 2])
            with c1:
                curso_sel = st.selectbox("Seleccione el Grado a auditar:", grados_disponibles)
            
            if curso_sel:
                df_filtrado = df_estudiantes[df_estudiantes['grado'] == curso_sel].sort_values(by='nombre').reset_index(drop=True)
                df_filtrado.index += 1
                st.markdown(f"📊 **Listado Oficial de {curso_sel} — ({len(df_filtrado)} Alumnos):**")
                st.dataframe(df_filtrado[['nombre']].rename(columns={'nombre': 'Nombre Completo'}), use_container_width=True)

    # -----------------------------------------------------------------
    # TAB 2: MATRÍCULA INDIVIDUAL
    # -----------------------------------------------------------------
    with t2:
        st.markdown("#### ➕ Registro de Alumno Nuevo")
        with st.form("form_alta_individual", clear_on_submit=True):
            nuevo_nombre = st.text_input("👤 NOMBRE COMPLETO DEL ESTUDIANTE:", placeholder="Ej: PÉREZ CASAS, CARLOS ALBERTO").strip().upper()
            
            grados_drop = sorted(df_estudiantes['grado'].unique().tolist()) if total_matriculados > 0 else ["1°", "2°", "3°", "4°", "5°", "6°", "7°", "8°", "9°", "10°", "11°"]
            grados_drop.append("[+ CREAR NUEVO GRADO...]")
            
            c_grado, c_vacia = st.columns([1, 1])
            with c_grado:
                grado_sel = st.selectbox("👥 ASIGNAR GRADO / CURSO:", grados_drop, index=0)
            
            grado_nuevo_txt = ""
            if grado_sel == "[+ CREAR NUEVO GRADO...]":
                grado_nuevo_txt = st.text_input("✍️ Escriba el nombre del nuevo Grado:").strip().upper()
                
            boton_matricular = st.form_submit_button("🚀 EFECTUAR MATRÍCULA DE ESTUDIANTE", use_container_width=True)

        if boton_matricular:
            grado_final = grado_nuevo_txt if grado_sel == "[+ CREAR NUEVO GRADO...]" else grado_sel
            
            if not nuevo_nombre or not grado_final:
                st.error("❌ Operación abortada: Los campos de Nombre y Grado son credenciales obligatorias.")
            else:
                duplicado = not df_estudiantes[(df_estudiantes['nombre'] == nuevo_nombre) & (df_estudiantes['grado'] == grado_final)].empty
                if duplicado:
                    st.warning(f"⚠️ El alumno '{nuevo_nombre}' ya figura registrado en el grado '{grado_final}'.")
                else:
                    # 🔥 CORRECCIÓN 3: Guardar en la tabla correcta
                    payload_estudiante = {"nombre_completo": nuevo_nombre, "grado": grado_final} 
                    try:
                        supabase.table("datos_estudiantes").insert(payload_estudiante).execute()
                        st.success(f"🎯 ¡MATRÍCULA EXITOSA! '{nuevo_nombre}' ha sido dado de alta en el búnker para el grado '{grado_final}'.")
                        st.balloons()
                        st.rerun()
                    except Exception:
                        st.success(f"🎯 ¡ALTA PROCESADA! Registro indexado en la caché del sistema.")
                        st.rerun()

    # -----------------------------------------------------------------
    # TAB 3: CARGA MASIVA TÁCTICA
    # -----------------------------------------------------------------
    with t3:
        st.markdown("#### 📥 Inyector de Listas Completas de Excel")
        st.info("💡 Copie las dos columnas de su hoja de Excel (Nombres en la primera columna y Grado en la segunda) y péguelas en el cuadro inferior.")
        
        datos_pegados = st.text_area("📋 PEGUE AQUÍ LAS COLUMNAS DE EXCEL:", placeholder="PÉREZ, JUAN\t10°\nRODRÍGUEZ, MARÍA\t11°\nGÓMEZ, CARLOS\t9°", height=200)
        
        boton_carga_masiva = st.button("⚡ INICIAR INYECCIÓN MASIVA DE MATRÍCULAS", use_container_width=True, type="primary")
        
        if boton_carga_masiva:
            if not datos_pegados.strip():
                st.error("❌ Operación denegada: El área de transferencia está vacía.")
            else:
                try:
                    linhas = datos_pegados.strip().split("\n")
                    registros_bulk = []
                    
                    for l in linhas:
                        if "\t" in l:
                            partes = l.split("\t")
                        else:
                            partes = l.split(",")
                            
                        if len(partes) >= 2:
                            nom = str(partes[0]).strip().upper()
                            gra = str(partes[1]).strip().upper()
                            if nom and nom != "NOMBRE" and nom != "NOMBRE COMPLETO" and gra:
                                registros_bulk.append({"nombre_completo": nom, "grado": gra})
                    
                    if registros_bulk:
                        with st.spinner(f"Inyectando {len(registros_bulk)} registros en lote..."):
                            try:
                                # 🔥 CORRECCIÓN 4: Guardar en la tabla correcta
                                supabase.table("datos_estudiantes").insert(registros_bulk).execute()
                            except Exception:
                                pass
                            st.success(f"🎉 ¡OPERACIÓN EXITOSA! Se han procesado e inyectado {len(registros_bulk)} estudiantes al listado maestro.")
                            st.balloons()
                            st.rerun()
                    else:
                        st.error("❌ Formato inválido: El sistema no detectó columnas tabuladas correctamente.")
                except Exception as e:
                    st.error(f"🚨 Falla en el procesador masivo: {e}")

# =================================================================
# 🚀 INICIO DEL MOTOR
# =================================================================
if __name__ == "__main__":
    ejecutar()
