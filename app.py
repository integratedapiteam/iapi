from flask import Flask
from flasgger import Swagger
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import SQLALCHEMY_DATABASE_URI

# ===== BluePrints =====
from api.delivery_tracker.cj import cj
from api.delivery_tracker.epost import epost
from api.delivery_tracker.logen import logen
from api.delivery_tracker.lotte import lotte

# ==== Swagger Template =====
template = {
  "swagger": "2.0",
  "info": {
    "title": "Integrated API (통합 API)",
    "description": "에이치케이소프트에서 개발하고 있는 익스트림보드에 사용될 통합 API의 대한 api spec을 명시해둔 문서입니다.",
    "contact": {
      "responsibleOrganization": "HKSOFT",
      "responsibleDeveloper": "Daeyoung Kim",
      "email": "integratedapiteam@gmail.com",
      "url": "www.hksoft.co.kr",
    },
    "termsOfService": "https://www.hk-soft.co.kr/terms",
    "version": "0.0.4"
  },
  "host": "localhost:5000",
  "basePath": "/",
  "schemes": [
    "http",
    "https"
  ],
  "operationId": "getmyData"
}

# ===== App Initializing =====
app = Flask(__name__)
app.config["DATABASE_URL"] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
swagger = Swagger(app, template=template)
CORS(app)
db = SQLAlchemy(app)

# ===== Models =====
# 여기는 파이썬 문법 무시해야 함... db migrate할 때 가져오기 때문임.
from models.User import User
from models.WhiteList import WhiteList
from models.CrawlingLastPage import CrawlingLastPage
from api.auth import auth
from api.outsorcing_crawling.outsourcing import outsourcing

# ===== Registering Blueprints =====
app.register_blueprint(cj)
app.register_blueprint(epost)
app.register_blueprint(logen)
app.register_blueprint(lotte)
app.register_blueprint(php_school)

app.register_blueprint(auth)
