import requests
import bs4
import FilterHTML

from flask import blueprints, jsonify
from util.logger import logger
from app import db
from models.CrawlingLastPage import CrawlingLastPage
from util.sms_send import send_sms_message

php_school = blueprints.Blueprint("php_school", __name__, url_prefix="/php_school")


@php_school.route("/", methods=["GET"])
def get_outsourcing_info():
    try:
        result_html = requests.get("https://www.phpschool.com/gnuboard4/bbs/board.php?bo_table=old_job&page=1")
        soup = bs4.BeautifulSoup(result_html.text, "html.parser")

        db.session.add(CrawlingLastPage(FilterHTML.filter_html(soup.select("td[class*='subject']")[3].find("span"), {}),
                                           "php_school"))

        message = "PHP SCHOOL에서 새 외주가 있습니다. 제목: " + FilterHTML.filter_html(soup.select("td[class*='subject']")[3]
                                                                           .find("span"), {})

        send_sms_message(message, "01057949511,01056046071")
        result = {"message": "success", "return": message}
        return jsonify(result), 200
    except Exception as e:
        logger.error(e)
        result = {"message": "failure"}
        return jsonify(result), 500



