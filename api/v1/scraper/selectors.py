from bs4 import BeautifulSoup
import requests
from api.v1.logins.models import UserLoginModel
from api.v1.logins.services import login_droopy
from api.v1.gis.servicies import split_address
from rest_framework.exceptions import NotAuthenticated, ValidationError
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from rest_framework.reverse import reverse, reverse_lazy
from rest_framework.response import Response


class Droopy:

    URL_SERVICIOS_M3 = "http://192.168.100.40/serviciosM3.php"

    def authenticate(request):

        if not request.user.is_authenticated:
            raise NotAuthenticated(
                detail={
                    "No autenticado": f"Se requiere estar logueado en el sistema. Inicie sesion en {reverse_lazy('admin:login', request=request)}"
                }
            )

        with requests.Session() as session:

            try:
                login = UserLoginModel.objects.get(
                    user=request.user, site_name__iexact="droopy"
                )
                login_droopy(session, login)

            except ObjectDoesNotExist as error:
                raise ValidationError(
                    detail={
                        "ObjectDoesNotExist": f"No existe credencial de autenticacion Droopy para el usuario {request.user}."
                    }
                ) from error

        return session

    def fetch_servicio_m3_from_droopy(request, **kwargs) -> dict:
        """
        Obtiene de Droopy los datos de un servicio.
                Parameters:
                        **kwargs: apellidoM3, nombreM3, direccionM3, alturaM3, dptoM3, sucursalM3, idM3, nrotelM3, SubmitM3

                Returns:
                        Servicio (dict): 'idM3', 'apellidoM3', 'nombreM3', 'direccionM3', 'alturaM3', 'dptoM3', 'ciudad'
        """
        data = {}

        if not "SubmitM3" in kwargs:
            kwargs["SubmitM3"] = "Consultar M3"

        session = Droopy.authenticate(request)

        response = session.get(url=Droopy.URL_SERVICIOS_M3, params=kwargs)

        bs = BeautifulSoup(response.text, features="html.parser")

        data_first_row = (
            bs.find("td", string="Ciudad").findParent().findNext("tr").findAll("td")
        )

        ciudad = data_first_row[4].string
        direccion = data_first_row[3].string
        nombre = data_first_row[2].string
        apellido = data_first_row[1].string
        cuentanro = data_first_row[0].string

        address_group = split_address(direccion)

        data = {
            "idM3": cuentanro,
            "apellidoM3": apellido,
            "nombreM3": nombre,
            "direccionM3": address_group[0],
            "alturaM3": address_group[1],
            "dptoM3": address_group[2],
            "ciudad": ciudad,
        }

        return data


class M3Web:

    URL_M3WEB = "http://192.168.0.26:8095/"

    def fetch_reclamos_abiertos_m3_from_m3web():
        """
        Obtiene los reclamos abiertos (solo M3) desde el M3Web.

                Returns:
                        Reclamos List[dict]
        """
        response = requests.get(M3Web.URL_M3WEB, stream=True)

        bs = BeautifulSoup(response.text, features="html.parser")

        reclamos = bs.find(id="mytable").find("tbody").findAll("tr")
        encabezados = bs.find(id="mytable").find("thead").findAll("th")

        keys = [e.get_text(strip=True).lower() for e in encabezados]

        keys.pop(0)
        keys.pop()

        result = []

        for reclamo in reclamos:
            values = [v.get_text(strip=True) for v in reclamo.findAll("td")]

            values.pop(0)
            values.pop()

            result.append(dict(zip(keys, values)))

        return result
