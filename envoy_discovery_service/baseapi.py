import logging

from flask.ext.restful import Api


log = logging.getLogger(__name__)


class API(Api):
    """RESTful API subclass."""
