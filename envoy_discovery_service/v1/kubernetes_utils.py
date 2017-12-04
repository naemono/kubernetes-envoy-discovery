import requests


def _get_pods_by_selector(selectors):
    url = 'https://kubernetes/api/v1/namespaces/default/pods'
    response = requests.get(url, timeout=10, params=selectors)

    if response and response.status_code != 200:
        return None

    return response.json().get('items')


def _get_service_endpoints(service):
    url = "https://kubernetes/api/v1/namespaces/{}/endpoints/{}".format(service['metadata']['namespace'],
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


def get_listeners_from_services(services):
    listeners = list()
    for service in services:
        endpoints = get_service_endpoints(service['metadata']['name'])
        for port in list(set([port['port'] for subset in endpoints['subsets']
                              for port in subset['ports']])):
            listeners.append(dict(
                address="tcp://0.0.0.0:{}".format(port),
                filters=[dict(
                    name="{}_{}".format(service['metadata']['name'], port),
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
                                    prefix="/{}_{}".format(service['metadata']['name'], port),
                                    cluster="{}_{}".format(service['metadata']['name'], port)
                                )]
                            )]
                        ),
                        filters=dict(name="router", config={})
                    )
                )]
            ))
    return listeners


def get_clusters_from_services(services, internal_k8s_envoy=True):
    clusters = list()
    for service in services:
        for port in service['spec']['ports']:
            if internal_k8s_envoy:
                hosts = [dict(url="tcp://{}:{}".format(service['metadata']['name'],
                                                       port['port']))]
            else:
                hosts = [dict(url="tcp://{}:{}".format(address['ip'], port['port']))
                         for subset in get_service_endpoints(service['metadata']['name'])['subsets']
                         for address in subset['addresses']]
            clusters.append(dict(
                name="{}_{}".format(service['metadata']['name'], port['port']),
                connect_timeout_ms=250,
                type="strict_dns" if internal_k8s_envoy else "static",
                lb_type="round_robin",
                features="http2",
                hosts=hosts
            ))
    return clusters


def get_k8s_services():
    url = 'https://kubernetes/api/v1/services'
    response = requests.get(url, timeout=10)

    if response and response.status_code != 200:
        return None

    return response.json().get('items')


def get_service_endpoints(service, namespace='default'):
    url = "https://kubernetes/api/v1/namespaces/{}/endpoints/{}".format(namespace, service)
    response = requests.get(url, timeout=10)

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
