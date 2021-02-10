import requests
import bs4
import FilterHTML

from app import db
from models.CrawlingLastPage import CrawlingLastPage

result_html = requests.get("https://www.phpschool.com/gnuboard4/bbs/board.php?bo_table=old_job&page=1")
soup = bs4.BeautifulSoup(result_html.text, "html.parser")

db.session.create(CrawlingLastPage(FilterHTML.filter_html(soup.select("td[class*='subject']")[3].find("span"), {}),
                                   "php_school"))



