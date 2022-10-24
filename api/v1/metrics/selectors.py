import requests

from requests import Session
from rest_framework import status


def fetch_eventos_de_nodos() -> dict:

    URL = "https://nodos.cpesr.com.ar/eventonodo/tabla_eventos"

    response = requests.get(URL)

    if response.status_code == status.HTTP_200_OK:
        return {"data": response.text, "status_code": status.HTTP_200_OK}
    else:
        return {"data": "", "status_code": response.status_code}


def fetch_detalle_evento_de_nodo(eventid: int) -> dict:
    URL = "https://nodos.cpesr.com.ar/eventonodo/detalle/" + str(eventid)

    response = requests.get(URL)

    if response.status_code == status.HTTP_200_OK:
        return {
            "data": response.text,
            "status_code": status.HTTP_200_OK,
            "eventid": eventid,
        }
    else:
        return {"data": "", "status_code": response.status_code, "eventid": eventid}


def fetch_llamadas_tecnicas(session: Session, data):
    url_endpoint_asterix = "https://www.usina.net.ar/llamadas_asterix.php"
    fecha = data["fecha"]
    payload_asterix = {
        "telefono": data["telefono"],
        "dia": fecha.day,
        "mes": fecha.month,
        "anio": fecha.year,
        "Submit": "Consultar",
    }

    asterix_response = session.post(url=url_endpoint_asterix, data=payload_asterix)
    return asterix_response.text
