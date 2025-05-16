import streamlit as st
from PIL import Image
import base64

def set_background(png_file):
    with open(png_file, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    css = f"""
    <style>
        .stApp {{
            background-image: url('data:image/png;base64,{encoded}');
            background-size: 300px;
            background-repeat: no-repeat;
            background-position: center;
            background-attachment: fixed;
            background-color: white;
        }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def login():
    st.title("Login de Entrevistador")
    entrevistadores = ["Don Gómez", "Doña Gómez", "Francesco", "Ana", "Carlos"]
    seleccion = st.selectbox("Selecciona tu nombre", entrevistadores)
    if st.button("Entrar"):
        st.session_state.entrevistador = seleccion
        st.session_state.logged_in = True

def landing():
    st.title(f"Bienvenido, {st.session_state.entrevistador}")
    st.subheader("Selecciona el tipo de entrevista que deseas realizar:")
    roles = {
        "🍽️ Camarero": "camarero",
        "🔪 Cocinero": "cocinero",
        "👩‍✈️ Hostess": "hostess",
        "👔 Director": "director",
        "👨‍🍳 Jefe de Cocina": "jefe_cocina",
        "🧼 Friegue": "friegue",
        "🚚 Repartidor": "repartidor"
    }

    for nombre, clave in roles.items():
        if st.button(nombre):
            st.session_state.rol = clave
            st.success(f"Has elegido la entrevista para: {nombre}")
            st.stop()

def main():
    set_background("logo_gastronomico.png")

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        login()
    else:
        landing()

if __name__ == "__main__":
    main()