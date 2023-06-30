from flask import Flask

from quran_chatgpt.views.backend import backend
from quran_chatgpt.views.twilio import twilio
from quran_chatgpt.views.home import home

app = Flask(__name__)

app.register_blueprint(home)
app.register_blueprint(backend)
app.register_blueprint(twilio)
