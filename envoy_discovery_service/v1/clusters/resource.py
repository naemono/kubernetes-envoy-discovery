from flask import jsonify
from flask.ext.restful import Resource
from envoy_discovery_service.v1.clusters import schema as clusters_schema
from envoy_discovery_service.v1 import kubernetes_utils
from envoy_discovery_service import app


class ClusterDiscoveryService(Resource):
    def get(self):
        clusters = kubernetes_utils.get_clusters_from_services(
            kubernetes_utils.get_k8s_services(),
            internal_k8s_envoy=app.config['internal_k8s_envoy'])
        config = dict(
            clusters=clusters)
        schema = clusters_schema.ClusterManagerSchema()
        result = schema.dump(config)
        return jsonify(result.data)
