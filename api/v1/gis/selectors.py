from geopy.geocoders import Nominatim

REGEX_STRIP_DIRECCION = (
    r"(?P<calle>^[\D]*)\s*(?P<altura>\d*)\s*(?P<casa>[\sa-zA-Z0-9]*)"
)


def fetch_geolocation(
    calle: str, numero: int, ciudad: str, provincia: str = "La Pampa"
):
    geolocator = Nominatim(user_agent=f"GIS CARD RACING ARG")

    try:
        location = geolocator.geocode(
            f"{calle} {numero}, {ciudad}, {provincia}",
            addressdetails=True,
            namedetails=True,
        )
    except:
        location = None
        
    return (
        {
            "latitude": location.latitude,
            "longitude": location.longitude,
            "address": location.raw["address"],
        }
        if location
        else None
    )


def generate_googlemaps_link(lat: float, lng: float):
    return f"http://www.google.com/maps/place/{lat},{lng}"
