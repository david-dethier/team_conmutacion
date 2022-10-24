# from api.v1.logins.services import login_services
# import requests
# from api.v1.logins.models import UserLoginModel

# with requests.Session() as session:

#     login = UserLoginModel.objects.get(
#         site_name__iexact="droopy", username__iexact="dethierd"
#     )

#     login_services.login_droopy(session, login)