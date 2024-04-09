import os

from dotenv import load_dotenv
from flask import Flask, request

from exceptions.auth_exception import AuthException
from exceptions.user_exception import UserException
from handlers.opa_handler import opa_decorator
from handlers.user_data_handler import get_all_users, create_user, login

load_dotenv()
app_port = os.environ.get("APP_PORT", 8000)
is_prod = os.environ.get("PROD", False)

app = Flask(__name__)


@app.errorhandler(AuthException)
def handle_auth_exception(e):
    return e.message, e.code


@app.errorhandler(UserException)
def handle_auth_exception(e):
    return e.message, e.code


# routes
@app.route("/")
def root():
    return "opa-py is running!"


@app.route('/api/users', methods=['GET'])
@opa_decorator('read', 'user')
def get_users():
    return get_all_users()


@app.route('/api/users', methods=['POST'])
@opa_decorator('create', 'user')
def post_users():
    create_user(request.json)
    return get_all_users()


@app.route('/api/login', methods=['POST'])
def route_login():
    return login(request.json)


if __name__ == '__main__':
    print(is_prod, app_port)
    if is_prod == 'True' or is_prod == 'true':
        from waitress import serve
        serve(app, host="0.0.0.0", port=app_port)
    else:
        app.run(debug=True, host='0.0.0.0', port=app_port)


