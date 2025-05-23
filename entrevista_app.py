import streamlit as st
import time

from evaluar_respuestas_con_referencias import evaluar_con_openai_con_referencias
from respuestas_tipo import RESPUESTAS_TIPO
from generar_column_values import generar_column_values_con_evaluacion
from enviar_a_monday import enviar_resultados_monday

ENTREVISTADORES = {
    "Keko": "frmichelin@grupogomez.es"
}

PREGUNTAS_GENERALES = [
    "¿Dónde vives actualmente y cómo sueles desplazarte al trabajo? En caso de utilizar transporte público, ¿cómo te organizas si sales del local después del último servicio (por ejemplo, fuera del horario del metro)?",
    "¿Tienes disponibilidad para trabajar por la noche y los fines de semana? ¿Podrías desplazarte sin problema a cualquiera de nuestros locales en esos horarios?",
    "¿Qué idiomas hablas y cuál es tu nivel en cada uno de ellos? Puedes mencionar si tienes fluidez al hablar, escribir o entender, y si los utilizas habitualmente en el trabajo.",
    "¿Qué es lo que más te gustaba y lo que menos de tu último trabajo? ¿Por qué motivo decidiste dejarlo?",
    "¿Cómo describirías el ambiente de trabajo en tus empleos anteriores? ¿Qué tal era tu relación con los compañeros y el equipo?"
]

PREGUNTAS_POR_ROL = {
    "camarero": [
        "Estás atendiendo cuatro mesas que han llegado con poco margen entre ellas. ¿Cómo decides a cuál atender primero?",
        "Háblame de una ocasión en la que ayudaste a un compañero que iba atrasado en su trabajo, aunque tú ya habías terminado tus tareas.",
        "Cuéntame sobre una ocasión en la que un cliente te dijo que un plato no estaba a su gusto, aunque ya lo había comido casi entero.",
        "En el briefing antes del servicio, tu director te indica que estás marcando mal los cubiertos. ¿Qué haces?",
        "Estás en el pase y ves que un plato está listo pero nadie lo recoge. No es para tu mesa. ¿Qué haces?",
        "Cuéntame sobre una ocasión en la que una mesa ya había pedido lo justo para cenar. ¿Qué hiciste?",
        "Has terminado tu servicio y estás a punto de irte. ¿Cómo dejas tu zona de trabajo?",
        "Cuéntame sobre una ocasión en la que cometiste un error al tomar una comanda y se lo serviste mal al cliente."
    ]
}

def main():
    st.set_page_config(page_title="Entrevista", layout="centered")
    if "pagina_actual" not in st.session_state:
        st.session_state.pagina_actual = "login"

    if st.session_state.pagina_actual == "login":
        st.title("Login de Entrevistador")
        seleccion = st.selectbox("Selecciona tu nombre", list(ENTREVISTADORES.keys()))
        if st.button("Entrar"):
            st.session_state.entrevistador = seleccion
            st.session_state.email = ENTREVISTADORES[seleccion]
            st.session_state.pagina_actual = "datos"

    elif st.session_state.pagina_actual == "datos":
        st.title("Datos del candidato")
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
            st.session_state.rol = "camarero"
            if st.form_submit_button("Comenzar entrevista"):
                st.session_state.preguntas_generales = PREGUNTAS_GENERALES
                st.session_state.preguntas_rol = PREGUNTAS_POR_ROL[st.session_state.rol]
                st.session_state.respuestas = []
                st.session_state.tiempos = []
                st.session_state.pagina_pregunta = 0
                st.session_state.start_time = time.time()
                st.session_state.pagina_actual = "preguntas"

    elif st.session_state.pagina_actual == "preguntas":
        todas = st.session_state.preguntas_generales + st.session_state.preguntas_rol
        index = st.session_state.pagina_pregunta
        st.markdown(f"**Pregunta {index + 1} de {len(todas)}**")
        st.markdown("Tienes 120 segundos para responder.")
        pregunta = todas[index]
        respuesta = st.text_area("Respuesta:", key=f"respuesta_{index}")
        if "respuesta_tiempo_inicio" not in st.session_state:
            st.session_state.respuesta_tiempo_inicio = time.time()
        tiempo_transcurrido = int(time.time() - st.session_state.respuesta_tiempo_inicio)

        avanzar = False
        if tiempo_transcurrido >= 120:
            avanzar = True
        else:
            if st.button("Enviar respuesta"):
                avanzar = True

        if avanzar:
            st.session_state.respuestas.append(respuesta)
            st.session_state.tiempos.append(min(tiempo_transcurrido, 120))
            st.session_state.pagina_pregunta += 1
            st.session_state.respuesta_tiempo_inicio = time.time()

            if st.session_state.pagina_pregunta >= len(todas):
                st.session_state.pagina_actual = "resultados"

    elif st.session_state.pagina_actual == "resultados":
        st.title("Enviando resultados...")
        column_values = generar_column_values_con_evaluacion(
            st.session_state.preguntas_generales,
            st.session_state.preguntas_rol,
            st.session_state.respuestas,
            st.session_state.rol
        )
        enviado, mensaje = enviar_resultados_monday(st.session_state, column_values)
        if enviado:
            st.success(mensaje)
        else:
            st.error(mensaje)

if __name__ == "__main__":
    main()