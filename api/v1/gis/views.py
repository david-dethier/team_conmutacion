from rest_framework.response import Response

from api.v1.metrics import serializers
from .selectors import fetch_geolocation
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import status
from .models import DomicilioGeoLocalizadoModel
from .models import CiudadModel
from .serializers import CiudadSerializer
from .serializers import DomicilioGeoLocalizadoSerializer
from .selectors import fetch_geolocation
from api.v1.scraper import selectors as scraper_selectors
from django.core.cache import cache
from api.v1.gis import servicies as gis_services
from api.v1.gis import selectors as gis_selectors
from django.conf import settings
import itertools
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError
from django.core import serializers


class CiudadViewSet(viewsets.ModelViewSet):

    serializer_class = CiudadSerializer


class DomicilioGeolocalizadoViewSet(viewsets.ModelViewSet):

    serializer_class = DomicilioGeoLocalizadoSerializer
    search_fields = ["calle", "numero", "barrio"]

    queryset = DomicilioGeoLocalizadoModel.objects.all()

    def use_direccion_geolocalizada_from_cache(self, cachekey):
        """
        Obtiene el registro desde la cache.

                Returns:
                        False o el valor.
        """
        data = cache.get(cachekey)
        return False if data is None else data

    def use_direccion_geolocalizada_from_db(self, address, data):
        """
        Obtiene el registro desde la base de datos.

                Returns:
                        False o DomicilioGeoLocalizadoModel
        """
        try:
            ciudad = CiudadModel.objects.get(nombre__iexact=data["ciudad"])
        except ObjectDoesNotExist as error:
            raise ValidationError(
                {"ObjectDoesNotExist": f"Ciudad {data['ciudad']} no existe."}
            ) from error

        try:
            # print(f'{address["calle"]} {address["nro"]} {ciudad.id}')
            domiciliogeolocalizado = DomicilioGeoLocalizadoModel.objects.select_related(
                "ciudad"
            ).get(
                calle__iexact=address["calle"],
                numero=address["nro"],
                ciudad=ciudad.id,
            )
        except ObjectDoesNotExist:
            return False

        return domiciliogeolocalizado

    def extrae_suburb_from_response_location(self, location):
        """
        Extrae el nombre del barrio segun exista o no en de la respuesta del servicio de geolocalizacion.

                Returns:
                        Barrio (str)
        """
        return (
            location["data"]["address"]["suburb"]
            if "suburb" in location["data"]["address"].keys()
            else ""
        )

    def extrae_ciudad_from_response_location(self, location):
        """
        Extrae el nombre de ciudad segun el key 'city' o 'town' en de la respuesta del servicio de geolocalizacion.

                Returns:
                        city (dict): CiudadModel serializado
        """
        if not (
            "city" in location["data"]["address"].keys()
            or "town" in location["data"]["address"].keys()
        ):
            city = CiudadSerializer(
                CiudadModel.objects.filter(nombre__icontains="santa rosa").first()
            )
        elif "city" in location["data"]["address"].keys():
            city = CiudadSerializer(
                CiudadModel.objects.filter(
                    nombre__icontains=location["data"]["address"]["city"].replace(
                        "Municipio de ", ""
                    )
                ).first()
            )
        else:
            city = CiudadSerializer(
                CiudadModel.objects.filter(
                    nombre__icontains=location["data"]["address"]["town"].replace(
                        "Municipio de ", ""
                    )
                ).first()
            )

        return city

    @action(methods=["get"], detail=False)
    def geolocalizar_reclamos_activos_m3(self, request, *args, **kwargs):

        data_from_m3web = (
            scraper_selectors.M3Web.fetch_reclamos_abiertos_m3_from_m3web()
        )

        direcciones = []
        direcciones_create = []
        direcciones_sin_localizar_create = []
        for registro in data_from_m3web:

            address = dict(
                itertools.islice(registro.items(), 5, 8)
            )  # Solo 'calle', 'nro' y 'piso dpto'

            # Sanitize calle
            address["calle"] = address["calle"].replace("#", "ñ")

            data_from_droopy = scraper_selectors.Droopy.fetch_servicio_m3_from_droopy(
                request, idM3=registro["nro cuenta"]
            )

            cachekey = gis_services.generate_address_cachekey(
                address["calle"], address["nro"], data_from_droopy["ciudad"]
            )

            # Consulta el domicilio en cache y si existe, lo usa e itera hacia el proximo registro.
            in_cache = self.use_direccion_geolocalizada_from_cache(cachekey)

            if in_cache != False:
                direcciones.append(in_cache)
                print(f"Se encontro direccion en cache: {cachekey}")
                continue

            # Consulta el domicilio en la bd y si existe lo incorpora a la cache. Luego se usa e itera al proximo registro.
            in_db = self.use_direccion_geolocalizada_from_db(address, data_from_droopy)

            if in_db != False:
                geo_data = DomicilioGeoLocalizadoSerializer(in_db).data
                cache.set(cachekey, geo_data, settings.CACHE_TTL_GEOCODE)
                direcciones.append(geo_data)
                print(
                    f"Se encontro direccion en la bd, y se agrego direccion a la cache: {cachekey}"
                )
                continue

            # En este punto, se debe procesar la direccion ya que no existe en cache ni en la base de datos.
            location = gis_services.geolocalizar(
                address["calle"], address["nro"], data_from_droopy["ciudad"]
            )

            # Verifica si el servicio de GeoDecodificacion pudo obtener la ubicacion.
            # Si no pudo, itera al proximo registro.

            if location["data"] is None:

                try:
                    ciudad = CiudadModel.objects.get(
                        nombre__iexact=data_from_droopy["ciudad"]
                    )
                except ObjectDoesNotExist as error:
                    raise ValidationError(
                        {
                            "ObjectDoesNotExist": f"Ciudad {data_from_droopy['ciudad']} no existe."
                        }
                    ) from error

                geo_data_sin_localizar = {
                    "calle": address["calle"],
                    "numero": address["nro"],
                    "casa": address["piso depto"],
                    "barrio": "",
                    "googlemaps_link": "",
                    "ciudad": ciudad.id,
                    "calle_alias": "",
                    "has_alias": False,
                    "is_pending_alias": True,
                }

                direcciones_sin_localizar_create.append(geo_data_sin_localizar)
                print(location["message"])
                continue

            city = self.extrae_ciudad_from_response_location(location)
            suburb = self.extrae_suburb_from_response_location(location)

            geo_data = {
                "calle": address["calle"],
                "numero": address["nro"],
                "casa": address["piso depto"],
                "barrio": suburb,
                "latitud": location["data"]["latitude"],
                "longitud": location["data"]["longitude"],
                "googlemaps_link": gis_selectors.generate_googlemaps_link(
                    location["data"]["latitude"], location["data"]["longitude"]
                ),
                "ciudad": city.data["id"],
                "calle_alias": "",
                "has_alias": False,
                "is_pending_alias": False,
            }

            cache.set(
                cachekey,
                geo_data,
                settings.CACHE_TTL_GEOCODE,
            )

            print(f"Se agrego a la cache: {cachekey}")

            direcciones.append(geo_data)
            direcciones_create.append(geo_data)

        direcciones_create.extend(direcciones_sin_localizar_create)

        serializer: DomicilioGeoLocalizadoSerializer = self.get_serializer(
            data=direcciones_create, many=True
        )

        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return Response(direcciones, status.HTTP_200_OK)

    @action(methods=["get"], detail=False)
    def geolocalizar_nuevos_alias(self, request, *args, **kwargs):

        registros_pendientes = DomicilioGeoLocalizadoModel.objects.filter(
            is_pending_alias=True, has_alias=True
        )

        for registro in registros_pendientes:
            print(registro)

        registros_pendientes_json = serializers.serialize("json", registros_pendientes)

        return Response(registros_pendientes_json, status=status.HTTP_200_OK)
