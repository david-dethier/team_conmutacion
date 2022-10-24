import requests
from rest_framework import status

def fetch_info_de_nodos() -> dict:
    URL = "https://nodos.cpesr.com.ar/caidasnodo/current"

    response = requests.get(URL)

    if response.status_code == status.HTTP_200_OK:
        return {"data": response.text, "status_code": status.HTTP_200_OK}
    else:
        return {"data": "", "status_code": response.status_code}