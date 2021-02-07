from flask import blueprints, request, jsonify
from util.logger import logger
import requests
from bs4 import BeautifulSoup
import datetime

logen = blueprints.Blueprint("logen", __name__, url_prefix="/logen")


@logen.route("/", methods=["GET"])
def get_delivery_tracker():
    try:
        verify = True
        message = None
        response = 200

        tracking_number = request.args.get("tracking_number")

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
