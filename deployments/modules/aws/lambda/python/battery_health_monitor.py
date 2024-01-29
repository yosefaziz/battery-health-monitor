import logging
from http import HTTPStatus
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)

STATE_MAP = {
    0: "power off",
    1: "power on",
    2: "discharge",
    3: "charge",
    4: "charge complete",
    5: "host mode",
    6: "shutdown",
    7: "error",
    8: "undefined",
}


def get_payload_bytes(payload_hex: str) -> bytes:
    """
    Converts the hexadecimal payload string into a bytes object.

    Args:
    - payload_hex: The hexadecimal payload string.

    Returns:
    - bytes: The payload bytes.
    """
    payload_bytes = bytes.fromhex(payload_hex)
    return payload_bytes


def decode_unix_timestamp(payload_bytes: bytes) -> int:
    """
    Extracts the timestamp from the payload bytes.
    The timestape is encoded on from the 4th to the 35th bit.

    Args:
    - payload_bytes: The payload bytes.

    Returns:
    - int: The unix timestamp.
    """
    # Get the first 5 bytes of the unsigned payload in little endian format
    time = int.from_bytes(payload_bytes[0:5], byteorder="little", signed=False)
    # Mask the first 35 bits. The minus 1 removes the 36th sign bit
    time &= (1 << 35) - 1
    # Shift the bits to the right by 4 to get the timestamp
    time >>= 4

    return time


def decode_state(payload_bytes: bytes) -> str:
    """
    Extracts the state from the payload bytes.
    The state is encoded on the 36th to the 39th bit.

    Args:
    - payload_bytes: The payload bytes.

    Returns:
    - str: The state.
    """
    # Right shift 4 bits from the 5th byte
    state = (payload_bytes[4] >> 4) & 0xF
    return STATE_MAP[state]


def decode_state_of_charge(payload_bytes: bytes) -> float:
    """
    Extracts the state of charge from the payload bytes.
    The state of charge is encoded on the 40th to the 47th bit.
    As the state of charge is a float with 0.5 precision, it was mulitplied by 2
    to store it as an integer.

    Args:
    - payload_bytes: The payload bytes.

    Returns:
    - float: The state of charge.
    """
    state_of_charge = payload_bytes[5] / 2.0
    if not -20.0 <= state_of_charge <= 100.0 or state_of_charge % 0.5 != 0:
        raise ValueError(
            "State of Charge out of range: must be between 0 and 100 "
            f"or a multiple of 0.5. Got: {state_of_charge}"
        )
    return state_of_charge


def decode_battery_temperature(payload_bytes: bytes) -> float:
    """
    Extracts the battery temperature from the payload bytes.
    The battery temperature is encoded on the 48th to the 55th bit.
    As the temperature is a float with 0.5 precision in between -20 and 100,
    it was mulitplied by 2 to store it as an integer.

    Args:
    - payload_bytes: The payload bytes.

    Returns:
    - float: The battery temperature.
    """
    temperature = (payload_bytes[6] / 2.0) - 20.0
    if not -20.0 <= temperature <= 100.0 or temperature % 0.5 != 0:
        raise ValueError(
            "Temperature out of range: must be between -20 and 100 "
            f"or a multiple of 0.5. Got: {temperature}"
        )

    return temperature


def decode_payload(payload_hex: str, device: str) -> dict:
    """
    Decodes the hexadecimal payload into a dictionary containing
    device, timestamp, state, state_of_charge, and temperature.

    Args:
    - payload_hex: The hexadecimal payload string.
    - device: The device name.

    Returns:
    - dict: Decoded data in the format:
      {
       "device": string,
       "time": integer,
       "state": string,
       "state_of_charge": float,
       "temperature": float
      }
    """
    payload_bytes = get_payload_bytes(payload_hex)
    time = decode_unix_timestamp(payload_bytes)
    state = decode_state(payload_bytes)
    state_of_charge = decode_state_of_charge(payload_bytes)
    temperature = decode_battery_temperature(payload_bytes)

    decoded_data = {
        "device": device,
        "time": time,
        "state": state,
        "state_of_charge": state_of_charge,
        "temperature": temperature,
    }

    return decoded_data


def main(event, context):  # pylint: disable=unused-argument
    try:
        logger.info("Starting battery health monitoring")

        payload_hex = event["payload"]
        logger.info("Received payload: %s", payload_hex)

        decoded_data = decode_payload(payload_hex, event["device"])
        logger.info("Decoded data: %s", decoded_data)

        print(decoded_data)

    except Exception as e:
        logger.error(e, exc_info=True)
        raise Exception(  # pylint: disable=broad-exception-raised
            "Error occurred while processing event"
        ) from e

    return {
        "statusCode": HTTPStatus.OK.value,
        "body": json.dumps("Successfully processed event"),
    }
