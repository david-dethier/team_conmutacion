import re
from typing import Optional
from bs4 import BeautifulSoup
from django.core.exceptions import ObjectDoesNotExist
from api.v1.gis.models import CiudadModel
from api.v1.red.models import Nodo

REGEX_PORCENTAJE = r"(\d{1,3}\.\d{0,2})"
REGEX_sanitize_ENTEROS = r"[-_\n]"


def parse_data_info_de_nodo(info_de_nodo: dict) -> list | None:
    soup = BeautifulSoup(info_de_nodo["data"], features="html.parser")
    tabla = soup.find("table", attrs={"class": "caidasdiarias"})

    if tabla is None:
        return None

    rows = tabla.findAll("tr")[1:]

    if rows == []:
        return None

    datalist = []

    for row in rows:

        cells = row.findAll(["td", "th"])

        if cells == []:
            return None

        modems_online = sanitize_somechars_data(cells[2].text)
        modems_offline = sanitize_somechars_data(cells[3].text)
        denominacion = cells[1].text.strip().upper()
        datalist.append(
            {
                "chasis": sanitize_somechars_data(cells[0].text).upper(),
                "denominacion": denominacion,
                "modems_online": 0 if modems_online == "" else int(modems_online),
                "modems_offline": 0 if modems_offline == "" else int(modems_offline),
                "modems_percent_online": sanitize_percentil_data(cells[4].text),
                "ciudad": resolve_ciudad_by_nodo(denominacion),
            }
        )

    return datalist


def sanitize_somechars_data(data: str) -> str:
    sanitize = re.sub(REGEX_sanitize_ENTEROS, " ", data).strip()
    return sanitize


def sanitize_percentil_data(data: str) -> float:
    if data == "":
        return 0.0
    return float(re.search(REGEX_PORCENTAJE, data.strip()).group(1))


def resolve_ciudad_by_nodo(
    denominacion: str, ciudad_default: Optional[str] = "Santa Rosa"
) -> int:
    try:
        nodo_obj = Nodo.objects.get(denominacion__iexact=denominacion)
        return nodo_obj.ciudad.id
    except ObjectDoesNotExist:
        if "catrilo" in denominacion.lower():
            return CiudadModel.objects.get(nombre__iexact="catrilo").id
        else:
            return CiudadModel.objects.get(nombre__iexact=ciudad_default).id
