import requests
import os

MONDAY_API_KEY = os.getenv("MONDAY_API_KEY")
BOARD_ID = 1939525964

HEADERS = {
    "Authorization": MONDAY_API_KEY,
    "Content-Type": "application/json"
}

def formatear_telefono(telefono):
    if not telefono.startswith("+"):
        return "+34" + telefono.strip()
    return telefono

def enviar_resultados_monday(session):
    try:
        nombre = session.nombre
        correo = session.correo
        telefono = formatear_telefono(session.telefono)
        entrevistador = session.entrevistador
        email_entrevistador = session.email
        rol = session.rol
        direccion = f"{session.via} {session.nombre_via}, Nº {session.numero}, Puerta {session.puerta}, CP {session.cp}, {session.ciudad}"
        tiempo_total = sum(session.tiempos)
        respuestas = session.respuestas

        mutation = {
            "query": f"""
                mutation {{
                  create_item (
                    board_id: {BOARD_ID},
                    item_name: "{nombre} - {rol}",
                    column_values: {{
                      "email": {{ "email": "{correo}", "text": "{correo}" }},
                      "phone": {{ "phone": "{telefono}", "countryShortName": "ES" }},
                      "text": "{direccion}",
                      "status": {{ "label": "{rol.capitalize()}" }},
                      "long_text": {{
                        "text": "Respuestas:\n{chr(10).join(respuestas)}"
                      }},
                      "numbers": {tiempo_total},
                      "person": {{ "email": "{email_entrevistador}" }}
                    }}
                  ) {{
                    id
                  }}
                }}
            """
        }

        response = requests.post("https://api.monday.com/v2", json=mutation, headers=HEADERS)

        if response.status_code == 200:
            data = response.json()
            if "errors" in data:
                return False, f"Error de GraphQL: {data['errors']}"
            return True, "✅ Entrevista enviada correctamente a Monday."
        else:
            return False, f"Error HTTP: {response.status_code} - {response.text}"

    except Exception as e:
        return False, f"❌ Error al enviar a Monday: {str(e)}"