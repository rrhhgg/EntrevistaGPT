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
        st.session_state.pagina_actual = "landing"

def landing():
    mostrar_logo()
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"### Bienvenid@ {st.session_state.entrevistador}")
    with col2:
        if st.button("Cerrar sesión 🔒"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.session_state.pagina_actual = "login"
            return

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
                st.session_state.pagina_actual = "datos"
                return
        i += 1

def formulario_datos():
    mostrar_logo()
    st.markdown("### 📋 Datos del candidato")
    with st.form("form_datos"):
        st.session_state.nombre = st.text_input("Nombre completo")
        st.session_state.telefono = st.text_input("Teléfono")
        st.session_state.correo = st.text_input("Correo electrónico")
        st.session_state.via = st.selectbox("Tipo de vía", ["Calle", "Avenida", "Plaza", "Camino"])
        st.session_state.nombre_via = st.text_input("Nombre de la vía")
        st.session_state.numero = st.text_input("Número")
        st.session_state.puerta = st.text_input("Puerta")
        st.session_state.cp = st.text_input("Código postal")
        st.session_state.ciudad = st.text_input("Ciudad")

        if st.form_submit_button("Comenzar entrevista"):
            st.session_state.pagina_actual = "preguntas"
            st.session_state.pagina_pregunta = 0
            st.session_state.tiempos = []
            st.session_state.respuestas = []

def main():
    if "pagina_actual" not in st.session_state:
        st.session_state.pagina_actual = "login"

    pagina = st.session_state.pagina_actual

    if pagina == "login":
        login()
    elif pagina == "landing":
        landing()
    elif pagina == "datos":
        formulario_datos()
    elif pagina == "preguntas":
        st.write("Aquí vendrán las preguntas...")

if __name__ == "__main__":
    main()