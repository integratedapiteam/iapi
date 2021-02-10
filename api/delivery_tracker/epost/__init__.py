from flask import blueprints, request, jsonify
from util.logger import logger
import requests
import FilterHTML
from bs4 import BeautifulSoup

epost = blueprints.Blueprint("epost", __name__, url_prefix="/epost")


@epost.route("/<string:tracking_number>", methods=['GET'])
def get_delivery_tracker(tracking_number):
    """우체국택배의 택배 배송 현황 및 내역을 추적하는 API입니다.
    우체국 택배의 경우, 운송장의 자리수는 13자리입니다. 테스트 운송장 번호가 있어, 해당 운송장 번호를 default로 사용하시어 개발에 참조하시면 됩니다.
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
