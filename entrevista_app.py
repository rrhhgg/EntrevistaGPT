import streamlit as st
import time
from datetime import datetime
from enviar_a_monday import enviar_a_monday


def normalizar_telefono(telefono):
    telefono = telefono.strip()
    if not telefono.startswith("+"):
        return f"+34 {telefono}"
    return telefono


def login():
    entrevistadores = {
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

    st.markdown("<div style='height: 500pt'></div>", unsafe_allow_html=True)

    if "entrevistador" not in st.session_state:
        st.session_state.entrevistador = None

    if st.session_state.entrevistador is None:
        entrevistador = st.selectbox("Selecciona tu nombre", list(entrevistadores.keys()))
        if st.button("Entrar"):
            st.session_state.entrevistador = {
                "nombre": entrevistador,
                "correo": entrevistadores[entrevistador]
            }
            st.experimental_rerun()
    else:
        st.markdown(f"<div style='display: flex; justify-content: space-between; align-items: center;'>"
                    f"<h3>Bienvenid@ {st.session_state.entrevistador['nombre']}</h3>"
                    f"<form action='' method='post'><button name='logout'>Cerrar sesión</button></form>"
                    f"</div>", unsafe_allow_html=True)

        if st.form_submit_button("Cerrar sesión", key="logout"):
            st.session_state.entrevistador = None
            st.experimental_rerun()


def pantalla_rol():
    st.markdown("<div style='height: 500pt'></div>", unsafe_allow_html=True)
    st.title("Selecciona el puesto de la entrevista")

    roles = {
        "🍽️ Camarero": "camarero",
        "🔪 Cocinero": "cocinero",
        "👩‍✈️ Hostess": "hostess",
        "👔 Director": "director",
        "👨‍🍳 Jefe de Cocina": "jefe_cocina",
        "🧼 Friegue": "friegue",
        "🚚 Repartidor": "repartidor"
    }

    cols = st.columns(len(roles))
    for i, (emoji_label, rol) in enumerate(roles.items()):
        if cols[i].button(emoji_label):
            st.session_state.rol = rol
            st.session_state.pagina = "datos"
            st.experimental_rerun()


def pantalla_datos():
    st.markdown("<div style='height: 500pt'></div>", unsafe_allow_html=True)
    st.title("Datos del candidato")

    with st.form("form_datos"):
        nombre = st.text_input("Nombre completo")
        telefono = st.text_input("Teléfono")
        correo = st.text_input("Correo electrónico")
        via = st.selectbox("Tipo de vía", ["Calle", "Avenida", "Plaza", "Otro"])
        nombre_via = st.text_input("Nombre de la vía")
        numero = st.text_input("Número")
        puerta = st.text_input("Puerta")
        cp = st.text_input("Código Postal")
        ciudad = st.text_input("Ciudad")

        if st.form_submit_button("Comenzar entrevista"):
            st.session_state.datos = {
                "nombre": nombre,
                "telefono": normalizar_telefono(telefono),
                "correo": correo,
                "via": via,
                "nombre_via": nombre_via,
                "numero": numero,
                "puerta": puerta,
                "cp": cp,
                "ciudad": ciudad,
                "entrevistador_email": st.session_state.entrevistador["correo"],
                "rol": st.session_state.rol
            }
            st.session_state.pagina = "entrevista"
            st.session_state.pregunta_actual = 0
            st.session_state.puntuaciones = []
            st.session_state.evaluaciones = []
            st.session_state.tiempos = []
            st.experimental_rerun()


def entrevista():
    preguntas_generales = [
        "¿Dónde vives actualmente y cómo sueles desplazarte al trabajo? En caso de utilizar transporte público, ¿cómo te organizas si sales del local después del último servicio (por ejemplo, fuera del horario del metro)?",
        "¿Tienes disponibilidad para trabajar por la noche y los fines de semana? ¿Podrías desplazarte sin problema a cualquiera de nuestros locales en esos horarios?",
        "¿Qué idiomas hablas y cuál es tu nivel en cada uno de ellos? Puedes mencionar si tienes fluidez al hablar, escribir o entender, y si los utilizas habitualmente en el trabajo.",
        "¿Qué es lo que más te gustaba y lo que menos de tu último trabajo? ¿Por qué motivo decidiste dejarlo?",
        "¿Cómo describirías el ambiente de trabajo en tus empleos anteriores? ¿Qué tal era tu relación con los compañeros y el equipo?"
    ]
    preguntas_especificas = [
        f"P{i+1} específica del rol {st.session_state.rol}" for i in range(8)
    ]

    todas_preguntas = preguntas_generales + preguntas_especificas

    idx = st.session_state.pregunta_actual
    if idx >= len(todas_preguntas):
        st.session_state.pagina = "resultados"
        st.experimental_rerun()

    st.title(f"Pregunta {idx + 1}")
    st.markdown("Tienes 120 segundos para responder.")

    start_time = time.time()
    respuesta = st.text_area("Tu respuesta:")

    if st.button("Siguiente") or time.time() - start_time > 120:
        duracion = round(time.time() - start_time)
        st.session_state.puntuaciones.append(7)
        st.session_state.evaluaciones.append("Evaluación automática")
        st.session_state.tiempos.append(duracion)
        st.session_state.pregunta_actual += 1
        st.experimental_rerun()


def mostrar_resultados():
    st.title("¡Entrevista completada!")

    puntuacion_total = sum(st.session_state.puntuaciones)
    tiempo_total = sum(st.session_state.tiempos)
    evaluacion_final = "Ejemplo de evaluación final"

    datos = st.session_state.datos.copy()
    datos.update({
        "puntuacion_total": puntuacion_total,
        "evaluacion_final": evaluacion_final,
        "tiempo_total": tiempo_total,
        "puntuaciones": st.session_state.puntuaciones,
        "evaluaciones": st.session_state.evaluaciones
    })

    st.markdown(f"✅ Puntuación total: {puntuacion_total} puntos")
    st.markdown(f"⏱️ Tiempo total: {tiempo_total} segundos")
    st.markdown("📦 Enviando datos a Monday...")

    success, msg = enviar_a_monday(datos, api_key="eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjI5NzQ5NDgyNCwiYWFpIjoxMSwidWlkIjo0NDIyNjMxNiwiaWFkIjoiMjAyMy0xMS0yMFQxNzowNjozNC4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6MTY4ODEzMjIsInJnbiI6ImV1YzEifQ.o1cqRb0B9pGxLS2PQQbU4_RkQlhW3GhGVkGUV3xiCxI", board_id=1939525964)

    if success:
        st.success("✅ Entrevista enviada correctamente a Monday.")
    else:
        st.error(f"❌ Hubo un problema al enviar la entrevista a Monday: {msg}")


def main():
    if "pagina" not in st.session_state:
        st.session_state.pagina = "login"

    if st.session_state.pagina == "login":
        login()
    elif st.session_state.pagina == "rol":
        pantalla_rol()
    elif st.session_state.pagina == "datos":
        pantalla_datos()
    elif st.session_state.pagina == "entrevista":
        entrevista()
    elif st.session_state.pagina == "resultados":
        mostrar_resultados()


if __name__ == "__main__":
    main()