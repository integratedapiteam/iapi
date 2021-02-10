import uuid
import random
import datetime

from flask import blueprints, jsonify, request
from models.User import User
from util.logger import logger
from app import db

auth = blueprints.Blueprint("auth", __name__, url_prefix="/auth")


@auth.route("/", methods=['POST'])
def issue_secret_key():
    """
    @name: issue_secret_key
    @description: Private key 를 발급해주는 api 입니다.
    :return:
    """
    try:
        key = uuid.UUID(int=random.getrandbits(128))
        key = str(key)
        key = key.replace("-", "")
        result = {"secret_key": key}
        return jsonify(result), 200
    except Exception as e:
        logger.error(str(e))
        result = {"message": str(e)}
        return jsonify(result), 500


@auth.route("/register", methods=['POST'])
def register():
    verify = True
    response = 200
    message = None
    try:
        request_json = request.get_json(silent=True)
        email = request_json["email"]
        name = request_json["name"]
        social_token = request_json["social_token"]
        social = request_json["social"]

        secret_key = uuid.UUID(int=random.getrandbits(128))
        secret_key = str(secret_key)
        secret_key = secret_key.replace("-", "")

        user = User(secret_key, email, name, social_token, social, datetime.datetime.now())
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        logger.error(e)
        verify = False
        response = 500
        message = "회원가입 시도 중에 서버 에러가 발생했습니다."
    finally:
        if verify is True:
            result = {"status": "success"}
        else:
            result = {"status": "failure", "message": message}
        return jsonify(result), response
