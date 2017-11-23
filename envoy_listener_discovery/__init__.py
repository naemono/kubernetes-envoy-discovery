from flask import Flask
from flask_marshmallow import Marshmallow

app = Flask(__name__)
ma = Marshmallow(app)

from envoy_listener_discovery.listeners.controller import listeners  # noqa

app.register_blueprint(listeners, url_prefix='/v1')
