import json
import pytest
import re
import responses


class TestClusterDiscoveryService():

    @pytest.fixture
    def url(self):
        return '/v1/clusters/'

    #################
    # Test for GET. #
    #################

    @responses.activate
    def test_cluster_discovery_service(self, app, url, k8s_service_response):
        responses.add(responses.GET, 'http://localhost:8001/api/v1/services',
                      json=k8s_service_response, status=200)
        response = app.get("{}devtools/devtools".format(url))
        response_data = json.loads(response.data.decode())

        assert response.status_code == 200
        assert response_data is not None
        assert len(response_data['clusters']) == 4
        for cluster in response_data['clusters']:
            assert cluster['type'] == 'static'
            for host in cluster['hosts']:
                assert re.compile("tcp://\w+.*:\d+").match(host['url']) is not None

    @responses.activate
    def test_cluster_discovery_service_external_envoy(
            self, app, url, k8s_service_response, k8s_endpoint_responses):
        responses.add(responses.GET, 'http://localhost:8001/api/v1/services',
                      json=k8s_service_response, status=200)
        responses.add(responses.GET, 'http://localhost:8001/api/v1/namespaces/default/endpoints/kubernetes-dashboard',
                      json=k8s_endpoint_responses['kubernetes-dashboard'], status=200)
        responses.add(responses.GET, 'http://localhost:8001/api/v1/namespaces/default/endpoints/kube-dns',
                      json=k8s_endpoint_responses['kube-dns'], status=200)
        responses.add(responses.GET, 'http://localhost:8001/api/v1/namespaces/default/endpoints/kubernetes',
                      json=k8s_endpoint_responses['kubernetes'], status=200)

        from envoy_discovery_service import app as envoy_app
        envoy_app.config['internal_k8s_envoy'] = False
        response = app.get("{}devtools/devtools".format(url))
        response_data = json.loads(response.data.decode())

        assert response.status_code == 200
        assert response_data is not None
        assert len(response_data['clusters']) == 4
        for cluster in response_data['clusters']:
            assert cluster['type'] == 'static'
            for host in cluster['hosts']:
                assert re.compile("tcp://\d+.\d+.\d+.\d+:\d+").match(host['url']) is not None
