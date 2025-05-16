import streamlit as st
from PIL import Image
import base64

# Diccionario de entrevistadores y correos
ENTREVISTADORES = {
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

def set_background(png_file):
    with open(png_file, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    css = f"""
    <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: 80%;
            background-repeat: no-repeat;
            background-position: top center;
            background-attachment: fixed;
            background-color: white;
        }}
        .spacer {{
            height: 250px;
        }}
        .header-container {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 2rem;
        }}
        .horizontal-buttons {{
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 1rem;
            margin-top: 3rem;
        }}
        .horizontal-buttons button {{
            font-size: 17px !important;
            padding: 0.75em 2em !important;
        }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def login():
    st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)
    st.title("Login de Entrevistador")
    seleccion = st.selectbox("Selecciona tu nombre", list(ENTREVISTADORES.keys()))
    if st.button("Entrar"):
        st.session_state.entrevistador = seleccion
        st.session_state.email = ENTREVISTADORES[seleccion]
        st.session_state.logged_in = True

def logout():
    st.markdown(
        f"""
        <div class="header-container">
            <h2>Bienvenid@ {st.session_state.entrevistador}</h2>
            <form action="" method="post">
                <button name="logout" type="submit">Cerrar sesión 🔒</button>
            </form>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.session_state.get("logout"):
        st.session_state.logged_in = False
        st.session_state.entrevistador = None
        st.session_state.email = None

def landing():
    st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)
    logout()
    roles = {
        "🍽️ Camarero": "camarero",
        "🔪 Cocinero": "cocinero",
        "👩‍✈️ Hostess": "hostess",
        "👔 Director": "director",
        "👨‍🍳 Jefe de Cocina": "jefe_cocina",
        "🧼 Friegue": "friegue",
        "🚚 Repartidor": "repartidor"
    }

    st.markdown('<div class="horizontal-buttons">', unsafe_allow_html=True)
    for nombre, clave in roles.items():
        if st.button(nombre, key=clave):
            st.session_state.rol = clave
            st.success(f"Has elegido la entrevista para: {nombre}")
            st.stop()
    st.markdown('</div>', unsafe_allow_html=True)

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