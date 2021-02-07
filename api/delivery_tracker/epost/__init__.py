from flask import blueprints, request, jsonify
from util.logger import logger
import requests
import FilterHTML
from bs4 import BeautifulSoup

epost = blueprints.Blueprint("epost", __name__, url_prefix="/epost")


@epost.route("/", methods=['GET'])
def get_delivery_tracker():
    try:
        verify = True
        message = None
        response = 200

        tracking_number = request.args.get("tracking_number")

        if len(tracking_number) != 13:
            verify = False
            message = "운송장 번호가 맞지 않습니다. 우체국 택배의 운송장 번호는 13자리입니다."
            response = 400

        if verify is True:
            tracking_html = requests.get("https://service.epost.go.kr/trace.RetrieveDomRigiTraceList"
                                         ".comm?sid1={0}&displayHeader=N".format(tracking_number))
            soup = BeautifulSoup(tracking_html.text, "html.parser")

            status_text = str(soup.findAll("td")[-1])

            history_list = []
            histories = soup.findAll("td")[4:]

            for idx, td in enumerate(histories):
                if idx % 4 == 0:
                    date = str(histories[idx])
                    date = FilterHTML.filter_html(date, {})
                    date = date.strip()

                    time = str(histories[idx + 1])
                    time = FilterHTML.filter_html(time, {})
                    time = time.strip()

                    location = str(histories[idx + 2])
                    location = FilterHTML.filter_html(location, {})
                    location = location.strip()

                    delivery_status = str(histories[idx + 3])
                    delivery_status = FilterHTML.filter_html(delivery_status, {})
                    delivery_status = delivery_status.strip()
                    delivery_status = delivery_status.replace("\t", "")
                    delivery_status = delivery_status.replace("\xa0", "")
                    delivery_status = delivery_status.replace("\n", "")
                    delivery_status = delivery_status.strip()

                    history = {
                        "date": date,
                        "location": location,
                        "datetime": date + " " + time,
                        "status": delivery_status,
                        "description": delivery_status
                    }

                    print(history)

                    history_list.append(history)

            if "배달완료" in status_text:
                status = "배달완료"
            elif "발송" in status_text:
                status = "발송중"
            elif "도착" in status_text:
                status = "도착"
            elif "배달준비" in status_text:
                status = "집화처리"
            else:
                status = "Unknown status"
    except Exception as e:
        verify = False
        message = "우체국 택배 배송조회에서 서버오류가 발생하였습니다."
        response = 500
        logger.error(str(e))
    finally:
        if verify is True:
            result = {"status": status, "tracking_number": tracking_number, "history": history_list}
        else:
            result = {"message": message}
        return jsonify(result), response
