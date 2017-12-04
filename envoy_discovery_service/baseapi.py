import logging

from flask_restful import Api


log = logging.getLogger(__name__)


class API(Api):
    """RESTful API subclass."""
