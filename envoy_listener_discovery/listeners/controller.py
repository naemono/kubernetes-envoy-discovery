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


def _get_service_endpoints(service):
    url = "http://localhost:8001/api/v1/namespaces/{}/endpoints/{}".format(service['metadata']['namespace'],
                                                                           service['metadata']['name'])
    response = requests.get(url, timeout=10)

    if response and response.status_code != 200:
        return None

    return response.json()


def _get_live_services(services):
    live_services = list()
    for service in services:
        if service.get('metadata', {}).get('labels'):
            endpoints = _get_service_endpoints(service)
            if endpoints:
                live_services.append(dict(
                    service=dict(
                        name=service['metadata']['name'],
                        ports=list(set([port['port'] for subset in endpoints['subsets']
                                        for port in subset['ports']]))
                    ),
                    pods=list(set([address['ip']
                                   for subset in endpoints['subsets']
                                   for address in subset['addresses']]))
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
    config = dict(
        listeners=listeners)
    schema = envoy_schema.ListenerConfigurationSchema()
    result = schema.dump(config)
    return jsonify(result.data)
