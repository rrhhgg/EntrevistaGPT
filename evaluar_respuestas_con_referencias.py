
import openai
import json
import re

def evaluar_con_openai_con_referencias(respuesta, pregunta, respuestas_tipo, rol, info=None):
    contexto = f"Información adicional relevante para esta pregunta: {info}" if info else "Sin información adicional relevante."

    prompt = f"""Eres un selector experto de personal en hostelería.

Estás evaluando la respuesta de un candidato al puesto de {rol}.

Pregunta: {pregunta}
{contexto}

Respuesta del candidato:
{respuesta}

Respuestas tipo buenas esperadas:
- {'\n- '.join(respuestas_tipo.get('buenas', []))}

Respuestas tipo malas comunes:
- {'\n- '.join(respuestas_tipo.get('malas', []))}

Evalúa la respuesta del candidato teniendo en cuenta tanto las respuestas tipo como la información adicional. 

Devuelve:
1. Una puntuación del 0 al 10 (solo el número).
2. Una justificación breve (máximo 2 líneas).

Formato de salida:
{
  "puntuacion": número,
  "justificacion": "texto"
}
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
