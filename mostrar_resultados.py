from evaluar_respuestas_con_referencias import evaluar_con_openai_con_referencias
from respuestas_tipo import RESPUESTAS_TIPO
from generar_column_values import generar_column_values_con_evaluacion
from enviar_a_monday import enviar_resultados_monday

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