import streamlit as st

def inyectar_estilos_omega():
    st.markdown("""
        <style>
        /* Estilo para los Títulos */
        .titulo-dash {
            color: #0d1b2a !important;
            font-family: 'Arial Black', sans-serif !important;
            font-size: 32px !important;
            text-transform: uppercase !important;
            border-left: 6px solid #ff4b4b !important;
            padding-left: 15px !important;
            margin-bottom: 5px !important;
        }
        /* Estilo para los Subtítulos */
        .subtitulo-dash {
            color: #555555 !important;
            font-family: 'Segoe UI', sans-serif !important;
            font-size: 18px !important;
            font-weight: 600 !important;
            margin-bottom: 25px !important;
            padding-left: 21px !important;
        }
        </style>
    """, unsafe_allow_html=True)
