from distutils.util import strtobool

from lru import LRUCacheDict

import logging
import requests
import yaml

from . import filters
from . import models
from .. import app

d = LRUCacheDict(max_size=10, expiration=60)

LOGGER = logging.getLogger(__name__)


if app.config['internal_k8s_envoy']:
    host = 'https://kubernetes'
else:
    host = 'http://localhost:8001'


try:
    TOKEN = open("/var/run/secrets/kubernetes.io/serviceaccount/token", "r").read()
except FileNotFoundError:
    TOKEN = None


def _create_filter(endpoints, service, service_filter):
    if isinstance(service_filter['type'](), models.TCPProxyFilter):
        # TODO Ensure that these configmaps that generate these filters are valid from marshallow models.
        # _ensure_model(service_filter)
        return dict(
            name="tcp_proxy",
            config=service_filter['filter']['config']
        )
    elif isinstance(service_filter['type'](), models.MongodbProxyFilter):
        # TODO Ensure that these configmaps that generate these filters are valid from marshallow models.
        # _ensure_model(service_filter)
        return dict(
            name="mongo_proxy",
            config=service_filter['filter']['config']
        )
    elif isinstance(service_filter['type'](), models.HTTPConnectionManagerFilter):
        # TODO Ensure that these configmaps that generate these filters are valid from marshallow models.
        # _ensure_model(service_filter)
        return dict(
            name="http_connection_manager",
            config=service_filter['filter']['config']
        )


def _endpoints_response_valid(endpoints):
    return not (endpoints['kind'] == 'Status' and endpoints['code'] == 404)


def _get_ip_for_node(node_name):
    url = "{}/api/v1/nodes/{}".format(host, node_name)
    response = requests.get(
        url, timeout=10, verify=False, headers={"Authorization": "Bearer " + TOKEN} if TOKEN else {})

    if response and response.status_code != 200:
        return None

    address = [address['address'] for address in response.json()['status']['addresses']
               if address['type'] == 'InternalIP']
    return address[0] if address else None


def _get_service_envoy_config(service):
    url = "{}/api/v1/namespaces/{}/configmaps/{}".format(host, service['metadata']['namespace'],
                                                         service['metadata']['name'])
    response = requests.get(url, timeout=10, verify=False, headers={
                            "Authorization": "Bearer " + TOKEN} if TOKEN else {})

    if response and response.status_code != 200:
        return None

    return response.json()


def _get_service_filters(service):
    service_envoy_config = _get_service_envoy_config(service)
    if not service_envoy_config:
        return []
    envoy_config = service_envoy_config.get('data', {}).get('envoy.config')
    if not envoy_config:
        return []
    try:
        envoy_yaml_config = yaml.load(envoy_config)
    except Exception as ex:
        return []
    envoy_filters = [envoy_filter for envoy_filter in envoy_yaml_config['filters']]
    service_filters = list()
    if not envoy_filters:
        return []
    for service_filter in envoy_filters:
        if service_filter['type'] not in filters.SUPPORTED_FILTERS:
            continue
        service_filters.append(dict(type=filters.FILTER_MAP[service_filter['type']],
                                    filter=service_filter))
    return service_filters


def _service_envoy_enabled(service):
    return strtobool(service['metadata'].get('labels', {}).get('envoyEnabled', 'false'))


def _get_pods_by_selector(selectors):
    url = "{}/api/v1/namespaces/default/pods".format(host)
    response = requests.get(url, timeout=10, params=selectors, verify=False,
                            headers={"Authorization": "Bearer " + TOKEN} if TOKEN else {})

    if response and response.status_code != 200:
        return None

    return response.json().get('items')


def _get_service_endpoints(service):
    url = "{}/api/v1/namespaces/{}/endpoints/{}".format(host, service['metadata']['namespace'],
                                                        service['metadata']['name'])
    response = requests.get(url, timeout=10, verify=False, headers={
        "Authorization": "Bearer " + TOKEN} if TOKEN else {})

    if response and response.status_code != 200:
        return None

    return response.json()


def get_listeners_from_services(services):
    listeners = list()
    try:
        if d['listeners']:
            LOGGER.info("Found listeners in cache")
            return d['listeners']
    except KeyError:
        LOGGER.info("listeners not found in cache")
        pass
    for service in services:
        endpoints = get_service_endpoints(service)
        if (not _service_envoy_enabled(service)
                or not _endpoints_response_valid(endpoints)):
            continue
        service_filters = _get_service_filters(service)
        if not service_filters:
            continue
        for port in service['spec'].get('ports', []):
            if not port.get('nodePort'):
                continue
            listeners.append(dict(
                address="tcp://0.0.0.0:{}".format(port['nodePort']),
                filters=[_create_filter(endpoints, service, service_filter)
                         for service_filter in service_filters],
                name="{}_{}".format(
                    service['metadata']['name'],
                    port['port'])
            ))
    LOGGER.info("Adding listeners to cache")
    d['listeners'] = listeners
    return listeners


def get_clusters_from_services(services, internal_k8s_envoy=False):
    clusters = list()
    circuit_breaker = dict(
        max_connections=1024000,
        max_pending_requests=1024000,
        max_requests=1024000,
        max_retries=3
    )
    circuit_breakers = dict(
        default=circuit_breaker,
        high=circuit_breaker
    )
    if not services:
        return clusters
    try:
        if d['clusters']:
            LOGGER.info("Found clusters in cache")
            return d['clusters']
    except KeyError:
        LOGGER.info("Clusters not found in cache")
        pass
    for service in services:
        endpoints = get_service_endpoints(service)
        for subset in endpoints.get('subsets', []):
            for address in subset.get('addresses', []):
                if not address.get('nodeName'):
                    continue
                ip = _get_ip_for_node(address['nodeName'])
                for port in service['spec']['ports']:
                    if internal_k8s_envoy:
                        hosts = [dict(url="tcp://{}:{}".format(service['metadata']['name'],
                                                               port['port']))]
                    else:
                        if service['spec']['clusterIP'] == 'None':
                            continue
                        hosts = [dict(url="tcp://{}:{}".format(
                            app.config['service_ip_override']
                            if app.config['service_ip_override']
                            else ip, port['nodePort'] if port.get('nodePort') else port['port']))]
                    clusters.append(dict(
                        name="{}_{}".format(service['metadata']['name'], port['port']),
                        connect_timeout_ms=250,
                        type="strict_dns" if internal_k8s_envoy else "static",
                        lb_type="round_robin",
                        circuit_breakers=circuit_breakers,
                        hosts=hosts
                    ))
    LOGGER.info("Adding clusters to cache")
    d['clusters'] = clusters
    return clusters


def get_k8s_services():
    try:
        if d['services']:
            LOGGER.info("Found services in cache")
            return d['services']
    except KeyError:
        LOGGER.info("Services not found in cache")
        pass
    url = "{}/api/v1/services".format(host)
    response = requests.get(url, timeout=10, verify=False, headers={
        "Authorization": "Bearer " + TOKEN} if TOKEN else {})

    if response is not None and response.status_code != 200:
        LOGGER.error("Invalid response: {}".format(response.text))
        return None

    services = response.json().get('items')
    LOGGER.info("Adding services to cache")
    d['services'] = services
    return services


def get_k8s_service(namespace, service_name):
    url = "{}/api/v1/namespaces/{}/services/{}".format(
        host, namespace, service_name
    )
    response = requests.get(url, timeout=10, verify=False, headers={
        "Authorization": "Bearer " + TOKEN} if TOKEN else {})

    if response and response.status_code != 200:
        return None

    return response.json()


def get_service_endpoints(service):
    url = "{}/api/v1/namespaces/{}/endpoints/{}".format(
        host, service['metadata']['namespace'], service['metadata']['name'])
    response = requests.get(
        url, timeout=10, verify=False, headers={"Authorization": "Bearer " + TOKEN} if TOKEN else {})

    if response and response.status_code != 200:
        return None

    return response.json()


def get_hosts_from_endpoints(endpoints):
    ports = hosts = list()
    if endpoints:
        ports = list(set([port['port'] for subset in endpoints['subsets']
                          for port in subset['ports']]))
        hosts = [dict(
            ip_address=address['ip'],
            port=ports[0],
            tags={}
        ) for subset in endpoints['subsets'] for address in subset['addresses']]
    return hosts
