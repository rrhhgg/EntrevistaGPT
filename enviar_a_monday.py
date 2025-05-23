import requests
import streamlit as st
import json

def enviar_a_monday(datos):
    api_key = st.secrets["monday_api_key"]
    board_id = 1939525964

    headers = {
        "Authorization": api_key,
        "Content-Type": "application/json"
    }

    column_values = {
        "phone_mkqjgqhj": datos["telefono"],
        "email_mkqjt99t": datos["correo"],
        "dropdown_mkqjbykm": {"labels": [datos["via"]]},
        "text_mkqjmeh1": datos["nombre_via"],
        "numeric_mkqjjj0g": int(datos["numero"]) if datos["numero"].isdigit() else 0,
        "text_mkqjwkmz": datos["puerta"],
        "numeric_mkqjwczq": int(datos["cp"]) if datos["cp"].isdigit() else 0,
        "text_mkqjx0sz": datos["ciudad"],
        "multiple_person_mkqhdm94": {"personsAndTeams": [{"email": datos["entrevistador_email"]}]},
        "dropdown_mkqhgq7t": {"labels": [datos["rol"]]},
        "numeric_mkqhfqy3": datos["puntuacion_total"],
        "text_mkqhc1ck": datos["evaluacion_final"],
        "numeric_mkqjs2kq": datos["tiempo_total"]
    }

    for i in range(13):
        columna_p = f"numeric_mkq{'je1xr' if i==0 else 'j583y' if i==1 else 'jtmhs' if i==2 else 'jp912' if i==3 else 'r6njmm' if i==4 else 'jax81' if i==5 else 'j4hff' if i==6 else 'jx55q' if i==7 else 'jx2t' if i==8 else 'jyb6b' if i==9 else 'j34xs' if i==10 else 'jsyt6' if i==11 else 'jbvax'}"
        columna_e = f"text_mkq{'jynvd' if i==0 else 'jq3x5' if i==1 else 'jvc1p' if i==2 else 'j3t0k' if i==3 else 'r6bc04' if i==4 else 'jtv3j' if i==5 else 'j5mt8' if i==6 else 'jqx0q' if i==7 else 'jbfd8' if i==8 else 'jx2qd' if i==9 else 'j998e' if i==10 else 'jks1c' if i==11 else 'jdwx5'}"
        column_values[columna_p] = datos["puntuaciones"][i]
        column_values[columna_e] = datos["evaluaciones"][i]

    col_vals_str = json.dumps(column_values).replace('"', '\"')

    mutation = {
        "query": f"""
        mutation {{
            create_item (
                board_id: {board_id},
                item_name: "{datos["nombre"]}",
                column_values: "{col_vals_str}"
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
        st.error("❌ Error al enviar a Monday")
        st.write(response.text)