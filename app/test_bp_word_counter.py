from flask import Flask
from bp_word_counter import bp_app

def test_bp_app():
    app = Flask(__name__)
    app.register_blueprint(bp_app, url_prefix="/api/v1")

    client = app.test_client()