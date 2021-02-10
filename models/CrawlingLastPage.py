from app import db
import datetime


class CrawlingLastPage(db.Model):
    """
    CrawlingLastPage
    =====
    idx: 크롤링 페이지의 인덱스
    last_page_title: 가장 최신의 타이틀
    page_category: 어떤 외주 사이트인지
    created_at: 생성일자
    """
    __tablename__ = "crawling_last_page"
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    idx = db.Column(db.Integer, primary_key=True, autoincrement=True)
    last_content_title = db.Column(db.String(255))
    page_category = db.Column(db.String(255))
    created_at = db.Column(db.DateTime)

    def __init__(self, last_content_title, page_category):
        self.last_content_title = last_content_title
        self.page_category = page_category
        self.created_at = datetime.datetime.now()