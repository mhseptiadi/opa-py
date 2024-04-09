import json
import os
from functools import wraps

import jwt
import requests
from dotenv import load_dotenv
from flask import Flask, request

from exceptions.auth_exception import AuthException
from handlers.jwt_handler import jwt_decode

load_dotenv()
opa_host = os.environ.get("OPA_HOST", "http://opa:8181")
opa_jwt_key = os.environ.get("OPA_JWT_KEY", "opaSecretKey")
app_name = os.environ.get("APP_NAME", "opa-py")

app = Flask(__name__)


def check_opa(roles, action, target):
    try:
        token = jwt.encode({
            "app": app_name
        }, opa_jwt_key, algorithm="HS256")

        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": "Bearer " + token
        }

        opa_input = json.dumps({
            "input": {
                "roles": roles,
                "action": action,
                "object": target
            }
        })

        response = requests.post(opa_host + "/v1/data/permission", headers=headers, data=opa_input)

    except Exception as e:
        app.logger.debug("Unexpected error requesting OPA server: %s", repr(e))
        raise AuthException("Unexpected error requesting OPA server", 500)

    if response.status_code != 200:
        raise AuthException(
            "OPA server response code: " + str(response.status_code) + ". message:" + str(response.json()),
            response.status_code
        )

    allowed = response.json()
    if allowed['result']['allow']:
        app.logger.debug("action allowed")
    else:
        raise AuthException("Not allowed", 403)


def get_token(header):
    if not header.startswith('Bearer '):
        raise AuthException('Invalid token', 403)

    return header[len('Bearer '):]


def opa_decorator(action, target):
    def _opa_decorator(f):
        @wraps(f)
        def __opa_decorator(*args, **kwargs):
            token = get_token(request.headers.get("Authorization", ""))
            data = jwt_decode(token)
            try:
                roles = data['roles']
                check_opa(roles, action, target)
            except Exception as e:
                raise e
            return f(*args, **kwargs)
        return __opa_decorator
    return _opa_decorator
