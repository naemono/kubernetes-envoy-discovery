import json
import pytest
import responses


class TestServiceDiscoveryService():

    @pytest.fixture
    def url(self):
        return "/v1/registration"

    #################
    # Test for GET. #
    #################

    @responses.activate
    def test_service_discovery_service(self, app, url, k8s_endpoint_responses, k8s_service_response):
        responses.add(responses.GET, 'https://kubernetes/api/v1/namespaces/kube-system/endpoints/kubernetes-dashboard',
                      json=k8s_endpoint_responses['kubernetes-dashboard'], status=200)
        service_responses = [item for item in k8s_service_response['items']
                             if item['metadata']['name'] == 'kubernetes-dashboard']
        responses.add(responses.GET, 'https://kubernetes/api/v1/namespaces/default/services/kubernetes-dashboard',
                      json=service_responses[0], status=200)
        response = app.get("{}/{}".format(url, 'kubernetes-dashboard'))
        response_data = json.loads(response.data.decode())

        assert response.status_code == 200
        assert response_data is not None
        assert len(response_data['hosts']) > 0
        for host in response_data['hosts']:
            for key in ['ip_address', 'port', 'tags']:
                assert key in host
