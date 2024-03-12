""" APIテスト

.envに指定されている認証情報とデバイスIDを利用して通るかどうかだけテスト
（実際にリクエストするのであまり良くない。。ロジックの精緻なテストと言うより、手動でポチポチpython -mするのを避ける用）
"""

import os
from api import SwitchBotApi as API

TEST_TARGET_DEVICE_ID = os.environ.get("TEST_TARGET_DEVICE_ID", None)


def test_get_thermal_info():
    api = API()

    # テスト対象のデバイスIDを取得する
    if TEST_TARGET_DEVICE_ID is None:
        raise ValueError("テスト用デバイスIDが指定されていません。.envにTEST_TARGET_DEVICE_IDを指定してください。")
    device_id = TEST_TARGET_DEVICE_ID

    # 温度を取得する
    result = api.get_thermal_info(device_id)

    # 結果を検証する
    assert -10 <= result.temperature <= 50, "それっぽい温度が取れている"
    assert 0 <= result.temperature <= 100, "それっぽい湿度が取れている"


def test_get_devices():
    api = API()

    result = api.get_devices()

    assert len(result) > 0, "デバイスが取れている"
