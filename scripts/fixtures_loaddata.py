import os
from django.core.management import call_command
from django.apps import apps

APPS_WITH_FIXTURES = ("metrics", "logins", "gis", "red")


def get_files(path):
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            yield file


def run():
    try:
        for app_name in APPS_WITH_FIXTURES:
            app_fixtures_path = os.path.join(
                apps.get_app_config(app_name).path, "fixtures"
            )
            for file in get_files(app_fixtures_path):
                print(file)
                call_command("loaddata", file)
    except Exception as e:
        print(e)
