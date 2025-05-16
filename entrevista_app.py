import streamlit as st

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

def mostrar_logo():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("logo_gastronomico.png", width=300)

def login():
    mostrar_logo()
    st.title("Login de Entrevistador")
    seleccion = st.selectbox("Selecciona tu nombre", list(ENTREVISTADORES.keys()))
    if st.button("Entrar"):
        st.session_state.entrevistador = seleccion
        st.session_state.email = ENTREVISTADORES[seleccion]
        st.session_state.logged_in = True

def logout():
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"### Bienvenid@ {st.session_state.entrevistador}")
    with col2:
        if st.button("Cerrar sesión 🔒"):
            st.session_state.logged_in = False
            st.session_state.entrevistador = None
            st.session_state.email = None

def landing():
    mostrar_logo()
    logout()
    st.markdown("### Selecciona el tipo de entrevista que deseas realizar:")

    roles = {
        "🍽️ Camarero": "camarero",
        "🔪 Cocinero": "cocinero",
        "👩‍✈️ Hostess": "hostess",
        "👔 Director": "director",
        "👨‍🍳 Jefe de Cocina": "jefe_cocina",
        "🧼 Friegue": "friegue",
        "🚚 Repartidor": "repartidor"
    }

    cols = st.columns(4)
    i = 0
    for nombre, clave in roles.items():
        with cols[i % 4]:
            if st.button(nombre, key=clave):
                st.session_state.rol = clave
                st.success(f"Has elegido la entrevista para: {nombre}")
                st.stop()
        i += 1

def main():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        login()
    else:
        landing()

if __name__ == "__main__":
    main()