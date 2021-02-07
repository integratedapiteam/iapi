import uuid
import random
from flask import blueprints, jsonify
from util.logger import logger

auth = blueprints.Blueprint("auth", __name__, url_prefix="/auth")


@auth.route("/", methods=['POST'])
def register():
    """
    @name: register
    @description: Private key를 발급해주는 api입니다.
    :return:
    """
    try:
        key = uuid.UUID(int=random.getrandbits(128))
        key = str(key)
        key = key.replace("-", "")
        result = {"secert_key": key}
        return jsonify(result), 200
    except Exception as e:
        logger.error(str(e))
        result = {"message": str(e)}
        return jsonify(result), 500