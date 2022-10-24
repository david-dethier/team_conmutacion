from geopy.geocoders import Nominatim


def run(*args):

    nominatim_dir = " ".join(args) + " La Pampa"

    geolocator = Nominatim(user_agent=f"GIS CARD RACING ARG")

    location = geolocator.geocode(
        nominatim_dir,
        addressdetails=True,
        namedetails=True,
    )

    print(location)
