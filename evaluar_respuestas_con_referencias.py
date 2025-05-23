import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def evaluar_con_openai_con_referencias(respuesta_candidato, pregunta, respuestas_tipo, rol):
    prompt = f"""
Eres un evaluador de entrevistas de selección para el puesto de {rol.upper()}.

A continuación, te doy una pregunta, cinco respuestas tipo (del 1 al 5) y la respuesta de un candidato.

Tu tarea es:

1. Analizar la respuesta del candidato.
2. Compararla con las cinco respuestas tipo.
3. Elegir cuál se le parece más (del 1 al 5).
4. Asignar la puntuación correspondiente:
   - Respuesta 1: 10 puntos
   - Respuesta 2: 8 puntos
   - Respuesta 3: 6 puntos
   - Respuesta 4: 4 puntos
   - Respuesta 5: 2 puntos
5. Justificar brevemente tu decisión.

---

Pregunta: {pregunta}

Respuestas tipo:
1. {respuestas_tipo[0]}
2. {respuestas_tipo[1]}
3. {respuestas_tipo[2]}
4. {respuestas_tipo[3]}
5. {respuestas_tipo[4]}

---

Respuesta del candidato:
{respuesta_candidato}

---

Devuélveme:
- La puntuación (solo el número).
- El número de la respuesta tipo más similar.
- Una breve justificación.
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=300
        )

        content = response.choices[0].message["content"]
        puntuacion = None
        justificacion = ""
        tipo_mas_parecido = ""

        for line in content.splitlines():
            if line.lower().startswith("puntuación:"):
                puntuacion = int(line.split(":")[1].strip())
            elif line.lower().startswith("evaluación:"):
                justificacion = line.split(":", 1)[1].strip()
            elif line.lower().startswith("el número de la respuesta tipo"):
                tipo_mas_parecido = line.split(":")[1].strip()

        if puntuacion is None:
            puntuacion = 0
            justificacion = "No se pudo interpretar una puntuación."

        return puntuacion, justificacion

    except Exception as e:
        return 0, f"❌ Error al evaluar con IA: {str(e)}"