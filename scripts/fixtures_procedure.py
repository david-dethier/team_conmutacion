import re
import json
import timeit
from typing import Optional
import requests

from pathlib import Path
from datetime import date, timedelta, datetime

from django.utils import timezone
from rest_framework import status
from bs4 import BeautifulSoup

import api.v1.metrics as metrics
import api.v1.gis as gis
import api.v1.logins as logins
import api.v1.red as red
from api.v1.metrics.models.commons import CuadrillaTecnicaModel
from api.v1.metrics.serializers.llamadas_tecnicas import CallModelSerializer
from api.v1.metrics.services import login_droopy
from api.v1.metrics.selectors import fetch_llamadas_tecnicas

from api.v1.metrics.services import parse_asterixpage_and_save_operatorcalls
from api.v1.logins.models import UserLoginModel


REGEX_PORCENTAJE = r"(\d{1,3}\.\d{0,2})"


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def fetch_eventos_de_nodos() -> dict:

    URL = "https://nodos.cpesr.com.ar/eventonodo/tabla_eventos"

    response = requests.get(URL)

    if response.status_code == status.HTTP_200_OK:
        return {"text": response.text, "status_code": status.HTTP_200_OK}
    else:
        return {"text": "", "status_code": response.status_code}


def fetch_detalle_evento_de_nodo(eventid: int) -> dict:
    URL = "https://nodos.cpesr.com.ar/eventonodo/detalle/" + str(eventid)

    response = requests.get(URL)

    if response.status_code == status.HTTP_200_OK:
        return {
            "text": response.text,
            "status_code": status.HTTP_200_OK,
            "eventid": eventid,
        }
    else:
        return {"text": "", "status_code": response.status_code, "eventid": eventid}


def extract_data_detalle_eventos_de_nodos(input_data: dict) -> list | None:
    soup = BeautifulSoup(input_data["text"], features="html.parser")
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
                "eventid": input_data["eventid"],
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


def extract_data_eventos_de_nodos(input_data: dict) -> list | None:
    soup = BeautifulSoup(input_data["text"], features="html.parser")
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


class Fixture:

    BASE_DIR_METRICS = Path(metrics.__path__[0]).resolve()
    BASE_DIR_GIS = Path(gis.__path__[0]).resolve()
    BASE_DIR_LOGIN = Path(logins.__path__[0]).resolve()
    BASE_DIR_RED = Path(red.__path__[0]).resolve()

    URL_COMPLETEDWORKS_CONEX = "http://192.168.36.36/Recladisticas/estadisConx.php"
    URL_COMPLETEDWORKS_RECLAMOS = "http://192.168.36.36/Recladisticas/estadisRec.php"

    TECHNICALTEAMS = [
        ("C 11", "Cuadrilla 11", 5),
        ("C 12", "Cuadrilla 12", 5),
        ("C 13", "Cuadrilla 13", 5),
        ("C 14", "Cuadrilla 14", 5),
        ("C 15", "Cuadrilla 15", 5),
        ("C 16", "Cuadrilla 16", 5),
        ("C PODA1", "Poda 1", 4),
        ("C PODA2", "Poda 2", 4),
        ("C PODA3", "Poda 3", 4),
        ("C PODA4", "Poda 4", 4),
        ("C PODA5", "Poda 5", 4),
        ("C PODA6", "Poda 6", 4),
        ("C PODA7", "Poda 7", 4),
        ("C PODA8", "Poda 8", 4),
        ("CPETEL A", "Cpetel A", 2),
        ("CPETEL B", "Cpetel B", 2),
        ("CPETEL C", "Cpetel C", 2),
        ("CPETEL D", "Cpetel D", 2),
        ("CPETEL E", "Cpetel E", 2),
        ("C CATRILO", "Cpetel Catrilo", 2),
        ("C BEBE1", "Cuadrilla Bebenet 1", 2),
        ("VICTOR COSTILLA", "Victor Costilla", 2),
        ("PUHL", "Puhl", 3),
        ("CORRAL", "Corral", 3),
        ("GARCIA", "Garcia", 3),
        ("O LERY", "O'Lery", 3),
        ("LEYES", "Leyes", 3),
        ("CAPPELLO", "Cappello", 3),
        ("MIELGO", "Mielgo", 3),
        ("CUA TELEFONIA CONMUTACION", "Conmutacion", 2),
        ("GARANTIA PODA", "Garantia Poda", 4),
        ("GARANTIA REDES", "Garantia Redes", 4),
        ("ZONA_01", "Zona 1", 2),
        ("ZONA_02", "Zona 2", 2),
        ("ZONA_03", "Zona 3", 2),
        ("ZONA_04", "Zona 4", 2),
        ("ZONA_05", "Zona 5", 2),
        ("ZONA_06", "Zona 6", 2),
        ("ZONA_07", "Zona 7", 2),
        ("ZONA_08", "Zona 8", 2),
        ("ZONA_09", "Zona 9", 2),
        ("ZONA_10", "Zona 10", 2),
        ("CUADRILLA A DESIGNAR", "Cuadrilla a Designar", 2),
        ("LOWOCHE", "Zona Lowoche", 2),
        ("TOAY", "Toay", 2),
        ("GERMAN SAGO", "German Sago", 2),
        ("ASIGNAR A CPETEL", "Asignar a CpeTel", 2),
        ("GUILLERMO RONCO (SUPERVIS", "Guillermo Ronco (Supervisor)", 2),
        ("RICARDO FELICI (INGENIERI", "Ricardo Felici", 2),
    ]

    COMPANIES = [
        ("UNSET", "UNSET", "UNSET"),
        ("Cpetel", "Guillermo Ronco", "15667748"),
        ("Plantel Exterior", "German Leventan", "15740320"),
        ("Zamora", "Pablo Zamora", "15619410"),
        ("Redes AR", "Sarandon", "15329576"),
    ]

    OPERATORS_NUMBERS = [
        (3375, 3385),
        (3333, 3388),
        (3371, 3383),
        (3384, 3374),
        (3381, 3378),
        (3387, 3377),
        (3372, 3382),
    ]

    def run(self):
        ...

    def create_fixture_ciudades(self):
        """Orden de ejecucion = 3"""
        
        json_data = []
        cities = [("Santa Rosa", 6300), ("Toay", 6303), ("Catrilo", 6330)]

        for item in cities:
            json_data.append(
                {
                    "model": "gis.CiudadModel",
                    "pk": len(json_data) + 1,
                    "fields": {
                        "nombre": item[0],
                        "provincia": "La Pampa",
                        "cp": item[1],
                        "cpa": None,
                    },
                }
            )
        try:
            with open(self.BASE_DIR_GIS / "fixtures/Ciudades.json", "w") as outfile:
                outfile.write(json.dumps(json_data))
        except:
            print("create_fixtures_CiudadModel FAIL")
            raise Exception(outfile.errors)

        print("create_fixtures_CiudadModel OK")
        return True

    def create_fixture_eventos_de_nodos(self):
        json_data_base = []
        json_data_detail = []
        response_base_data = fetch_eventos_de_nodos()
        events_list = extract_data_eventos_de_nodos(response_base_data)
        for event_data in events_list:
            json_data_base.append(
                {
                    "model": "metrics.NodoEventoModel",
                    "fields": event_data,
                }
            )

            response_detail_data = fetch_detalle_evento_de_nodo(event_data["eventid"])
            details_list = extract_data_detalle_eventos_de_nodos(response_detail_data)

            for detail_data in details_list:
                json_data_detail.append(
                    {
                        "model": "metrics.NodoEventoEquipoAfectadoModel",
                        "pk": len(json_data_detail) + 1,
                        "fields": detail_data,
                    }
                )

        try:
            with open(
                self.BASE_DIR_METRICS
                / "fixtures/EventosDeNodosIncluyeEquiposAfectados.json",
                "w",
            ) as outfile:
                outfile.write(json.dumps(json_data_base))

        except:
            print("create_fixtures_NodoEventoModel FAIL")
            raise Exception(outfile.errors)

        try:

            with open(
                self.BASE_DIR_METRICS / "fixtures/NodoEventoEquipoAfectado.json", "w"
            ) as outfile:
                outfile.write(json.dumps(json_data_detail))

        except:
            print("create_fixtures_NodoEventoEquipoAfectadoModel FAIL")
            raise Exception(outfile.errors)

        print("create_fixtures_NodoEventoModel OK")
        print("create_fixtures_NodoEventoEquipoAfectadoModel OK")
        return True

    def create_fixture_cuadrillas_tecnicas(self):
        """Orden de ejecucion = 2"""

        json_data = []

        for team_key, team_alias, company_model in self.TECHNICALTEAMS:

            json_data.append(
                {
                    "model": "metrics.CuadrillaTecnicaModel",
                    "pk": len(json_data) + 1,
                    "fields": {
                        "name": team_key.upper(),
                        "alias": team_alias,
                        "company_model": company_model,
                        "is_in_service": True,
                    },
                }
            )

        try:
            with open(
                self.BASE_DIR_METRICS / "fixtures/2-CuadrillaTecnicaModel.json", "w"
            ) as outfile:
                outfile.write(json.dumps(json_data))
        except:
            print("create_fixtures_CuadrillaTecnicaModel FAIL")
            raise Exception(outfile.errors)

        print("create_fixtures_CuadrillaTecnicaModel OK")
        return True

    def create_fixture_empresas(self):
        """Orden de ejecucion = 1"""
        json_data = []

        for company_name, boss_name, work_phone in self.COMPANIES:

            json_data.append(
                {
                    "model": "metrics.EmpresaModel",
                    "pk": len(json_data) + 1,
                    "fields": {
                        "company_name": company_name,
                        "boss_name": boss_name,
                        "work_phone": work_phone,
                        "is_in_service": True,
                    },
                }
            )

        try:
            with open(
                self.BASE_DIR_METRICS / "fixtures/1-EmpresaModel.json", "w"
            ) as outfile:
                outfile.write(json.dumps(json_data))
        except:
            print("create_fixtures_EmpresaModel FAIL")
            raise Exception(outfile.errors)

        print("create_fixtures_EmpresaModel OK")
        return True

    def create_fixture_llamadas_tecnicas(self, days: Optional[int] = 30):

        with requests.Session() as session:
            starttime = timeit.default_timer()
            login = UserLoginModel.objects.get(
                site_name__iexact="droopy", username__iexact="dethierd"
            )

            login_droopy(session, login)
            print("LOGUEADO EN :", timeit.default_timer() - starttime)

            start_date = date.today() - timedelta(days)
            end_date = date.today()
            json_data = []

            for L1, L2 in self.OPERATORS_NUMBERS:
                starttime = timeit.default_timer()
                for single_date in daterange(start_date, end_date):
                    print(single_date.strftime("%Y-%m-%d"))

                    serializer_L1 = CallModelSerializer(
                        data={"telefono": L1, "fecha": single_date}
                    )
                    serializer_L2 = CallModelSerializer(
                        data={"telefono": L2, "fecha": single_date}
                    )

                    if serializer_L1.is_valid(True):
                        list_html = fetch_llamadas_tecnicas(
                            session, serializer_L1.validated_data
                        )
                        data_L1 = parse_asterixpage_and_save_operatorcalls(
                            list_html,
                            serializer_L1.validated_data["telefono"],
                            serializer_L1.validated_data["fecha"],
                            True,
                        )
                        for registry in data_L1:
                            print(f'{L1}    {single_date}    {registry["fecha"]}')

                            json_data.append(
                                {
                                    "model": "metrics.LlamadasTecnicasModel",
                                    "pk": len(json_data) + 1,
                                    "fields": registry,
                                }
                            )

                    if serializer_L2.is_valid(True):
                        list_html = fetch_llamadas_tecnicas(
                            session, serializer_L2.validated_data
                        )
                        data_L2 = parse_asterixpage_and_save_operatorcalls(
                            list_html,
                            serializer_L2.validated_data["telefono"],
                            serializer_L2.validated_data["fecha"],
                            True,
                        )

                        for registry in data_L2:
                            print(f'{L2}    {single_date}    {registry["fecha"]}')

                            json_data.append(
                                {
                                    "model": "metrics.LlamadasTecnicasModel",
                                    "pk": len(json_data) + 1,
                                    "fields": registry,
                                }
                            )

                print(
                    f"{L1} y {L2} FINALIZADOS EN :, {timeit.default_timer() - starttime}"
                )

            try:
                with open(
                    self.BASE_DIR_METRICS / "fixtures/LlamadasTecnicasModel.json", "w"
                ) as outfile:
                    outfile.write(json.dumps(json_data))
            except:
                print("create_fixtures_LlamadasTecnicasModel FAIL")
                raise Exception(outfile.errors)

            print("create_fixtures_LlamadasTecnicasModel OK")
            return True

    def create_fixture_conexiones_completedworks(self):
        """
        Para que se cree con exito el fixture,
        las siguientes tablas deben llenarse antes, en este orden:
        "metrics_empresa"
        "metrics_cuadrilla_tecnica"
        """
        start_date = date.today() - timedelta(30)
        end_date = date.today()
        json_data = []

        for single_date in daterange(start_date, end_date):

            data = requests.get(self.URL_COMPLETEDWORKS_CONEX, {"fecha": single_date})
            if data.content.decode("utf-8") == "":
                print(f'ERROR : No hay datos para esta fecha " {single_date} "')
                continue

            json_teams = json.loads(data.content)
            for team in json_teams:
                technicalteam_name = team["cuadrilla"].upper()

                technicalteam_queryset = CuadrillaTecnicaModel.objects.filter(
                    name=technicalteam_name
                )

                if not technicalteam_queryset.exists():
                    print(
                        f"ERROR : No se encontro technicalteam_name en la BD {technicalteam_name}/{team['cuadrilla']}"
                    )
                    continue

                json_data.append(
                    {
                        "model": "metrics.ConexionesCompletedWorkModel",
                        "pk": len(json_data) + 1,
                        "fields": {
                            "date": str(single_date),
                            "quantity": team["cantidad"],
                            "technical_team_id": technicalteam_queryset.values().first()[
                                "id"
                            ],
                        },
                    }
                )

        try:
            with open(
                self.BASE_DIR_METRICS / "fixtures/ConexionesCompletedWorks.json",
                "w",
            ) as outfile:
                outfile.write(json.dumps(json_data))
        except:
            print("create_fixtures_ConexionesCompletedWorkModel FAIL")
            raise Exception(outfile.errors)

        print("create_fixtures_ConexionesCompletedWorkModel OK")
        return True

    def create_fixture_reclamos_completedworks(self):
        """
        Para que se cree con exito el fixture,
        las siguientes tablas deben llenarse antes, en este orden:
        "metrics_empresa"
        "metrics_cuadrilla_tecnica"
        """

        start_date = date.today() - timedelta(30)
        end_date = date.today()
        json_data = []

        for single_date in daterange(start_date, end_date):

            data = requests.get(
                self.URL_COMPLETEDWORKS_RECLAMOS, {"fecha": single_date}
            )
            if data.content.decode("utf-8") == "":
                print(f'ERROR : No hay datos para esta fecha " {single_date} "')
                continue

            json_teams = json.loads(data.content)
            for team in json_teams:

                technicalteam_name = team["cuadrilla"].upper()
                technicalteam_queryset = CuadrillaTecnicaModel.objects.filter(
                    name=technicalteam_name
                )

                if not technicalteam_queryset.exists():
                    print(
                        f"ERROR : No se encontro technicalteam_name en la BD {technicalteam_name}/{team['cuadrilla']}"
                    )
                    continue

                json_data.append(
                    {
                        "model": "metrics.ReclamosCompletedWorkModel",
                        "pk": len(json_data) + 1,
                        "fields": {
                            "date": str(single_date),
                            "quantity": team["cantidad"],
                            "technical_team_id": technicalteam_queryset.values().first()[
                                "id"
                            ],
                        },
                    }
                )

        try:
            with open(
                self.BASE_DIR_METRICS / "fixtures/ReclamosCompletedWork.json", "w"
            ) as outfile:
                outfile.write(json.dumps(json_data))
        except:
            print("create_fixtures_ReclamosCompletedWorkModel FAIL")
            raise Exception(outfile.errors)

        print("create_fixtures_ReclamosCompletedWorkModel OK")
        return True
