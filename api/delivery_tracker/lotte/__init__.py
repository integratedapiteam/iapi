from flask import blueprints, request, jsonify
from util.logger import logger
import requests
import FilterHTML
from bs4 import BeautifulSoup

lotte = blueprints.Blueprint("lotte", __name__, url_prefix="/lotte")


@lotte.route("/", methods=['GET'])
def get_tracking_status():
    """롯데택배의 택배 배송 현황 및 내역을 추적하는 API입니다.
    아래부터는 paramter들을 다룹니다.
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
        response = 200
        message = None

        tracking_number = request.args.get("tracking_number")

        if len(tracking_number) != 10 and len(tracking_number) != 12:
            verify = False
            response = 400
            message = "잘못된 운송장 번호입니다. 롯데택배의 경우 10자리 혹은 12자리의 운송장번호입니다."

        if verify is True:
            tracking_html = requests.get("https://www.lotteglogis.com/home/reservation/tracking/linkView?InvNo={0}"
                                         .format(tracking_number))
            soup = BeautifulSoup(tracking_html.text, "html.parser")

            histories = soup.findAll("td")[4:]

            history_list = []

            print(len(histories))

            for idx, td in enumerate(histories):
                if idx % 4 == 0:
                    delivery_status = FilterHTML.filter_html(str(histories[idx]), {})
                    delivery_status = delivery_status.strip()

                    datetime = FilterHTML.filter_html(str(histories[idx+1]), {})
                    datetime = datetime.strip()

                    location = FilterHTML.filter_html(str(histories[idx+2]), {})
                    location = location.strip()

                    delivery_status_description = FilterHTML.filter_html(str(histories[idx+3]), {})
                    delivery_status_description = delivery_status_description.strip()

                    history = {
                        "datetime": datetime.replace("-", "."),
                        "date": datetime[0:10].replace("-", "."),
                        "location": location,
                        "status": delivery_status,
                        "description": delivery_status_description
                    }

                    history_list.append(history)

            history_list = list(reversed(history_list))

            status = str(soup.findAll("td")[4])

            if "배달완료" in status:
                status = "배달완료"
            elif "상품접수" in status:
                status = "집화처리"
            elif "상품 이동중" in status:
                status = "배송중"
            else:
                status = "Unknown Status"

    except Exception as e:
        logger.error(e, exc_info=True)
        verify = False
        response = 500
        message = "롯데택배 배송조회에서 서버 에러가 발생하였습니다."
    finally:
        if verify is True:
            result = {"status": status, "history": history_list, "tracking_number": tracking_number}
        else:
            result = {"message": message}

        return jsonify(result), response
