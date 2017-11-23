import requests

from flask import Blueprint, jsonify
from envoy_listener_discovery.listeners import models
from envoy_listener_discovery.listeners import schema as envoy_schema


listeners = Blueprint('v1', __name__)


def _get_pods_by_selector(selectors):
    url = 'http://localhost:8001/api/v1/namespaces/default/pods'
    response = requests.get(url, timeout=10, params=selectors)

    if response and response.status_code != 200:
        return None

    return response.json().get('items')


def _get_k8s_services():
    url = 'http://localhost:8001/api/v1/services'
    response = requests.get(url, timeout=10)

    if response and response.status_code != 200:
        return None

    return response.json().get('items')


def _get_ports_from_service(service):
    ports = list()
    for port in service['spec']['ports']:
        if port.get('nodePort'):
            ports.append(port['nodePort'])
        else:
            ports.append(port['targetPort'])
    return ports


def _get_live_services(services):
    live_services = list()
    for service in services:
        if service.get('metadata', {}).get('labels'):
            pods = _get_pods_by_selector(
                service.get('metadata', {}).get('labels'))
            if pods:
                live_services.append(dict(
                    service=dict(
                        name=service['metadata']['name'],
                        ports=_get_ports_from_service(service)
                    ),
                    pods=list(set([
                        item['status']['hostIP'] for item in pods]))
                ))
    return live_services


def _get_listeners_from_services(services):
    listeners = list()
    for service in services:
        for port in service['service']['ports']:
            listeners.append(dict(
                address="tcp://0.0.0.0:{}".format(port),
                filters=[dict(
                    name="{}_{}".format(service['service']['name'], port),
                    config=dict(
                        access_log=dict(path="/dev/stdout"),
                        codec_type="auto",
                        stat_prefix="ingress_http",
                        route_config=dict(
                            virtual_hosts=[dict(
                                name="backend",
                                domains=["*"],
                                routes=[dict(
                                    timeout_ms=0,
                                    prefix="/{}_{}".format(service['service']['name'], port),
                                    cluster="{}_{}".format(service['service']['name'], port)
                                )]
                            )]
                        ),
                        filters=dict(name="router", config={})
                    )
                )]
            ))
    return listeners


def _get_clusters_from_services(services):
    clusters = list()
    for service in services:
        for port in service['service']['ports']:
            clusters.append(dict(
                name="{}_{}".format(service['service']['name'], port),
                connect_timeout_ms=250,
                type="strict_dns",
                lb_type="round_robin",
                features="http2",
                hosts=[dict(url="tcp://{}:{}".format(service['service']['name'], port))]
            ))
    return clusters


@listeners.route('/listeners/')
def index():
    services = _get_k8s_services()
    valid_services = _get_live_services(services)
    listeners = _get_listeners_from_services(valid_services)
    clusters = _get_clusters_from_services(valid_services)
    config = dict(
        listeners=listeners,
        admin=dict(
            access_log_path="/dev/stsdout",
            address="tcp://0.0.0.0:8001"
        ),
        cluster_manager=dict(
            clusters=clusters
        )
    )
    schema = envoy_schema.ListenerConfigurationSchema()
    result = schema.dump(config)
    return jsonify(result.data)
