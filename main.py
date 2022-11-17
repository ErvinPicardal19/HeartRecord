import os
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from py_dotenv import read_dotenv
from heart import HeartRate, HeartRateSingle, Login

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
read_dotenv(dotenv_path)

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("ACCESS_TOKEN_SECRET")
jwt = JWTManager(app)
api = Api(app)

api.add_resource(HeartRate, "/heart")

api.add_resource(HeartRateSingle, "/heart/<id>")

api.add_resource(Login, "/auth")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)