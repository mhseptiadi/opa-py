import datetime
import os

import jwt
from dotenv import load_dotenv
from flask import Flask

from exceptions.auth_exception import AuthException

load_dotenv()
jwt_key = os.environ.get("JWT_KEY", "mySecretKey")

app = Flask(__name__)


def jwt_decode(token):
    try:
        data = jwt.decode(token, jwt_key, algorithms=["HS256"])
        app.logger.debug(data)
        return data
    except Exception as e:
        raise AuthException("JWT Error: " + repr(e), 403)


def jwt_encode(data):
    try:
        data['iat'] = datetime.datetime.now(tz=datetime.timezone.utc)
        data['exp'] = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=1)
        return jwt.encode(data, jwt_key, algorithm="HS256")
    except Exception as e:
        raise AuthException("JWT Error: " + repr(e), 403)
