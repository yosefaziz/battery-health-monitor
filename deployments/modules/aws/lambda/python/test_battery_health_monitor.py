import unittest
import json
from http import HTTPStatus
from unittest.mock import patch
from battery_health_monitor import (
    get_payload_bytes,
    decode_unix_timestamp,
    decode_state,
    decode_state_of_charge,
    decode_battery_temperature,
    decode_payload,
    main,
)

INPUT_1 = {"device": "foo", "payload": "F1E6E63676C75000"}
OUTPUT_1 = {
    "device": "foo",
    "time": 1668181615,
    "state": "error",
    "state_of_charge": 99.5,
    "temperature": 20.0,
}

INPUT_2 = {"device": "bar", "payload": "9164293726C85400"}
OUTPUT_2 = {
    "device": "bar",
    "time": 1668453961,
    "state": "discharge",
    "state_of_charge": 100.0,
    "temperature": 22.0,
}

INPUT_3 = {"device": "baz", "payload": "6188293726C75C00"}
OUTPUT_3 = {
    "device": "baz",
    "time": 1668454534,
    "state": "discharge",
    "state_of_charge": 99.5,
    "temperature": 26.0,
}

TEST_CASES = [
    {"input": INPUT_1, "output": OUTPUT_1},
    {"input": INPUT_2, "output": OUTPUT_2},
    {"input": INPUT_3, "output": OUTPUT_3},
]

BYTES_CASE_1 = b"\xf1\xe6\xe66v\xc7P\x00"

SUCCESSFUL_RETURN = {
    "statusCode": HTTPStatus.OK.value,
    "body": json.dumps("Successfully processed event"),
}


class TestBatteryHealthMonitor(unittest.TestCase):
    """Unit Test Class for the Battery Health Monitoring Lambda Function"""

    def test_get_payload_bytes(self):
        self.assertEqual(get_payload_bytes(INPUT_1["payload"]), BYTES_CASE_1)

    def test_decode_unix_timestamp(self):
        self.assertEqual(decode_unix_timestamp(BYTES_CASE_1), 1668181615)

    def test_decode_state(self):
        self.assertEqual(decode_state(BYTES_CASE_1), "error")

    def test_decode_state_of_charge(self):
        self.assertEqual(decode_state_of_charge(BYTES_CASE_1), 99.5)

    def test_decode_battery_temperature(self):
        self.assertEqual(decode_battery_temperature(BYTES_CASE_1), 20.0)

    def test_decode_payload(self):
        for case in TEST_CASES:
            self.assertEqual(
                decode_payload(
                    case["input"]["payload"], case["input"]["device"]
                ),
                case["output"],
            )

    def test_main(self):
        for case in TEST_CASES:
            with patch(
                "battery_health_monitor.decode_payload"
            ) as mock_decode_payload:
                mock_decode_payload.return_value = case["output"]
                self.assertEqual(main(case["input"], None), SUCCESSFUL_RETURN)


if __name__ == "__main__":
    unittest.main()
