from evaluar_respuestas_con_referencias import evaluar_con_openai_con_referencias
from respuestas_tipo import RESPUESTAS_TIPO

ID_COLUMNAS = {
    "generales": {
        "puntuacion": [
            "numeric_mkqje1xr", "numeric_mkqj583y", "numeric_mkqjtmhs",
            "numeric_mkqjp912", "numeric_mkr6njmm"
        ],
        "evaluacion": [
            "text_mkqjynvd", "text_mkqjq3x5", "text_mkqjvc1p",
            "text_mkqj3t0k", "text_mkr6bc04"
        ]
    },
    "camarero": {
        "puntuacion": [
            "numeric_mkqjax81", "numeric_mkqj4hff", "numeric_mkqjx55q",
            "numeric_mkqjx2t", "numeric_mkqjyb6b", "numeric_mkqj34xs",
            "numeric_mkqjsyt6", "numeric_mkqjbvax"
        ],
        "evaluacion": [
            "text_mkqjtv3j", "text_mkqj5mt8", "text_mkqjqx0q",
            "text_mkqjbfd8", "text_mkqjx2qd", "text_mkqj998e",
            "text_mkqjks1c", "text_mkqjdwx5"
        ]
    }
}

def generar_column_values_con_evaluacion(preguntas_generales, preguntas_especificas, respuestas, rol):
    column_values = {}
    total_preguntas_generales = len(preguntas_generales)

    for i, pregunta in enumerate(preguntas_generales):
        respuesta = respuestas[i]
        respuestas_tipo = RESPUESTAS_TIPO.get(rol, {}).get(pregunta, [])
        if respuestas_tipo:
            puntuacion, evaluacion = evaluar_con_openai_con_referencias(
                respuesta, pregunta, respuestas_tipo, rol
            )
        else:
            puntuacion, evaluacion = 0, "No se pudo evaluar: faltan respuestas tipo para esta pregunta."
        column_values[ID_COLUMNAS["generales"]["puntuacion"][i]] = puntuacion
        column_values[ID_COLUMNAS["generales"]["evaluacion"][i]] = evaluacion

    for j, pregunta in enumerate(preguntas_especificas):
        respuesta = respuestas[j + total_preguntas_generales]
        respuestas_tipo = RESPUESTAS_TIPO.get(rol, {}).get(pregunta, [])
        if respuestas_tipo:
            puntuacion, evaluacion = evaluar_con_openai_con_referencias(
                respuesta, pregunta, respuestas_tipo, rol
            )
        else:
            puntuacion, evaluacion = 0, "No se pudo evaluar: faltan respuestas tipo para esta pregunta."
        column_values[ID_COLUMNAS[rol]["puntuacion"][j]] = puntuacion
        column_values[ID_COLUMNAS[rol]["evaluacion"][j]] = evaluacion

    return column_values