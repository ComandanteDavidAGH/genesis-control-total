import streamlit as st

def inyectar_estilos_omega():
    st.markdown("""
        <style>
        /* TÍTULO Y SUBTÍTULO OMEGA (Nuevos) */
        .titulo-dash {
            color: #0d1b2a !important;import streamlit as st

def inyectar_estilos_omega():
    st.markdown("""
        <style>
        /* MANTENEMOS TUS CLASES ORIGINALES PARA BORDES Y CAJAS */
        .stContainer { border: 1px solid #e0e0e0; border-radius: 10px; padding: 10px; }
        
        /* TÍTULOS - Solo añadimos esto si no interfiere con lo anterior */
        .titulo-dash {
            color: #0d1b2a;
            font-family: sans-serif;
            font-size: 32px;
            border-left: 6px solid #ff4b4b;
            padding-left: 15px;
        }
        </style>
    """, unsafe_allow_html=True)
            font-family: sans-serif !important;
            font-size: 32px !important;
            border-left: 6px solid #ff4b4b !important;
            padding-left: 15px !important;
            margin-bottom: 5px !important;
        }
        .subtitulo-dash {
            color: #555555 !important;
            font-size: 18px !important;
            font-weight: 600 !important;
            margin-bottom: 25px !important;
            padding-left: 21px !important;
        }
        /* NOTA: NO TOCAMOS NADA DE .stContainer o .css-1r6slp, 
           así tus bordes y cajas quedan intactos. */
        </style>
    """, unsafe_allow_html=True)
