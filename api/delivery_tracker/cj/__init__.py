from flask import blueprints, request, jsonify
from util.logger import logger
import requests
import FilterHTML
from bs4 import BeautifulSoup

cj = blueprints.Blueprint("cj", __name__, url_prefix="/cj")


@cj.route("/", methods=['GET'])
def get_delivery_tracker():
    try:
        verify = True
        message = None
        response = 200

        tracking_number = request.args.get("tracking_number")

        if len(tracking_number) != 10:
            verify = False
            message = "운송장 길이가 맞지 않습니다. CJ대한통운의 운송장은 10자리입니다."
            response = 400

        if verify is True:
            tracking_html = requests.get("http://nplus.doortodoor.co.kr/web/detail.jsp?slipno={0}".format(tracking_number))
            tracking_html = tracking_html.text
            soup = BeautifulSoup(tracking_html, "html.parser")

            history_list = []

            histories = soup.findAll("td")[34:]

            for idx, history in enumerate(histories):
                if idx % 6 == 0:
                    date = histories[idx]
                    time = histories[idx+1]
                    location = histories[idx+2]
                    delivery_status = histories[idx+5]

                    date = str(date)
                    date = FilterHTML.filter_html(date, {})
                    date = date.strip()

                    time = str(time)
                    time = FilterHTML.filter_html(time, {})
                    time = time.strip()

                    location = str(location)
                    location = FilterHTML.filter_html(location, {})
                    location = location.strip()

                    delivery_status = str(delivery_status)
                    delivery_status = FilterHTML.filter_html(delivery_status, {})
                    delivery_status = delivery_status.strip()

                    delivery_history = {
                        "date": date.replace("-", "."),
                        "location": location.split(" ")[0].replace(" \n Tel", ""),
                        "daretime": date.replace("-", ".") + " " + time,
                        "status": delivery_status,
                        "description": delivery_status
                    }

                    history_list.append(delivery_history)

            history_list = list(reversed(history_list))

            if "배달완료" in soup.td.text:
                status = "배달완료"
            elif "집화처리" in soup.td.text:
                status = "집화처리"
            elif "(미등록운송장)" in soup.td.text:
                status = "미등록 운송장"
            elif soup.text is None:
                status = "택배사 오류"
            else:  # 해당 부분은 상태값 조사 이후에 다시 추가하는 걸로 하겠습니다. (2021.02.05 김대영 추가)
                status = "Unknown status"

    except Exception as e:
        logger.error(e, exc_info=True)
        verify = False
        message = "CJ대한통운 배송조회에서 서버 오류가 발생하였습니다."
        response = 500
    finally:
        if verify is True:
            result = {"tracking_number": tracking_number, "status": status, "history": history_list}
        else:
            result = {"message": message}

        return jsonify(result), response
