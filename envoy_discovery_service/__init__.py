import os
from distutils.util import strtobool

from flask import Flask
from flask_marshmallow import Marshmallow

from .logger import setup_logging

setup_logging()


app = Flask(__name__)
# Allow trailing, or no trailing slashes
app.url_map.strict_slashes = False
# Is Envoy running as an internal k8s service?
app.config['internal_k8s_envoy'] = strtobool(os.environ.get('INTERNAL_K8S_ENVOY', 'False'))
app.config['service_ip_override'] = os.environ.get('SERVICE_IP_OVERRIDE')
app.config['DEBUG'] = strtobool(os.environ.get('FLASK_DEBUG', 'True'))
ma = Marshmallow(app)

from envoy_discovery_service.v1.blueprint import v1_blueprint  # noqa

app.register_blueprint(v1_blueprint, url_prefix='/v1')
