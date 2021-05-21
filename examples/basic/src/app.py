import json
import os

from dotenv import load_dotenv
from flask import Flask

from src.events import *
from src.services.rabbit import rabbit

load_dotenv()


def create_app():
    app = Flask(__name__)

    app.config['MQ_URL'] = os.getenv('MQ_URL')
    app.config['MQ_EXCHANGE'] = os.getenv('MQ_EXCHANGE')
    app.config['FLASK_ENV'] = os.getenv('FLASK_ENV')

    rabbit.init_app(
        app,
        'basic',
        json.loads,
        json.dumps,
        app.config.get('FLASK_ENV') == 'production'
    )

    @app.route('/ping', methods=['GET'])
    def _():
        rabbit.send(body='ping', routing_key='ping.message')
        return 'pong'

    @app.route('/ping-error', methods=['GET'])
    def __():
        rabbit.send(body='ping', routing_key='ping.error')
        return 'pong'

    return app
