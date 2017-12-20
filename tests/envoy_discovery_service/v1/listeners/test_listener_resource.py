import json
import pytest
import responses


class TestListeners():

    @pytest.fixture
    def url(self):
        return '/v1/listeners/test_cluster/test_node'

    #################
    # Test for GET. #
    #################

    @responses.activate
    def test_listener_discovery_service(self, app, k8s_endpoint_responses,
                                        k8s_service_response, k8s_configmap_response,
                                        url):
        responses.add(responses.GET, 'http://localhost:8001/api/v1/services',
                      json=k8s_service_response, status=200)
        for service, namespace in [('kubernetes-dashboard', 'kube-system'),
                                   ('kube-dns', 'kube-system'),
                                   ('kubernetes', 'default')]:
            responses.add(responses.GET, 'http://localhost:8001/api/v1/namespaces/{}/endpoints/{}'.format(
                namespace, service),
                json=k8s_endpoint_responses[service], status=200)
        responses.add(responses.GET, 'http://localhost:8001/api/v1/namespaces/{}/configmaps/{}'.format(
            'kube-system', 'kubernetes-dashboard'),
            json=k8s_configmap_response['example-envoy-service'], status=200)
        response = app.get(url)
        response_data = json.loads(response.data.decode())

        assert response.status_code == 200
        assert response_data is not None
        assert len(response_data['listeners']) == 1
        assert sorted(['mongo_proxy', 'tcp_proxy']) == sorted([filter['name']
                                                               for listener in response_data['listeners']
                                                               for filter in listener['filters']])
