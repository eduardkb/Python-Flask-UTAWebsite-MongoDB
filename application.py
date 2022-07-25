from email.mime import application
from flask import Flask
application = Flask(__name__)

@application.route('/')
def hello_world():
    return 'Sup, Ed. Subscribe.'