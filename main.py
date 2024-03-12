import functions_framework
import flask
from google.cloud import pubsub_v1

from api import SwitchBotAPIRequestFailedError, SwitchBotApi
from model.thermal_info import ThermalInfo
from settings import Settings
from utils.logger import get_logger

LOGGER = get_logger(__name__)
SETTINGS = Settings()


def get_swithbot_thermal_info(request: flask.Request) -> None:
    """SwitchBot APIを使って温湿度データを取得する"""
    device_id = request.args.get("device_id")
    api = SwitchBotApi()

    return api.get_thermal_info(device_id)


def publish_to_pubsub(thermal_info: ThermalInfo) -> None:
    """Pub/Subにデータを送信する"""
    publisher = pubsub_v1.PublisherClient()
    data = thermal_info.model_dump_json().encode("utf-8")
    future = publisher.publish(SETTINGS.target_pubsub_topic_path, data)
    LOGGER.debug(future.result())


@functions_framework.http
def main(request: flask.Request) -> flask.Response:
    # 温湿度データの取得
    try:
        thermal_info = get_swithbot_thermal_info(request)
    except SwitchBotAPIRequestFailedError as e:
        return flask.Response(str(e), status=503)

    # Pub/Subにデータを送信
    publish_to_pubsub(thermal_info)

    return flask.Response("OK", status=200)
