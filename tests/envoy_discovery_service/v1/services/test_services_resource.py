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
    def test_service_discovery_service(self, app, url, k8s_endpoint_responses):
        responses.add(responses.GET, 'https://kubernetes/api/v1/namespaces/default/endpoints/kubernetes-dashboard',
                      json=k8s_endpoint_responses['kubernetes-dashboard'], status=200)
        response = app.get("{}/{}".format(url, 'kubernetes-dashboard'))
        response_data = json.loads(response.data.decode())

        assert response.status_code == 200
        assert response_data is not None
        assert len(response_data['hosts']) > 0
        for host in response_data['hosts']:
            for key in ['ip_address', 'port', 'tags']:
                assert key in host
