import streamlit as st

def inyectar_estilos_omega():
    """
    Inyecta la matriz estética unificada de Génesis Omega Pro.
    Controla títulos, contornos de tablas, colores de fuentes y bordes de alta definición.
    """
    st.markdown("""
        <style>
        /* =================================================================
           🎨 1. CORE DE COLORES Y FUENTES GENERALES (Alto Contraste)
           ================================================================= */
        html, body, [data-testid="stAppViewContainer"] {
            color: #0d1b2a !important;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        /* Forzar que todos los textos de párrafos y bloques tengan tipografía nítida */
        p, span, li, div {
            color: #0d1b2a !important;
        }

        /* Labels y etiquetas de los campos en negro puro y negrita */
        div[data-testid="stMainBlockContainer"] label p {
            color: #0d1b2a !important;
            font-weight: 800 !important;
            font-size: 13px !important;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        /* =================================================================
           🏛️ 2. ARQUITECTURA DE TITULOS CON LÍNEA DORADA INSTITUCIONAL
           ================================================================= */
        h1, .titulo-nasa {
            color: #0d1b2a !important;
            font-family: 'Arial Black', sans-serif !important;
            font-size: 34px !important;
            font-weight: 900 !important;
            margin-bottom: 5px !important;
            text-transform: uppercase !important;
        }

        /* Inyección automática de la línea dorada debajo de los títulos principales */
        div[data-testid="stHeader"] + div, h1, .titulo-nasa {
            border-bottom: 3px solid #d4af37 !important;
            padding-bottom: 8px !important;
            margin-bottom: 20px !important;
        }

        h2, h3, .subtitulo-nasa {
            color: #0d1b2a !important;
            font-family: 'Arial Black', sans-serif !important;
            font-weight: 800 !important;
            text-transform: uppercase !important;
        }

        /* =================================================================
           🗃️ 3. CONTORNOS BLINDADOS PARA TABLAS Y DATA EDITORS
           ================================================================= */
        div[data-testid="stDataEditor"], 
        div[data-testid="stDataFrame"], 
        div[data-testid="stTable"],
        .stTable {
            border: 2.5px solid #0d1b2a !important;
            border-radius: 8px !important;
            box-shadow: 0px 5px 15px rgba(0,0,0,0.08) !important;
            overflow: hidden !important;
            background-color: #ffffff !important;
        }

        /* Forzar texto interno de las tablas en alta definición */
        div[data-testid="stDataEditor"] div, div[data-testid="stDataFrame"] div {
            color: #0d1b2a !important;
            font-weight: 600 !important;
        }

        /* =================================================================
           🎛️ 4. CONTORNOS DE ALTA DEFINICIÓN EN SELECTORES E INPUTS
           ================================================================= */
        /* Cajas de selección (Dropdowns) */
        div[data-baseweb="select"] {
            border: 2px solid #0d1b2a !important;
            border-radius: 6px !important;
            background-color: #ffffff !important;
        }
        
        /* Texto interno de los selectores */
        div[data-baseweb="select"] div {
            color: #0d1b2a !important;
            font-weight: bold !important;
        }

        /* Inputs de números, fechas y textos */
        div[data-testid="stNumberInput"] input, 
        div[data-testid="stTextInput"] input,
        div[data-testid="stDateInput"] input {
            border: 2px solid #0d1b2a !important;
            border-radius: 6px !important;
            color: #0d1b2a !important;
            font-weight: bold !important;
            background-color: #ffffff !important;
            height: 42px !important;
        }

        /* =================================================================
           📦 5. CONTENEDORES MÁSTER (Cajas de Mando y Uploaders)
           ================================================================= */
        /* Cajas contenedoras con borde rígido (with st.container(border=True)) */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            border: 2px solid #0d1b2a !important;
            border-radius: 8px !important;
            box-shadow: 0px 4px 15px rgba(0,0,0,0.04) !important;
            background-color: #ffffff !important;
        }

        /* Áreas de arrastre de archivos (Drag & Drop) */
        div[data-testid="stFileUploader"] {
            border: 2px dashed #0d1b2a !important;
            border-radius: 8px !important;
            background-color: #f8f9fa !important;
            padding: 12px !important;
        }
        </style>
    """, unsafe_allow_html=True)
