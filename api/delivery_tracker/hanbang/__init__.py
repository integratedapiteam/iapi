from flask import blueprints, request, jsonify
from util.logger import logger
import requests
import FilterHTML
from bs4 import BeautifulSoup

hanbang = blueprints.Blueprint("hanbang", __name__, url_prefix="/hanbang")


@hanbang.route("/", methods=['GET'])
def get_tracking_status():
    try:
        verify = True
        response = 200
        message = None

        tracking_number = request.args.get("tracking_number")

        if len(tracking_number) != 12:
            verify = False
            response = 400
            message = "잘못된 운송장 번호입니다. 한방택배의 경우 12자리의 운송장번호입니다."

        if verify is True:
            pass

    except Exception as e:
        logger.error(e, exc_info=True)
        verify = False
        response = 500
        message = "한방택배 배송조회에서 서버 에러가 발생하였습니다."
    finally:
        if verify is True:
            result = {""}
        else:
            result = {"message": message}
        return jsonify(result), response