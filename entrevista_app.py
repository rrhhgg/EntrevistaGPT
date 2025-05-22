import streamlit as st
import time

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

PREGUNTAS_COMUNES = [
    "¿Qué idiomas hablas y con qué nivel?",
    "¿Tienes medio de transporte propio para llegar al trabajo?"
]

PREGUNTAS_POR_ROL = {
    "camarero": [
        "Cuéntame cómo recomiendas un vino a un cliente que no sabe qué pedir."
    ]
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

def logout():
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"### Bienvenid@ {st.session_state.entrevistador}")
    with col2:
        if st.button("Cerrar sesión 🔒"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.session_state.pagina_actual = "login"

def landing():
    mostrar_logo()
    logout()
    st.markdown("### Selecciona el tipo de entrevista que deseas realizar:")

    roles = {
        "🍽️ Camarero": "camarero"
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
            preguntas_especificas = PREGUNTAS_POR_ROL.get(st.session_state.rol, [])
            st.session_state.preguntas = PREGUNTAS_COMUNES + preguntas_especificas
            st.session_state.pagina_pregunta = 0
            st.session_state.respuestas = []
            st.session_state.tiempos = []
            st.session_state.start_time = time.time()
            st.session_state.pagina_actual = "preguntas"

def entrevista():
    mostrar_logo()
    preguntas = st.session_state.preguntas
    pagina = st.session_state.pagina_pregunta

    if pagina >= len(preguntas):
        mostrar_resultados()
        return

    pregunta = preguntas[pagina]
    st.markdown(f"### Pregunta {pagina + 1} de {len(preguntas)}")
    st.write("⏱️ Tienes 120 segundos para responder.")
    respuesta = st.text_area(pregunta, key=f"respuesta_{pagina}")

    tiempo_transcurrido = int(time.time() - st.session_state.start_time)
    if tiempo_transcurrido >= 120:
        avanzar = True
    else:
        avanzar = st.button("Enviar respuesta")

    if avanzar:
        st.session_state.respuestas.append(respuesta)
        st.session_state.tiempos.append(min(tiempo_transcurrido, 120))
        st.session_state.start_time = time.time()
        st.session_state.pagina_pregunta += 1
        st.experimental_rerun()

def mostrar_resultados():
    mostrar_logo()
    st.markdown("### 📝 Resultados de la Entrevista")

    total_puntos = 0
    st.session_state.evaluaciones = []

    for i, respuesta in enumerate(st.session_state.respuestas):
        puntuacion = 7
        justificacion = "Ejemplo de evaluación generada automáticamente."
        total_puntos += puntuacion
        st.markdown(f"**Pregunta {i+1}:** Puntuación: {puntuacion}/10")
        st.markdown(f"Justificación: {justificacion}")
        st.markdown("---")

    st.markdown(f"**⏱️ Tiempo total empleado:** {sum(st.session_state.tiempos)} segundos")
    st.markdown(f"**✅ Puntuación total:** {total_puntos} puntos")

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
        entrevista()

if __name__ == "__main__":
    main()