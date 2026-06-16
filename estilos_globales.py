import streamlit as st

def inyectar_estilos_omega():
    # Esta es la base mínima, sin CSS complicado para no romper nada
    st.markdown("""
        <style>
        .titulo-dash { color: #0d1b2a; }
        </style>
    """, unsafe_allow_html=True)
