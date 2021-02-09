from app import db
import datetime


class User(db.Model):
    """
    idx: 유저의 인덱스
    secret_key: 해당 유저에게 발급한 secret_key
    email: 해당 유저의 이메일
    name: 해당 유저의 이름
    social_token: 해당 유저의 소셜 토큰
    created_at: 유저 생성일
    updated_at: 유저 수정일
    """
    __tablename__ = "user"
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    idx = db.Column(db.Integer, autoincrement=True, primary_key=True)
    secret_key = db.Column(db.String(120), unique=True)
    email = db.Column(db.String(120), unique=True)
    name = db.Column(db.String(120))
    social_token = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now())

    def __init__(self, secret_key, email, name, social_token, updated_at):
        self.idx = None
        self.secret_key = secret_key
        self.email = email
        self.name = name
        self.social_token = social_token
        self.created_at = datetime.datetime.now()
        self.updated_at = updated_at

    def as_dict(self):
        return {x.name: getattr(self, x.name) for x in self.__table__.columns}
