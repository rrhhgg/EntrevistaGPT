
import streamlit as st
from evaluar_respuestas_con_referencias import evaluar_respuesta

st.set_page_config(page_title="Entrevista Camarero", layout="centered")

# Simulación de preguntas
preguntas_generales = [
    "¿Dónde vives actualmente y cómo sueles desplazarte al trabajo?",
    "¿Tienes disponibilidad para trabajar por la noche y los fines de semana?",
    "¿Qué idiomas hablas y cuál es tu nivel?",
    "¿Qué te gustaba y qué no de tu último trabajo?",
    "¿Cómo era el ambiente de trabajo en tus empleos anteriores?"
]

# Inicialización
if "pagina_actual" not in st.session_state:
    st.session_state.pagina_actual = 0
if "respuestas" not in st.session_state:
    st.session_state.respuestas = []
if "puntuaciones" not in st.session_state:
    st.session_state.puntuaciones = []
if "evaluaciones" not in st.session_state:
    st.session_state.evaluaciones = []
if "respuesta_temp" not in st.session_state:
    st.session_state.respuesta_temp = ""

pagina = st.session_state.pagina_actual

if pagina < len(preguntas_generales):
    pregunta_actual = preguntas_generales[pagina]
    st.markdown(f"**Pregunta {pagina+1}:** {pregunta_actual}")

    respuesta_input = st.text_area(
        "Tu respuesta",
        key=f"respuesta_p{pagina}",
        value="",
        placeholder="Escribe tu respuesta aquí..."
    )

    if st.button("Siguiente") and respuesta_input.strip() != "":
        resultado = evaluar_respuesta(
            pregunta=pregunta_actual,
            respuesta_usuario=respuesta_input,
            rol="Camarero",
            respuesta_tipo=None
        )

        st.session_state.respuestas.append(respuesta_input)
        st.session_state.puntuaciones.append(resultado["puntuacion"])
        st.session_state.evaluaciones.append(resultado["evaluacion"])
        st.session_state.pagina_actual += 1

elif pagina == len(preguntas_generales):
    st.success("✅ Entrevista finalizada")
    st.markdown("### Resultados:")
    for i, pregunta in enumerate(preguntas_generales):
        st.markdown(f"**{pregunta}**")
        st.markdown(f"- Respuesta: {st.session_state.respuestas[i]}")
        st.markdown(f"- Puntuación: {st.session_state.puntuaciones[i]}")
        st.markdown(f"- Evaluación: {st.session_state.evaluaciones[i]}")
        st.markdown("---")
