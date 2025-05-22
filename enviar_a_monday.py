import requests
import streamlit as st

def enviar_a_monday(datos):
    api_key = st.secrets["monday_api_key"]
    board_id = 1939525964

    headers = {
        "Authorization": api_key,
        "Content-Type": "application/json"
    }

    mutation = {
        "query": f"""
        mutation {{
          create_item(
            board_id: {board_id},
            item_name: "{datos['nombre']}",
            column_values: {{
              "phone_mkqjgqhj": "{datos['telefono']}",
              "email_mkqjt99t": "{datos['correo']}",
              "dropdown_mkqjbykm": {{ "labels": ["{datos['via']}"] }},
              "text_mkqjmeh1": "{datos['nombre_via']}",
              "numeric_mkqjjj0g": {datos['numero']},
              "text_mkqjwkmz": "{datos['puerta']}",
              "numeric_mkqjwczq": {datos['cp']},
              "text_mkqjx0sz": "{datos['ciudad']}",
              "multiple_person_mkqhdm94": {{ "personsAndTeams": [{{ "email": "{datos['entrevistador_email']}" }}] }},
              "dropdown_mkqhgq7t": {{ "labels": ["{datos['rol']}"] }},
              "numeric_mkqhfqy3": {datos['puntuacion_total']},
              "text_mkqhc1ck": "{datos['evaluacion_final']}",
              "numeric_mkqjs2kq": {datos['tiempo_total']},
              "numeric_mkqje1xr": {datos['puntuaciones'][0]},
              "numeric_mkqj583y": {datos['puntuaciones'][1]},
              "numeric_mkqjtmhs": {datos['puntuaciones'][2]},
              "numeric_mkqjp912": {datos['puntuaciones'][3]},
              "numeric_mkr6njmm": {datos['puntuaciones'][4]},
              "numeric_mkqjax81": {datos['puntuaciones'][5]},
              "numeric_mkqj4hff": {datos['puntuaciones'][6]},
              "numeric_mkqjx55q": {datos['puntuaciones'][7]},
              "numeric_mkqjx2t": {datos['puntuaciones'][8]},
              "numeric_mkqjyb6b": {datos['puntuaciones'][9]},
              "numeric_mkqj34xs": {datos['puntuaciones'][10]},
              "numeric_mkqjsyt6": {datos['puntuaciones'][11]},
              "numeric_mkqjbvax": {datos['puntuaciones'][12]},
              "text_mkqjynvd": "{datos['evaluaciones'][0]}",
              "text_mkqjq3x5": "{datos['evaluaciones'][1]}",
              "text_mkqjvc1p": "{datos['evaluaciones'][2]}",
              "text_mkqj3t0k": "{datos['evaluaciones'][3]}",
              "text_mkr6bc04": "{datos['evaluaciones'][4]}",
              "text_mkqjtv3j": "{datos['evaluaciones'][5]}",
              "text_mkqj5mt8": "{datos['evaluaciones'][6]}",
              "text_mkqjqx0q": "{datos['evaluaciones'][7]}",
              "text_mkqjbfd8": "{datos['evaluaciones'][8]}",
              "text_mkqjx2qd": "{datos['evaluaciones'][9]}",
              "text_mkqj998e": "{datos['evaluaciones'][10]}",
              "text_mkqjks1c": "{datos['evaluaciones'][11]}",
              "text_mkqjdwx5": "{datos['evaluaciones'][12]}"
            }}
          ) {{
            id
          }}
        }}
        """
    }

    response = requests.post(
        url="https://api.monday.com/v2",
        json=mutation,
        headers=headers
    )

    if response.status_code == 200:
        st.success("✅ Entrevista enviada a Monday con éxito.")
    else:
        st.error(f"❌ Error al enviar a Monday: {response.text}")