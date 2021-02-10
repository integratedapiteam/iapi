from flask import blueprints, request, jsonify
from util.logger import logger
import requests
import FilterHTML
from bs4 import BeautifulSoup

cu = blueprints.Blueprint("cu", __name__, url_prefix="/cu")


@cu.route("/<string:tracking_number>", methods=["GET"])
def get_tracking_status(tracking_number):
    """CU POST의 배송조회 API입니다.
    GS POST BOX는 운송장의 자리수가 10자리입니다. 참조부탁드립니다.
    ---
    tags:
      - delivery_tracker
    parameters:
        - name: tracking_number
          in: query
          type: string
          enum: ["1111111111111"]
          required: true
          default: null
    responses:
      200:
        description: 택배 배송조회 및 현황 조회가 성공했음을 의미합니다.
      400:
        description: 송장번호의 자릿수가 안 맞을 때 리턴합니다.
      500:
        description: 서버 오류가 발생했을 때 리턴합니다.
    """
    verify = True
    response = 200
    message = None

    try:
        print(tracking_number)
    except Exception as e:
        logger.error(e)
        verify = False
        response = 500
        message = "농협택배 배송조회 중 서버오류가 발생했습니다."
    finally:
        if verify is True:
            pass
        else:
            result = {"message": message}
        return jsonify(result), response
