from . import models


SUPPORTED_FILTERS = {'http_connection_manager', 'tcp_proxy', 'mongo_proxy'}


FILTER_MAP = {
    'http_connection_manager': models.HTTPConnectionManagerFilter,
    'tcp_proxy': models.TCPProxyFilter,
    'mongo_proxy': models.MongodbProxyFilter,
}
