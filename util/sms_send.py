import requests
from util.logger import logger
from config import ALIGO_KEY, ALIGO_IDENTIFIER


def send_sms_message(message, receiver):
    try:
        requests.post("https://apis.aligo.in/send", {
            "key": ALIGO_KEY,
            "user_id": ALIGO_IDENTIFIER,
            "message": message,
            "receiver": receiver
        })
    except Exception as e:
        logger.error(e, exc_info=True)