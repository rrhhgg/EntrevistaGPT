
import requests
import json

def enviar_a_monday(datos, api_key, board_id):
    url = "https://api.monday.com/v2"

    headers = {
        "Authorization": api_key,
        "Content-Type": "application/json",
    }

    column_values = {
        "phone_mkqjgqhj": {"phone": datos["telefono"], "countryShortName": "ES"},
        "email_mkqjt99t": {"email": datos["correo"]},
        "dropdown_mkqjbykm": {"labels": [datos["via"]]},
        "text_mkqjmeh1": datos["nombre_via"],
        "numeric_mkqjjj0g": int(datos["numero"]) if datos["numero"].isdigit() else None,
        "text_mkqjwkmz": datos["puerta"],
        "numeric_mkqjwczq": int(datos["cp"]) if datos["cp"].isdigit() else None,
        "text_mkqjx0sz": datos["ciudad"],
        "multiple_person_mkqhdm94": {"personsAndTeams": [{"email": datos["entrevistador_email"]}]},
        "dropdown_mkqhgq7t": {"labels": [datos["rol"]]},
        "numeric_mkqhfqy3": datos["puntuacion_total"],
        "text_mkqhc1ck": datos["evaluacion_final"],
        "numeric_mkqjs2kq": datos["tiempo_total"]
    }

    for i, val in enumerate(datos["puntuaciones"]):
        if i < 5:
            column_values[f"numeric_mkqje1xr".replace("1", str(i+1))] = val
        else:
            column_values[f"numeric_mkqjax81".replace("1", str(i-4))] = val

    for i, val in enumerate(datos["evaluaciones"]):
        if i < 5:
            column_values[f"text_mkqjynvd".replace("1", str(i+1))] = val
        else:
            column_values[f"text_mkqjtv3j".replace("1", str(i-4))] = val

    column_values_str = json.dumps(column_values).replace('"', '\"')

    query = {
        "query": f"""mutation {{
            create_item (
                board_id: {board_id},
                item_name: "{datos["nombre"]}",
                column_values: "{column_values_str}"
            ) {{
                id
            }}
        }}"""
    }

    response = requests.post(url, headers=headers, data=json.dumps(query))
    if response.status_code == 200:
        result = response.json()
        if "errors" in result:
            print("❌ Error al enviar a Monday:")
            print(json.dumps(result, indent=2))
            return False
        else:
            print("✅ Enviado correctamente")
            return True
    else:
        print("❌ Error de red o autenticación:", response.status_code)
        print(response.text)
        return False
