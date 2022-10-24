import re
import requests

from requests import Session
from datetime import datetime

from django.core import signing
from django.utils import timezone

from rest_framework.exceptions import APIException

from api.v1.metrics.selectors import fetch_llamadas_tecnicas
from api.v1.metrics.models.llamadas_tecnicas import LlamadasTecnicasModel
from api.v1.metrics.serializers.llamadas_tecnicas import CallModelSerializer
from api.v1.logins.models import UserLoginModel
from api.v1.logins import services as login_services
from bs4 import BeautifulSoup

REGEX_PORCENTAJE = r"(\d{1,3}\.\d{0,2})"


def parse_llamadas_tecnicas(request_data):
    with requests.Session() as session:

        login = UserLoginModel.objects.get(
            site_name__iexact="droopy", username__iexact="dethierd"
        )

        login_services.login_droopy(session, login)

        serializer = CallModelSerializer(data=request_data)

        if serializer.is_valid(True):
            list_html = fetch_llamadas_tecnicas(session, serializer.validated_data)
            saved_data = parse_asterixpage_and_save_operatorcalls(
                list_html,
                serializer.validated_data["telefono"],
                serializer.validated_data["fecha"],
            )

        return saved_data


def parse_asterixpage_and_save_operatorcalls(
    llamadas_asterix_page, telefono, fecha, by_pass_save=False
):
    soup = BeautifulSoup(llamadas_asterix_page, features="html.parser")
    list_calls = []
    rows = soup.find_all("tr")

    for row in rows[2:-1]:

        cells = row.find_all("td")

        model = LlamadasTecnicasModel()
        model.telefono = telefono
        model.fecha = str(fecha)
        model.fecha_detalle = datetime.strptime(
            cells[0].text, "%Y-%m-%d %H:%M:%S"
        ).replace(tzinfo=timezone.get_current_timezone())
        model.origen_src = cells[1].text
        model.destino_dst = cells[2].text
        model.canal_channel = cells[3].text
        model.canal_destino_dstchannel = cells[4].text
        model.estado_disposition = cells[5].text
        model.id_unico = cells[6].text
        model.grabacion = cells[7].a.attrs["href"]

        if by_pass_save == False:
            try:
                m, c = LlamadasTecnicasModel.objects.get_or_create(
                    id_unico=model.id_unico,
                    defaults={
                        "telefono": model.telefono,
                        "fecha": model.fecha,
                        "fecha_detalle": str(model.fecha_detalle),
                        "origen_src": model.origen_src,
                        "destino_dst": model.destino_dst,
                        "canal_channel": model.canal_channel,
                        "canal_destino_dstchannel": model.canal_destino_dstchannel,
                        "estado_disposition": model.estado_disposition,
                        "id_unico": model.id_unico,
                        "grabacion": model.grabacion,
                    },
                )

                print(f"{m}   :   {c}")

            except APIException as exc:
                print(exc)

        list_calls.append(
            {
                "telefono": model.telefono,
                "fecha": model.fecha,
                "fecha_detalle": str(model.fecha_detalle),
                "origen_src": model.origen_src,
                "destino_dst": model.destino_dst,
                "canal_channel": model.canal_channel,
                "canal_destino_dstchannel": model.canal_destino_dstchannel,
                "estado_disposition": model.estado_disposition,
                "id_unico": model.id_unico,
                "grabacion": model.grabacion,
            }
        )

    return list_calls


# def login_droopy(session: Session, login) -> Session:
#     payload_login = {
#         "txtusuario": login.username,
#         "txtclave": signing.loads(login.password),
#         "Submit": "Enviar",
#     }

#     validar_sesion_response = session.post(
#         "https://www.usina.net.ar/validar_sesion.php", data=payload_login
#     )
#     print(validar_sesion_response.status_code)


def parse_data_evento_de_nodo_equipos_afectados(
    detalle_de_evento: dict,
) -> list | None:
    soup = BeautifulSoup(detalle_de_evento["data"], features="html.parser")
    tabla = soup.find("table", attrs={"class": "caidasdiarias"})

    if tabla is None:
        return None

    rows = tabla.findAll("tr")[1:]

    if rows is []:
        return None

    datalist = []
    for row in rows:
        cells = row.findAll("td")[:-1]

        if cells is []:
            return None

        if cells[6].text == "":
            online_datetime = None
        else:
            online_datetime = str(
                datetime.strptime(cells[6].text, "%Y-%m-%d %H:%M:%S").replace(
                    tzinfo=timezone.get_current_timezone()
                )
            )

        datalist.append(
            {
                "evento": int(detalle_de_evento["eventid"]),
                "macaddress": cells[0].text,
                "model": cells[1].text,
                "cuenta": cells[2].text,
                "domicilio": cells[3].text,
                "estado_provisioning": cells[4].text,
                "email": cells[5].text,
                "online_datetime": online_datetime,
            }
        )

    return datalist


def parse_data_evento_de_nodo(info_de_evento: dict, eventos_ignorados: list) -> list | None:
    soup = BeautifulSoup(info_de_evento["data"], features="html.parser")
    tabla = soup.find("table", attrs={"class": "caidasdiarias"})

    if tabla is None:
        return None

    rows = tabla.findAll("tr")[1:]

    if rows is []:
        return None

    datalist = []
    for row in rows:
        cells = row.findAll("td")[:-1]

        if cells is []:
            return None

        # Solo se parsearan los nuevos eventos que aun no hayan finalizado.
        # El resto ya esta almacenado en la bd.
        if int(cells[0].text) in eventos_ignorados:
            print(f"Se ignoro el evento {cells[0].text}")
            continue

        if cells[2].text == "":
            inicio = None
        else:
            inicio = str(
                datetime.strptime(cells[2].text, "%Y-%m-%d %H:%M:%S").replace(
                    tzinfo=timezone.get_current_timezone()
                )
            )

        if cells[4].text == "":
            fin = None
        else:
            fin = str(
                datetime.strptime(cells[4].text, "%Y-%m-%d %H:%M:%S").replace(
                    tzinfo=timezone.get_current_timezone()
                )
            )
        datalist.append(
            {
                "eventid": cells[0].text,
                "nodo": cells[1].text,
                "inicio": inicio,
                "antiguedad": cells[3].text,
                "fin": fin,
                "duracion": cells[5].text,
                "tipo": cells[6].text,
                "estado": cells[7].text,
                "equipos_afectados": cells[8].findAll("span")[2:][0].text,
                "equipos_caidos": cells[8].findAll("span")[:1][0].text,
                "porcentaje_online": re.search(REGEX_PORCENTAJE, cells[9].text).group(
                    1
                ),
            }
        )

    return datalist

