import re
from subprocess import call

from api.v1.gis.selectors import REGEX_STRIP_DIRECCION
from api.v1.gis import selectors as gis_selectors


def split_address(address: str):
    """
    address [str]:
    calle, numero, ciudad
    """
    groups = re.match(
        "(?P<calle>^[\D]*)\s*(?P<altura>\d*)\s*(?P<casa>[\sa-zA-Z0-9]*)", address
    )

    return groups


def join_address(address: str, ciudad):
    return " ".join([address["calle"], address["nro"], address["piso depto"], ciudad])


'''
parametros ordenados
'''
def generate_address_cachekey(calle, nro, ciudad):
    return "_".join([calle, nro, ciudad]).replace(" ", "_").lower()


def geolocalizar(calle, altura, ciudad):

    location = gis_selectors.fetch_geolocation(
        calle=calle,
        numero=altura,
        ciudad=ciudad,
    )

    result = {
        "data": location,
        "message": f"Reverse Decode encontrado para {calle} {altura} {ciudad}",
    }

    if location is None:
        result[
            "message"
        ] = f"Reverse Decode no encontrado para {calle} {altura} {ciudad}"

    return result

    # serializer.save(
    #         latitud=location["latitude"],
    #         longitud=location["longitude"],
    #         calle=location["address"]["road"],
    #         barrio=location["address"]["suburb"],
    #     )
