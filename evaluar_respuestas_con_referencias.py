
import openai
import json
import re

def evaluar_respuesta(pregunta, respuesta_usuario, rol, respuesta_tipo=None):
    prompt = f"""Eres un selector experto de personal en hostelería.

Analiza la siguiente respuesta de un candidato al rol de {rol}.

Pregunta: {pregunta}
Respuesta del candidato: {respuesta_usuario}
Respuesta esperada o ideal (si aplica): {respuesta_tipo if respuesta_tipo else "No disponible"}

Devuelve en formato JSON dos cosas:
{{
  "puntuacion": número del 0 al 10 según la calidad de la respuesta,
  "evaluacion": una breve evaluación escrita de máximo 2 líneas
}}
"""

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        content = completion["choices"][0]["message"]["content"]

        # Buscar el JSON dentro del texto
        match = re.search(r"\{.*\}", content, re.DOTALL)
        if match:
            return json.loads(match.group())
        else:
            return {
                "puntuacion": 0,
                "evaluacion": "⚠️ No se pudo interpretar la respuesta del modelo"
            }

    except Exception as e:
        return {
            "puntuacion": 0,
            "evaluacion": f"⚠️ Error al evaluar: {str(e)}"
        }
