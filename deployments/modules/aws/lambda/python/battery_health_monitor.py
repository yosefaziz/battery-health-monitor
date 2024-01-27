import logging
from http import HTTPStatus

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def main(event, context):
    try:
        logger.info("Starting battery health monitor")
        print(f"Event: {event}, Context: {context}")
    except Exception as e:
        logger.error(e, exc_info=True)
        raise Exception("Error occurred while processing event")

    return {
        "statusCode": HTTPStatus.OK.value
        }
