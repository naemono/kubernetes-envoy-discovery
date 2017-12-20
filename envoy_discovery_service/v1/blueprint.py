from flask import Blueprint
from envoy_discovery_service.baseapi import API
from envoy_discovery_service.v1.listeners.resource import ListenerDiscoveryService
from envoy_discovery_service.v1.clusters.resource import ClusterDiscoveryService
from envoy_discovery_service.v1.services.resource import ServiceDiscoveryService


v1_blueprint = Blueprint('v1', __name__, url_prefix='/v1')
api = API(app=v1_blueprint)

api.add_resource(ListenerDiscoveryService,
                 '/listeners/<string:service_cluster>/<string:service_node>')
api.add_resource(ClusterDiscoveryService,
                 '/clusters/<string:service_cluster>/<string:service_node>')
api.add_resource(ServiceDiscoveryService, '/registration/<string:service_name>')
