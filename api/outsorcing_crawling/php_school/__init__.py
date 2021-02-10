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
        message = "새 외주가 없습니다."

        last_page = db.session.query(CrawlingLastPage).filter(CrawlingLastPage.page_category == "php_school")
        last_url = soup.select("td[class*='subject']")[3].find("a")
        last_url = str(last_url)[9:70].replace("..", "www.phpschool.com/gnuboard4")
        last_url = last_url.replace("amp;", "")
        last_url = last_url.replace("page=1", "")

        logger.info(last_page.all())

        if len(last_page.all()) == 0:
            last_page = None
        else:
            last_page = last_page.all()

        if last_page is None:
            db.session.add(
                CrawlingLastPage(FilterHTML.filter_html(soup.select("td[class*='subject']")[3].find("span"), {}),
                                 "php_school"))
            db.session.commit()

            message = "[PHP_SCHOOL] " + last_url

            send_sms_message(message, "01056046071")
        else:
            if last_page[0].last_content_title != FilterHTML.filter_html(soup.select("td[class*='subject']")[3]
                                                                               .find("span"), {}):
                db.session.delete(CrawlingLastPage(FilterHTML.filter_html(soup.select("td[class*='subject']")[3].find("span"), {}),
                                 "php_school"))
                db.session.commit()

        result = {"message": "success", "return": message}
        return jsonify(result), 200
    except Exception as e:
        logger.error(e, exc_info=True)
        result = {"message": "failure"}
        return jsonify(result), 500



