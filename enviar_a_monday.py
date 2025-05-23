
import requests
import json

def enviar_a_monday(datos, api_key, board_id):
    url = "https://api.monday.com/v2"
    headers = {
        "Authorization": api_key,
        "Content-Type": "application/json"
    }

    entrevistador_ids = {
        "frmichelin@grupogomez.es": 44226316,
        "m.demiguel@grupogomez.es": 44226317,
        "a.alandi@grupogomez.es": 44226318,
        "c.domenech@grupogomez.es": 44226319,
        "maria.martin@grupogomez.es": 44226320,
        "v.cobusneanu@grupogomez.es": 44226321,
        "j.barzola@grupogomez.es": 44226322,
        "v.gomez@grupogomez.es": 44226323,
        "mada.broton@grupogomez.es": 44226324
    }

    entrevistador_email = datos["entrevistador_email"]
    entrevistador_id = entrevistador_ids.get(entrevistador_email, None)

    if not entrevistador_id:
        print(f"❌ No se encontró ID de entrevistador para {entrevistador_email}")
        return False

    telefono = datos["telefono"]
    if not telefono.startswith("+"):
        telefono = "+34" + telefono.lstrip("0")

    column_values = {
        "multiple_person_mkqhdm94": {"personsAndTeams": [{"id": entrevistador_id, "kind": "person"}]},
        "dropdown_mkqhgq7t": {"labels": [datos["rol"].capitalize()]},
        "date": {"date": datos.get("fecha", "")},
        "numeric_mkqhfqy3": datos["puntuacion_total"],
        "text_mkqhc1ck": datos["evaluacion_final"],
        "dropdown_mkqjbykm": {"labels": [datos["via"]]},
        "text_mkqjmeh1": datos["nombre_via"],
        "numeric_mkqjjj0g": datos["numero"],
        "text_mkqjwkmz": datos["puerta"],
        "numeric_mkqjwczq": datos["cp"],
        "text_mkqjx0sz": datos["ciudad"],
        "phone_mkqjgqhj": {"phone": telefono, "countryShortName": "ES"},
        "email_mkqjt99t": {"email": datos["correo"], "text": datos["correo"]},
        "numeric_mkqjs2kq": datos["tiempo_total"]
    }

    for i in range(1, 6):
        num_id = ["e1xr", "583y", "tmhs", "p912", "6njmm"][i-1]
        text_id = ["ynvd", "q3x5", "vc1p", "3t0k", "r6bc04"][i-1]
        column_values[f"numeric_mkqj{num_id}"] = datos["puntuaciones"][i-1]
        column_values[f"text_mkqj{text_id}"] = datos["evaluaciones"][i-1]

    if datos["rol"] == "camarero":
        for i in range(8):
            num_id = ["ax81","4hff","x55q","x2t","yb6b","34xs","syt6","bvax"][i]
            text_id = ["tv3j","5mt8","qx0q","bfd8","x2qd","998e","ks1c","dwx5"][i]
            column_values[f"numeric_mkqj{num_id}"] = datos["puntuaciones"][i+5]
            column_values[f"text_mkqj{text_id}"] = datos["evaluaciones"][i+5]

    query = """
    mutation ($item_name: String!, $board_id: Int!, $column_values: JSON!) {
      create_item (
        item_name: $item_name,
        board_id: $board_id,
        column_values: $column_values
      ) {
        id
      }
    }
    """

    payload = {
        "query": query,
        "variables": {
            "item_name": datos["nombre"],
            "board_id": int(board_id),
            "column_values": json.dumps(column_values)
        }
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        print("📤 Payload enviado:", json.dumps(payload, indent=2))
        response.raise_for_status()
        print("📥 Respuesta de Monday:", response.text)
        return True
    except Exception as e:
        print(f"❌ Error al enviar a Monday: {e}")
        print("❌ Respuesta:", response.text if 'response' in locals() else "No hay respuesta")
        return False
