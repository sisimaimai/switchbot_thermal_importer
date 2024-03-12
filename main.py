import functions_framework
import flask
from google.cloud import pubsub_v1

from api import SwitchBotAPIRequestFailedError, SwitchBotApi
from model.thermal_info import ThermalInfo
from settings import Settings
from utils.logger import get_logger

LOGGER = get_logger(__name__)
SETTINGS = Settings()


# TODO: リトライ処理
def get_swithbot_thermal_info(device_id: str) -> ThermalInfo:
    api = SwitchBotApi()

    return api.get_thermal_info(device_id)


def transfer_all(all_thermal_info: list[ThermalInfo]) -> None:
    """Pub/Sub経由ですべての温湿度データを送信する"""
    publisher = pubsub_v1.PublisherClient()
    messages = [
        thermal_info.model_dump_json().encode("utf-8")
        for thermal_info in all_thermal_info
    ]
    futures = [
        publisher.publish(SETTINGS.target_pubsub_topic_path, message)
        for message in messages
    ]

    for future in futures:
        LOGGER.debug(future.result())


@functions_framework.http
def main(request: flask.Request) -> flask.Response:
    device_ids = request.args.get("device_ids").split(",")
    LOGGER.info(f"device_ids: {device_ids}")

    # すべてのデバイスで温湿度データの取得
    try:
        all_thermal_info = [
            get_swithbot_thermal_info(device_id) for device_id in device_ids
        ]
    except SwitchBotAPIRequestFailedError as e:
        return flask.Response(str(e), status=503)

    # Pub/Subにデータを送信
    transfer_all(all_thermal_info)

    return flask.Response("OK", status=200)
