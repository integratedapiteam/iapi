import requests
import bs4
import FilterHTML

from app import db
from models.CrawlingLastPage import CrawlingLastPage
from util.sms_send import send_sms_message

result_html = requests.get("https://www.phpschool.com/gnuboard4/bbs/board.php?bo_table=old_job&page=1")
soup = bs4.BeautifulSoup(result_html.text, "html.parser")

db.session.create(CrawlingLastPage(FilterHTML.filter_html(soup.select("td[class*='subject']")[3].find("span"), {}),
                                   "php_school"))

message = "PHP SCHOOL에서 새 외주가 있습니다. 제목: " + FilterHTML.filter_html(soup.select("td[class*='subject']")[3]
                                                                   .find("span"), {})

send_sms_message(message, "01057949511,01056046071")



