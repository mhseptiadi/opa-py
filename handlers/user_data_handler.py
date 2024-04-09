import json
import os

import bcrypt
from dotenv import load_dotenv

from exceptions.auth_exception import AuthException
from exceptions.user_exception import UserException
from handlers.jwt_handler import jwt_encode

load_dotenv()
hash_round = os.environ.get("HASH_ROUND", 13)

# todo: use db
userJson = open('users.json')
usersData = json.load(userJson)


def get_all_users():
    return usersData


def create_user(data):
    password = bcrypt.hashpw(str.encode(data['password']), bcrypt.gensalt(int(hash_round)))

    try:
        user = {
            "email": data['email'],
            "name": data['name'],
            "password": password.decode(),
            "roles": data['roles']
        }

        usersData.append(user)

    except Exception as e:
        raise UserException("Invalid user data", 400)


def login(data):
    try:
        for user in usersData:
            if user['email'] == data['email']:
                if bcrypt.checkpw(str.encode(data['password']), str.encode(user['password'])):
                    return {
                        "token": "Bearer " + jwt_encode(user)
                    }
                else:
                    raise AuthException("Email or Password invalid", 403)
    except Exception as e:
        raise AuthException("Email or Password invalid", 403)

    raise AuthException("Email or Password invalid", 403)
