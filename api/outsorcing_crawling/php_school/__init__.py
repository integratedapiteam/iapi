import requests
import bs4
import FilterHTML

from config import SQLALCHEMY_DATABASE_URI
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models.CrawlingLastPage import CrawlingLastPage
from util.sms_send import send_sms_message

engine = sqlalchemy.create_engine(SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()

result_html = requests.get("https://www.phpschool.com/gnuboard4/bbs/board.php?bo_table=old_job&page=1")
soup = bs4.BeautifulSoup(result_html.text, "html.parser")

session.add(CrawlingLastPage(FilterHTML.filter_html(soup.select("td[class*='subject']")[3].find("span"), {}),
                                   "php_school"))

message = "PHP SCHOOL에서 새 외주가 있습니다. 제목: " + FilterHTML.filter_html(soup.select("td[class*='subject']")[3]
                                                                   .find("span"), {})

send_sms_message(message, "01057949511,01056046071")



