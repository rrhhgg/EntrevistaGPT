
import openai
import json
import re

def evaluar_con_openai_con_referencias(respuesta, pregunta, respuestas_tipo, rol, info=None):
    def limpiar(texto):
        return texto.replace("{", "{{").replace("}", "}}").replace('"', '\"').replace("\n", " ").strip()

    contexto = f"Información adicional relevante para esta pregunta: {limpiar(info)}" if info else "Sin información adicional relevante."

    buenas = respuestas_tipo.get("buenas", [])
    malas = respuestas_tipo.get("malas", [])

    def formato_ejemplo(lista):
        resultado = ""
        for r in lista:
            linea = f'- {r["texto"]}'
            if r.get("explicacion"):
                linea += f' /{r["explicacion"]}/'
            if r.get("puntuacion") is not None:
                linea += f' ({r["puntuacion"]})'
            resultado += limpiar(linea) + "\n"
        return resultado.strip()

    prompt = f"""Eres un selector experto de personal en hostelería.

Estás evaluando la respuesta de un candidato al puesto de {limpiar(rol)}.

Pregunta: {limpiar(pregunta)}
{contexto}

Respuesta del candidato:
{limpiar(respuesta)}

Respuestas tipo buenas esperadas:
{formato_ejemplo(buenas)}

Respuestas tipo malas comunes:
{formato_ejemplo(malas)}

Evalúa la respuesta del candidato teniendo en cuenta las respuestas tipo, sus explicaciones, las puntuaciones orientativas y el contexto. 

Devuelve:
1. Una puntuación del 0 al 10 (solo el número).
2. Una justificación breve (máximo 2 líneas).

Formato de salida:
{{
  "puntuacion": número,
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
