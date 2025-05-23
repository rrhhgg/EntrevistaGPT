
import streamlit as st
import time
import json
from datetime import datetime
from enviar_a_monday import enviar_a_monday

st.set_page_config(page_title="Entrevista Camarero", layout="centered")

# Fondo con logo centrado
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://yurest.s3.eu-west-3.amazonaws.com/logo_gastronomico.png");
    background-size: 500pt;
    background-repeat: no-repeat;
    background-position: top center;
}
[data-testid="stHeader"] {background: rgba(0,0,0,0);}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

if "pagina" not in st.session_state:
    st.session_state.pagina = "login"

if "datos_personales" not in st.session_state:
    st.session_state.datos_personales = {}

if "preguntas" not in st.session_state:
    st.session_state.preguntas = [
        # Generales
        "¿Dónde vives actualmente y cómo sueles desplazarte al trabajo? En caso de utilizar transporte público, ¿cómo te organizas si sales del local después del último servicio (por ejemplo, fuera del horario del metro)?",
        "¿Tienes disponibilidad para trabajar por la noche y los fines de semana? ¿Podrías desplazarte sin problema a cualquiera de nuestros locales en esos horarios?",
        "¿Qué idiomas hablas y cuál es tu nivel en cada uno de ellos? Puedes mencionar si tienes fluidez al hablar, escribir o entender, y si los utilizas habitualmente en el trabajo.",
        "¿Qué es lo que más te gustaba y lo que menos de tu último trabajo? ¿Por qué motivo decidiste dejarlo?",
        "¿Cómo describirías el ambiente de trabajo en tus empleos anteriores? ¿Qué tal era tu relación con los compañeros y el equipo?",
        # Camarero
        "¿Cómo das la bienvenida a una mesa y cómo te presentas?",
        "¿Qué haces si un cliente tiene una alergia alimentaria?",
        "¿Cómo recomiendas un vino a un cliente que no sabe qué elegir?",
        "¿Cómo organizas tus mesas cuando hay mucho trabajo?",
        "¿Qué haces si ves que un compañero necesita ayuda durante el servicio?",
        "¿Cómo actúas si un plato no está como esperaba el cliente?",
        "¿Qué haces si ves una copa o plato sucio?",
        "¿Qué haces cuando entregas la cuenta?"
    ]

if "respuestas" not in st.session_state:
    st.session_state.respuestas = []

if "tiempos" not in st.session_state:
    st.session_state.tiempos = []

def login():
    st.title("Selecciona tu nombre")
    entrevistador = st.selectbox("", ["Keko", "Maika", "Alba", "Cristina", "Maria", "Vlad", "Julio", "Vanesa", "Mada"])
    if st.button("Entrar"):
        st.session_state.entrevistador = entrevistador
        st.session_state.pagina = "datos"

def datos_personales():
    st.title("Datos del candidato")
    nombre = st.text_input("Nombre completo")
    telefono = st.text_input("Teléfono")
    correo = st.text_input("Correo electrónico")
    via = st.selectbox("Tipo de vía", ["Calle", "Avenida", "Plaza", "Otro"])
    nombre_via = st.text_input("Nombre de la vía")
    numero = st.text_input("Número")
    puerta = st.text_input("Puerta")
    cp = st.text_input("Código Postal")
    ciudad = st.text_input("Ciudad")

    if st.button("Comenzar entrevista"):
        if not telefono.startswith("+"):
            telefono = "+34" + telefono
        st.session_state.datos_personales = {
            "nombre": nombre,
            "telefono": telefono,
            "correo": correo,
            "via": via,
            "nombre_via": nombre_via,
            "numero": numero,
            "puerta": puerta,
            "cp": cp,
            "ciudad": ciudad
        }
        st.session_state.pagina = "entrevista"
        st.session_state.inicio = time.time()
        st.session_state.indice = 0

def entrevista():
    indice = st.session_state.indice
    preguntas = st.session_state.preguntas
    if indice < len(preguntas):
        st.subheader(f"Pregunta {indice + 1}")
        st.markdown("Tienes 120 segundos para responder.")
        inicio = time.time()
        respuesta = st.text_area(preguntas[indice], height=200)
        if st.button("Siguiente") or time.time() - inicio > 120:
            st.session_state.respuestas.append(respuesta)
            st.session_state.tiempos.append(int(time.time() - inicio))
            st.session_state.indice += 1
    else:
        st.session_state.pagina = "final"

def final():
    st.title("✅ Entrevista completada")
    respuestas = st.session_state.respuestas
    tiempos = st.session_state.tiempos
    puntuaciones = [7] * len(respuestas)
    evaluaciones = ["Evaluación automática"] * len(respuestas)
    total = sum(puntuaciones)
    tiempo_total = sum(tiempos)
    evaluacion_final = "Ejemplo de evaluación final"

    datos = {
        **st.session_state.datos_personales,
        "entrevistador_email": "frmichelin@grupogomez.es",
        "rol": "camarero",
        "puntuaciones": puntuaciones,
        "evaluaciones": evaluaciones,
        "puntuacion_total": total,
        "evaluacion_final": evaluacion_final,
        "tiempo_total": tiempo_total
    }

    st.write(f"✅ Puntuación total: {total}")
    st.write("📦 Enviando datos a Monday...")
    try:
        resultado = enviar_a_monday(datos, api_key="eyJhbGciOiJIUzI1NiJ9...", board_id=1939525964)
        if resultado:
            st.success("✅ Enviado correctamente a Monday")
        else:
            st.error("❌ Hubo un problema al enviar la entrevista a Monday.")
    except Exception as e:
        st.error(f"❌ Error al enviar a Monday:

{e}")

def main():
    if st.session_state.pagina == "login":
        login()
    elif st.session_state.pagina == "datos":
        datos_personales()
    elif st.session_state.pagina == "entrevista":
        entrevista()
    elif st.session_state.pagina == "final":
        final()

main()
