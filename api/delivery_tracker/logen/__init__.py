from flask import blueprints, request, jsonify
from util.logger import logger
import requests
from bs4 import BeautifulSoup
import datetime

logen = blueprints.Blueprint("logen", __name__, url_prefix="/logen")


@logen.route("/<string:tracking_number>/", methods=["GET"])
def get_delivery_tracker(tracking_number):
    """로젠택배의 택배 배송 현황 및 내역을 추적하는 API입니다.
    로젠택배의 운송장 자리수는 11자리이며, 상세한 배송 설명을 제공합니다. 배송현황 설명은 history 배열의 description field를 참조하시면 됩니다.
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
    try:
        verify = True
        message = None
        response = 200

        if len(tracking_number) != 11:
            verify = False
            message = "운송장 번호가 잘못되었습니다. 로젠택배의 운송장 번호는 11자리입니다."
            response = 400

        if verify is True:
            tracking_html = requests.get("https://www.ilogen.com/web/personal/trace/{0}".format(tracking_number))
            soup = BeautifulSoup(tracking_html.text, "html.parser")

            status_text = str(soup.findAll("td")[-11])

            history_list = []

            for idx, td in enumerate(soup.findAll("td")[18:-12]):
                if idx % 8 == 0:
                    date = str(soup.findAll("td")[18:-12][idx])
                    location = str(soup.findAll("td")[18:-12][idx + 1])
                    delivery_status = str(soup.findAll("td")[18:-12][idx + 2])
                    delivery_status_description = str(soup.findAll("td")[18:-12][idx + 3])

                    date = date.replace("<td>", "")
                    date = date.replace("</td>", "")
                    date = date.strip()

                    location = location.replace("<td>", "")
                    location = location.replace("</td>", "")
                    location = location.strip()

                    delivery_status = delivery_status.replace("<td>", "")
                    delivery_status = delivery_status.replace("</td>", "")
                    delivery_status = delivery_status.strip()

                    delivery_status_description = delivery_status_description.replace("<td>", "")
                    delivery_status_description = delivery_status_description.replace("</td>", "")
                    delivery_status_description = delivery_status_description.strip()

                    history = {
                        "datetime": date,
                        "date": date[0:10],
                        "location": location,
                        "status": delivery_status,
                        "description": delivery_status_description
                    }

                    history_list.append(history)

            if "배송완료" in status_text:
                status = "배달완료"
            elif "배송출고" in status_text:
                status = "발송중"
            elif "배송입고" in status_text:
                status = "집화처리"
            else:
                status = "Unknown status"
    except Exception as e:
        logger.error(str(e), exc_info=True)
        verify = False
        message = "로젠택배 배송조회에서 오류가 발생하였습니다."
        response = 500
    finally:
        if verify is True:
            result = {"status": status, "tracking_number": tracking_number, "history": history_list}
        else:
            result = {"message": message}
        return jsonify(result), response
