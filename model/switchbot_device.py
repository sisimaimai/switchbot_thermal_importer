from __future__ import annotations
import datetime

from utils.logger import get_logger
from pydantic import BaseModel
import json


JST = datetime.timezone(datetime.timedelta(hours=+9), "JST")
LOGGER = get_logger(__name__)

class SwitchbotDevice(BaseModel):
    """SwitchBotのデバイス情報を格納するクラス
    """

    device_id: str
    device_name: str
    device_type: str
    enable_cloud_service: bool
    hub_device_id: str

    def __setattr__(self, name, value):
        if value is None:
            LOGGER.warning(f"Attribute '{name}' is set to None.")
        super().__setattr__(name, value)

    @staticmethod
    def from_json_devices(devices: str) -> list[SwitchbotDevice]:
        """
        JSONからSwitchBotDeviceオブジェクトのリストを作成します。

        Args:
            devices (str): デバイスを表すJSON文字列。

        Returns:
            List[SwitchBotDevice]: SwitchBotDeviceオブジェクトのリスト。

        Example:
            devices = '''
            [
                {
                    "deviceId": "123456",
                    "deviceName": "Thermostat",
                    "deviceType": "thermostat",
                    "enableCloudService": true,
                    "hubDeviceId": "789012"
                },
                {
                    "deviceId": "654321",
                    "deviceName": "Light Switch",
                    "deviceType": "switch",
                    "enableCloudService": false,
                    "hubDeviceId": "098765"
                }
            ]
            '''
            switchbot_devices = SwitchBotDevice.from_json_devices(devices)
        """
        devices_list = json.loads(devices)
        return [
            SwitchbotDevice(
                device_id=device.get("deviceId"),
                device_name=device.get("deviceName"),
                device_type=device.get("deviceType"),
                enable_cloud_service=device.get("enableCloudService"),
                hub_device_id=device.get("hubDeviceId"),
            )
            for device in devices_list
        ]
