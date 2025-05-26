
import openai
import json
import re

def evaluar_con_openai_con_referencias(respuesta, pregunta, respuestas_tipo, rol):
    prompt = f"""Eres un selector experto de personal en hostelería.

Estás evaluando la respuesta de un candidato al puesto de {rol}.

Pregunta: {pregunta}
Respuesta del candidato: {respuesta}

Respuestas tipo esperadas:
- {'\n- '.join(respuestas_tipo)}

Evalúa la respuesta del candidato en base a las respuestas tipo y los criterios del puesto.

Devuelve:
1. Una puntuación del 0 al 10.
2. Una justificación breve (1 o 2 frases).

Formato:
{{
  "puntuacion": número entero,
  "justificacion": "texto"
}}
"""

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        content = completion["choices"][0]["message"]["content"]
        match = re.search(r"\{.*?\}", content, re.DOTALL)
        if match:
            resultado = json.loads(match.group())
            return resultado["puntuacion"], resultado["justificacion"]
        else:
            return 0, "⚠️ No se pudo interpretar la evaluación del modelo."

    except Exception as e:
        return 0, f"⚠️ Error al evaluar con OpenAI: {str(e)}"
