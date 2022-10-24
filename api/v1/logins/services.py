from requests import Response, Session, session
from django.core import signing

def login_droopy(session: Session, login) -> Response:
    payload_login = {
        "txtusuario": login.username,
        "txtclave": signing.loads(login.password),
        "Submit": "Enviar",
    }

    post_response = session.post(
        "https://www.usina.net.ar/validar_sesion.php", data=payload_login
    )
    return post_response
    # print(validar_sesion_response.status_code)