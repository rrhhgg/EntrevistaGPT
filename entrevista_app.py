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

    datos = {
        "nombre": st.session_state.nombre,
        "telefono": st.session_state.telefono,
        "correo": st.session_state.correo,
        "via": st.session_state.via,
        "nombre_via": st.session_state.nombre_via,
        "numero": st.session_state.numero,
        "puerta": st.session_state.puerta,
        "cp": st.session_state.cp,
        "ciudad": st.session_state.ciudad,
        "entrevistador_email": st.session_state.email,
        "rol": st.session_state.rol,
        "puntuacion_total": total_puntos,
        "evaluacion_final": "Ejemplo de evaluación final",
        "tiempo_total": sum(st.session_state.tiempos),
        "puntuaciones": [7]*13,
        "evaluaciones": ["Evaluación automática"]*13
    }

    st.write("📦 Enviando datos a Monday...")
    st.write(datos)

    try:
        from enviar_a_monday import enviar_a_monday
        enviar_a_monday(datos)
        st.session_state.envio_ok = True
        st.write("✅ Enviado correctamente")
    except Exception as e:
        st.session_state.envio_ok = False
        st.write("❌ Error al enviar")
        st.write(e)

    st.session_state.pagina_actual = "envio"