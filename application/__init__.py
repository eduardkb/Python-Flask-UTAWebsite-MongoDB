from flask import Flask

# 2 imports below are for MongoDB setup
from config import Config
from flask_mongoengine import MongoEngine

# import for easy restAPI programming
from flask_restx import Api

api = Api()

app = Flask(__name__)

#for it to work in AWS:
application = app

app.config.from_object(Config)

# configure external mongoDB
# app.config["MONGODB_HOST"] = 'alex.mongohq.com/app12345678'
# app.config["MONGODB_PORT"] = 10043
# app.config["MONGODB_DATABASE"] = 'dbname'
# app.config["MONGODB_USERNAME"] = 'user'
# app.config["MONGODB_PASSWORD"] = 'password'
# db = MongoEngine(app)


db = MongoEngine()
db.init_app(app)

# initialize api variable
# api.init_app(app)


from application import routes