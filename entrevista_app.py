
import streamlit as st
from evaluar_respuestas_con_referencias import evaluar_respuesta

# Datos de entrevistadores
ENTREVISTADORES = {
    "Keko": "keko@grupogomez.es",
    "Maika": "maika@grupogomez.es",
    "Alba": "alba@grupogomez.es",
    "Cristina": "cristina@grupogomez.es",
    "Maria": "maria@grupogomez.es",
    "Vlad": "vlad@grupogomez.es",
    "Julio": "julio@grupogomez.es",
    "Vanesa": "vanesa@grupogomez.es",
    "Mada": "mada@grupogomez.es"
}

# Preguntas generales
PREGUNTAS_GENERALES = [
    "¿Dónde vives actualmente y cómo sueles desplazarte al trabajo?\nEn caso de utilizar transporte público, ¿cómo te organizas si sales del local después del último servicio (por ejemplo, fuera del horario del metro)?",
    "¿Tienes disponibilidad para trabajar por la noche y los fines de semana?\n¿Podrías desplazarte sin problema a cualquiera de nuestros locales en esos horarios?",
    "¿Qué idiomas hablas y cuál es tu nivel en cada uno de ellos?\nPuedes mencionar si tienes fluidez al hablar, escribir o entender, y si los utilizas habitualmente en el trabajo.",
    "¿Qué es lo que más te gustaba y lo que menos de tu último trabajo?\n¿Por qué motivo decidiste dejarlo?",
    "¿Cómo describirías el ambiente de trabajo en tus empleos anteriores?\n¿Qué tal era tu relación con los compañeros y el equipo?"
]

# Inicializar estado
if "pagina" not in st.session_state:
    st.session_state.pagina = "login"
if "entrevistador" not in st.session_state:
    st.session_state.entrevistador = None
if "entrevista_rol" not in st.session_state:
    st.session_state.entrevista_rol = None
if "datos_personales" not in st.session_state:
    st.session_state.datos_personales = {}
if "respuestas" not in st.session_state:
    st.session_state.respuestas = []
if "puntuaciones" not in st.session_state:
    st.session_state.puntuaciones = []
if "evaluaciones" not in st.session_state:
    st.session_state.evaluaciones = []
if "pregunta_actual" not in st.session_state:
    st.session_state.pregunta_actual = 0

# LOGIN
if st.session_state.pagina == "login":
    st.title("👤 Selección de entrevistador")
    entrevistador = st.selectbox("Selecciona tu nombre", list(ENTREVISTADORES.keys()))
    if st.button("Acceder"):
        st.session_state.entrevistador = entrevistador
        st.session_state.pagina = "menu"

# MENÚ PRINCIPAL
elif st.session_state.pagina == "menu":
    st.markdown(f"👋 Bienvenid@ **{st.session_state.entrevistador}**")
    st.markdown("### Selecciona el puesto a entrevistar:")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🍽️ Camarero"):
            st.session_state.entrevista_rol = "Camarero"
            st.session_state.pagina = "datos"
    with col2:
        if st.button("🔪 Cocinero"):
            st.session_state.entrevista_rol = "Cocinero"
            st.session_state.pagina = "datos"
    with col3:
        if st.button("👨‍🍳 Jefe de Cocina"):
            st.session_state.entrevista_rol = "Jefe de Cocina"
            st.session_state.pagina = "datos"

    col4, col5, col6 = st.columns(3)
    with col4:
        if st.button("👔 Director"):
            st.session_state.entrevista_rol = "Director"
            st.session_state.pagina = "datos"
    with col5:
        if st.button("🧼 Friegaplatos"):
            st.session_state.entrevista_rol = "Friegaplatos"
            st.session_state.pagina = "datos"
    with col6:
        if st.button("🚚 Repartidor"):
            st.session_state.entrevista_rol = "Repartidor"
            st.session_state.pagina = "datos"
    if st.button("👩‍✈️ Hostess"):
        st.session_state.entrevista_rol = "Hostess"
        st.session_state.pagina = "datos"

# DATOS PERSONALES
elif st.session_state.pagina == "datos":
    st.title(f"📋 Datos del candidato para el puesto de {st.session_state.entrevista_rol}")
    nombre = st.text_input("Nombre y apellidos")
    telefono = st.text_input("Teléfono")
    correo = st.text_input("Correo electrónico")
    col1, col2 = st.columns(2)
    with col1:
        calle = st.text_input("Calle")
        numero = st.text_input("Número")
    with col2:
        puerta = st.text_input("Puerta")
        cp = st.text_input("Código postal")
    ciudad = st.text_input("Ciudad")

    if st.button("Comenzar entrevista"):
        st.session_state.datos_personales = {
            "nombre": nombre,
            "telefono": telefono,
            "correo": correo,
            "direccion": f"{calle}, {numero}, {puerta}, {cp}, {ciudad}"
        }
        st.session_state.pagina = "entrevista"

# ENTREVISTA
elif st.session_state.pagina == "entrevista":
    idx = st.session_state.pregunta_actual
    if idx < len(PREGUNTAS_GENERALES):
        st.markdown(f"**Pregunta {idx+1}:**")
        st.markdown(PREGUNTAS_GENERALES[idx].replace("\n", "  
"))
        respuesta = st.text_area("Tu respuesta", key=f"respuesta_{idx}", value="", placeholder="Escribe tu respuesta...")

        if st.button("Siguiente"):
            resultado = evaluar_respuesta(
                pregunta=PREGUNTAS_GENERALES[idx],
                respuesta_usuario=respuesta,
                rol=st.session_state.entrevista_rol,
                respuesta_tipo=None
            )
            st.session_state.respuestas.append(respuesta)
            st.session_state.puntuaciones.append(resultado["puntuacion"])
            st.session_state.evaluaciones.append(resultado["evaluacion"])
            st.session_state.pregunta_actual += 1
            st.experimental_rerun()

    else:
        st.session_state.pagina = "final"

# RESULTADO FINAL
elif st.session_state.pagina == "final":
    st.success("✅ Entrevista finalizada")
    st.markdown(f"**Candidato:** {st.session_state.datos_personales['nombre']}")
    st.markdown(f"**Puesto:** {st.session_state.entrevista_rol}")
    st.markdown("---")
    for i, pregunta in enumerate(PREGUNTAS_GENERALES):
        st.markdown(f"**{pregunta.replace('\n', '  
')}**")
        st.markdown(f"- Respuesta: {st.session_state.respuestas[i]}")
        st.markdown(f"- Puntuación: {st.session_state.puntuaciones[i]}")
        st.markdown(f"- Evaluación: {st.session_state.evaluaciones[i]}")
        st.markdown("---")
