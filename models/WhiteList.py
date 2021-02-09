from app import db
from sqlalchemy import ForeignKey
import datetime


class WhiteList(db.Model):
    """
    idx: 해당 화이트리스트 IP의 인덱스
    ip_address: 아이피 주소
    user: 해당 IP를 갖고 있는 유저의 인덱스
    created_at: 생성 일자
    """

    __tablename__ = "white_list"
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    idx = db.Column(db.Integer, autoincrement=True, primary_key=True)
    ip_address = db.Column(db.String(50))
    user = db.Column(db.Integer, ForeignKey("user.idx"), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())

    def __init__(self, ip_address):
        self.ip_address = ip_address

    def as_dict(self):
        return {x.name: getattr(self, x.name) for x in self.__table__.columns}
