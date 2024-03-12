import datetime

import functions_framework
import flask

from api import SwitchBotAPIRequestFailedError, SwitchBotApi
from settings import Settings

SETTINGS = Settings()


@functions_framework.http
def main(request: flask.Request) -> flask.Response:
    device_id = request.args.get("device_id")
    api = SwitchBotApi()

    try:
        thermal_info = api.get_thermal_info(device_id)
    except SwitchBotAPIRequestFailedError as e:
        return flask.Response(str(e), status=503)

    return thermal_info.model_dump_json()
