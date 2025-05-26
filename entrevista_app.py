import streamlit as st
import time
from respuestas_tipo import RESPUESTAS_TIPO

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
    '¿Dónde vives actualmente y cómo sueles desplazarte al trabajo? En caso de utilizar transporte público, ¿cómo te organizas si sales del local después del último servicio (por ejemplo, fuera del horario del metro)?',
    '¿Tienes disponibilidad para trabajar por la noche y los fines de semana? ¿Podrías desplazarte sin problema a cualquiera de nuestros locales en esos horarios?',
    '¿Qué idiomas hablas y cuál es tu nivel en cada uno de ellos? Puedes mencionar si tienes fluidez al hablar, escribir o entender, y si los utilizas habitualmente en el trabajo.',
    '¿Qué es lo que más te gustaba y lo que menos de tu último trabajo? ¿Por qué motivo decidiste dejarlo?',
    '¿Cómo describirías el ambiente de trabajo en tus empleos anteriores? ¿Qué tal era tu relación con los compañeros y el equipo?'
]

PREGUNTAS_POR_ROL = {
    "camarero": ['Estás atendiendo cuatro mesas que han llegado con poco margen entre ellas. ¿Cómo decides a cuál atender primero?', 'Háblame de una ocasión en la que ayudaste a un compañero que iba atrasado en su trabajo, aunque tú ya habías terminado tus tareas.', 'Cuéntame sobre una ocasión en la que un cliente te dijo que un plato no estaba a su gusto, aunque ya lo había comido casi entero.', 'En el briefing antes del servicio, tu director te indica que estás marcando mal los cubiertos. ¿Qué haces?', 'Estás en el pase y ves que un plato está listo pero nadie lo recoge. No es para tu mesa. ¿Qué haces?', 'Cuéntame sobre una ocasión en la que una mesa ya había pedido lo justo para cenar. ¿Qué hiciste?', 'Has terminado tu servicio y estás a punto de irte. ¿Cómo dejas tu zona de trabajo?', 'Cuéntame sobre una ocasión en la que cometiste un error al tomar una comanda y se lo serviste mal al cliente.']
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

    respuesta_key = f"respuesta_{pagina}"
    if respuesta_key not in st.session_state:
        st.session_state[respuesta_key] = ""
    if "respuesta_tiempo_inicio" not in st.session_state:
        st.session_state.respuesta_tiempo_inicio = time.time()
    if "respuesta_confirmada" not in st.session_state:
        st.session_state.respuesta_confirmada = False

    respuesta = st.text_area(pregunta, key=respuesta_key)

    tiempo_transcurrido = int(time.time() - st.session_state.respuesta_tiempo_inicio)
    tiempo_maximo = min(tiempo_transcurrido, 120)

    if not st.session_state.respuesta_confirmada:
        if st.button("✅ Cargar respuesta") and respuesta.strip():
            st.session_state.respuesta_confirmada = True
            st.session_state.respuestas.append(respuesta.strip())
            st.session_state.tiempos.append(tiempo_maximo)
    else:
        st.success("✅ Respuesta cargada correctamente.")
        if st.button("➡️ Siguiente pregunta"):
            st.session_state.pagina_pregunta += 1
            st.session_state.respuesta_confirmada = False
            st.session_state.pop("respuesta_tiempo_inicio", None)


def mostrar_resultados():
    mostrar_logo()
    st.markdown("### 📝 Resultados de la Entrevista")

    preguntas = st.session_state.preguntas
    respuestas = st.session_state.respuestas
    rol = st.session_state.rol

    # Separar preguntas generales y específicas
    preguntas_generales = preguntas[:5]
    preguntas_especificas = preguntas[5:]

    evaluaciones = []
    total_puntos = 0

    
    for i, pregunta in enumerate(preguntas_generales):
        st.code(f"PREGUNTA ACTUAL: {pregunta}")
        st.code(f"ENCONTRADA EN RESPUESTAS_TIPO: {pregunta in RESPUESTAS_TIPO.get(rol, {})}")
        respuesta = respuestas[i]
        tipo = "generales"
        respuestas_tipo = RESPUESTAS_TIPO.get(rol, {}).get(pregunta, [])
        if respuestas_tipo:
            puntuacion, justificacion = evaluar_con_openai_con_referencias(respuesta, pregunta, respuestas_tipo, rol)
        else:
            puntuacion, justificacion = 0, "No se pudo evaluar: faltan respuestas tipo para esta pregunta."
        total_puntos += puntuacion
        st.markdown(f"**Pregunta {i+1}:** Puntuación: {puntuacion}/10")
        st.markdown(f"Justificación: {justificacion}")
        st.markdown("---")



    for j, pregunta in enumerate(preguntas_especificas):
        respuesta = respuestas[j + len(preguntas_generales)]
        tipo = rol
        respuestas_tipo = RESPUESTAS_TIPO.get(rol, {}).get(pregunta, [])
        if respuestas_tipo:
            puntuacion, justificacion = evaluar_con_openai_con_referencias(respuesta, pregunta, respuestas_tipo, rol)
        else:
            puntuacion, justificacion = 0, "No se pudo evaluar: faltan respuestas tipo para esta pregunta."
        total_puntos += puntuacion
        st.markdown(f"**Pregunta {j+1+len(preguntas_generales)}:** Puntuación: {puntuacion}/10")
        st.markdown(f"Justificación: {justificacion}")
        st.markdown("---")

    st.markdown(f"**⏱️ Tiempo total empleado:** {sum(st.session_state.tiempos)} segundos")
    st.markdown(f"**✅ Puntuación total:** {total_puntos} puntos")

    # Evaluación real con OpenAI para envío
    column_values = generar_column_values_con_evaluacion(
        preguntas_generales,
        preguntas_especificas,
        respuestas,
        rol
    )

    enviado, mensaje = enviar_resultados_monday(st.session_state, column_values)
    if enviado:
        st.success(mensaje)
    else:
        st.error(mensaje)

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