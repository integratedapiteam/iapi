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
from api.auth import auth

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
    "termsOfService": "https://www.hksoft.co.kr/terms",
    "version": "0.0.3"
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
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
swagger = Swagger(app, template=template)
CORS(app)
db = SQLAlchemy(app)

# ===== Registering Blueprints =====
app.register_blueprint(cj)
app.register_blueprint(epost)
app.register_blueprint(logen)
app.register_blueprint(lotte)

app.register_blueprint(auth)
