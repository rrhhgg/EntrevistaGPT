import streamlit as st
import time
from datetime import datetime
from enviar_a_monday import enviar_a_monday

def normalizar_telefono(telefono):
    telefono = telefono.strip()
    if not telefono.startswith("+"):
        return f"+34 {telefono}"
    return telefono

def login():
    entrevistadores = {
        "Keko": "frmichelin@grupogomez.es",
        "Maika": "m.demiguel@grupogomez.es",
        "Alba": "a.alandi@grupogomez.es",
        "Cristina": "c.domenech@grupogomez.es",
        "Maria": "maria.martin@grupogomez.es",
        "Vlad": "v.cobusneanu@grupogomez.es",
        "Julio": "j.barzola@grupogomez.es",
        "Vanesa": "v.gomez@grupogomez.es",
        "Mada": "mada.broton@grupogomez.es"
    }

    if "entrevistador" not in st.session_state:
        st.session_state.entrevistador = None

    st.markdown(
        f"""
        <style>
            .fondo-logo {{
                background-image: url('https://raw.githubusercontent.com/rrhhgg/EntrevistaGPT/main/logo_gastronomico.png');
                background-size: 500px auto;
                background-repeat: no-repeat;
                background-position: top center;
                padding-top: 520px;
            }}
            .boton-centrado {{
                display: flex;
                justify-content: center;
            }}
        </style>
        <div class="fondo-logo"></div>
        """, unsafe_allow_html=True
    )

    if st.session_state.entrevistador is None:
        st.write("## Selecciona tu nombre")
        entrevistador = st.selectbox("", list(entrevistadores.keys()), key="selector")
        if st.button("Entrar"):
            st.session_state.entrevistador = {
                "nombre": entrevistador,
                "correo": entrevistadores[entrevistador]
            }
            st.session_state.pagina = "menu"

    else:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"### Bienvenid@ {st.session_state.entrevistador['nombre']}")
        with col2:
            if st.button("Cerrar sesión"):
                st.session_state.entrevistador = None
                st.session_state.pagina = "login"