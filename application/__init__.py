from flask import Flask

# 2 imports below are for MongoDB setup
from config import Config
from flask_mongoengine import MongoEngine

# import for easy restAPI programming
from flask_restx import Api

api = Api()

app = Flask(__name__)
app.config.from_object(Config)

db = MongoEngine()
db.init_app(app)

# initialize api variable
api.init_app(app)


from application import routes