from flask import jsonify
from flask_restful import Resource
from envoy_discovery_service.v1.services import schema as services_schema
from envoy_discovery_service.v1 import kubernetes_utils


class ServiceDiscoveryService(Resource):
    def get(self, service_name, namespace='default'):
        service = kubernetes_utils.get_k8s_service(namespace, service_name)
        endpoints = kubernetes_utils.get_service_endpoints(service)
        hosts = kubernetes_utils.get_hosts_from_endpoints(endpoints)
        config = dict(
            hosts=hosts)
        schema = services_schema.ServiceSchema()
        result = schema.dump(config)
        return jsonify(result.data)
