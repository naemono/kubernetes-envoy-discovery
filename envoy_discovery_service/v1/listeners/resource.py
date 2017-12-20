from flask import jsonify
from flask_restful import Resource
from envoy_discovery_service.v1.listeners import schema as listeners_schema
from envoy_discovery_service.v1 import kubernetes_utils


class ListenerDiscoveryService(Resource):
    def get(self, service_cluster, service_node):
        services = kubernetes_utils.get_k8s_services()
        listeners = kubernetes_utils.get_listeners_from_services(services)
        config = dict(
            listeners=listeners)
        schema = listeners_schema.ListenerConfigurationSchema()
        result = schema.dump(config)
        return jsonify(result.data)
