from flask import blueprints, request, jsonify
from util.logger import logger
import requests
import FilterHTML
from bs4 import BeautifulSoup

lotte = blueprints.Blueprint("lotte", __name__, url_prefix="/lotte")


@lotte.route("/", methods=['GET'])
def get_tracking_status():
    try:
        verify = True
        response = 200
        message = None
        pass
    except Exception as e:
        logger.error(e, exc_info=True)
    finally:
        if verify is True:
            result = {""}
        else:
            result = {"message": message}
        return jsonify(result), response