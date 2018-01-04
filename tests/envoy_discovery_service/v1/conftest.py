import pytest
from envoy_discovery_service import app as flask_app


@pytest.fixture(scope='session')
def app(request):
    """An application test client."""
    flask_app.testing = True
    ctx = flask_app.test_request_context()
    ctx.push()

    # Pop the request context after each request.
    request.addfinalizer(ctx.pop)
    test_client = flask_app.test_client()
    return test_client


@pytest.fixture
def k8s_service_response():
    return {
        "kind": "ServiceList",
        "apiVersion": "v1",
        "metadata": {
                "selfLink": "/api/v1/services",
                "resourceVersion": "197380"
        },
        "items": [
            {
                "metadata": {
                    "name": "kubernetes",
                    "namespace": "default",
                    "selfLink": "/api/v1/namespaces/default/services/kubernetes",
                                "uid": "0f201149-ba7c-11e7-b775-08002771376b",
                                "resourceVersion": "6",
                                "creationTimestamp": "2017-10-26T18:32:45Z",
                                "labels": {
                                    "component": "apiserver",
                                    "provider": "kubernetes"
                                }
                },
                "spec": {
                    "ports": [
                        {
                            "name": "https",
                            "protocol": "TCP",
                            "port": 443,
                            "targetPort": 8443
                        }
                    ],
                    "clusterIP": "10.0.0.1",
                    "type": "ClusterIP",
                    "sessionAffinity": "ClientIP"
                },
                "status": {
                    "loadBalancer": {}
                }
            },
            {
                "metadata": {
                    "name": "kube-dns",
                    "namespace": "kube-system",
                    "selfLink": "/api/v1/namespaces/kube-system/services/kube-dns",
                                "uid": "19e2873a-ba7c-11e7-b775-08002771376b",
                                "resourceVersion": "145",
                                "creationTimestamp": "2017-10-26T18:33:03Z",
                                "labels": {
                                    "addonmanager.kubernetes.io/mode": "Reconcile",
                                    "k8s-app": "kube-dns",
                                    "kubernetes.io/name": "KubeDNS"
                                },
                    "annotations": {
                                    "kubectl.kubernetes.io/last-applied-configuration": "{\"apiVersion\":\"v1\",\"kind\":\"Service\",\"metadata\":{\"annotations\":{},\"labels\":{\"addonmanager.kubernetes.io/mode\":\"Reconcile\",\"k8s-app\":\"kube-dns\",\"kubernetes.io/name\":\"KubeDNS\"},\"name\":\"kube-dns\",\"namespace\":\"kube-system\"},\"spec\":{\"clusterIP\":\"10.0.0.10\",\"ports\":[{\"name\":\"dns\",\"port\":53,\"protocol\":\"UDP\"},{\"name\":\"dns-tcp\",\"port\":53,\"protocol\":\"TCP\"}],\"selector\":{\"k8s-app\":\"kube-dns\"}}}\n"
                                }
                },
                "spec": {
                    "ports": [
                        {
                            "name": "dns",
                            "protocol": "UDP",
                            "port": 53,
                            "targetPort": 53
                        },
                        {
                            "name": "dns-tcp",
                            "protocol": "TCP",
                            "port": 53,
                            "targetPort": 53
                        }
                    ],
                    "selector": {
                        "k8s-app": "kube-dns"
                    },
                    "clusterIP": "10.0.0.10",
                    "type": "ClusterIP",
                    "sessionAffinity": "None"
                },
                "status": {
                    "loadBalancer": {}
                }
            },
            {
                "metadata": {
                    "name": "kubernetes-dashboard",
                    "namespace": "kube-system",
                    "selfLink": "/api/v1/namespaces/kube-system/services/kubernetes-dashboard",
                                "uid": "19c46cc4-ba7c-11e7-b775-08002771376b",
                                "resourceVersion": "129",
                                "creationTimestamp": "2017-10-26T18:33:02Z",
                                "labels": {
                                    "addonmanager.kubernetes.io/mode": "Reconcile",
                                    "app": "kubernetes-dashboard",
                                    "kubernetes.io/minikube-addons": "dashboard",
                                    "kubernetes.io/minikube-addons-endpoint": "dashboard",
                                    "envoyEnabled": "true"
                                },
                    "annotations": {
                                    "kubectl.kubernetes.io/last-applied-configuration": "{\"apiVersion\":\"v1\",\"kind\":\"Service\",\"metadata\":{\"annotations\":{},\"labels\":{\"addonmanager.kubernetes.io/mode\":\"Reconcile\",\"app\":\"kubernetes-dashboard\",\"kubernetes.io/minikube-addons\":\"dashboard\",\"kubernetes.io/minikube-addons-endpoint\":\"dashboard\"},\"name\":\"kubernetes-dashboard\",\"namespace\":\"kube-system\"},\"spec\":{\"ports\":[{\"nodePort\":30000,\"port\":80,\"targetPort\":9090}],\"selector\":{\"app\":\"kubernetes-dashboard\"},\"type\":\"NodePort\"}}\n"
                                }
                },
                "spec": {
                    "ports": [
                        {
                            "protocol": "TCP",
                            "port": 80,
                            "targetPort": 9090,
                            "nodePort": 30000
                        }
                    ],
                    "selector": {
                        "app": "kubernetes-dashboard"
                    },
                    "clusterIP": "10.0.0.241",
                    "type": "NodePort",
                    "sessionAffinity": "None",
                    "externalTrafficPolicy": "Cluster"
                },
                "status": {
                    "loadBalancer": {}
                }
            },
            {
                "metadata": {
                    "name": "mongo_no_cluster_ip",
                    "namespace": "default",
                    "selfLink": "/api/v1/namespaces/default/services/mongo",
                                "uid": "60ca4ee4-e07c-11e7-8511-122cc2daa808",
                                "resourceVersion": "1377050",
                                "creationTimestamp": "2017-12-14T03:10:46Z",
                                "labels": {
                                    "name": "mongo_no_cluster_ip"
                                }
                },
                "spec": {
                    "ports": [
                        {
                            "protocol": "TCP",
                            "port": 27017,
                            "targetPort": 27017
                        }
                    ],
                    "selector": {
                        "role": "mongo_no_cluster_ip"
                    },
                    "clusterIP": "None",
                    "type": "ClusterIP",
                    "sessionAffinity": "None"
                },
                "status": {
                    "loadBalancer": {}
                }
            }
        ]
    }


@pytest.fixture
def k8s_endpoint_responses():
    return {
        "kubernetes-dashboard": {
            "kind": "Endpoints",
            "apiVersion": "v1",
            "metadata": {
                    "name": "kubernetes-dashboard",
                    "namespace": "kube-system",
                    "selfLink": "/api/v1/namespaces/kube-system/endpoints/kubernetes-dashboard",
                    "uid": "19c75967-ba7c-11e7-b775-08002771376b",
                    "resourceVersion": "206874",
                    "creationTimestamp": "2017-10-26T18:33:02Z",
                    "labels": {
                            "addonmanager.kubernetes.io/mode": "Reconcile",
                            "app": "kubernetes-dashboard",
                            "kubernetes.io/minikube-addons": "dashboard",
                            "kubernetes.io/minikube-addons-endpoint": "dashboard"
                    }
            },
            "subsets": [
                {
                    "addresses": [
                        {
                            "ip": "172.17.0.2",
                            "nodeName": "minikube",
                            "targetRef": {
                                "kind": "Pod",
                                "namespace": "kube-system",
                                "name": "kubernetes-dashboard-6zgkm",
                                "uid": "19bc438f-ba7c-11e7-b775-08002771376b",
                                "resourceVersion": "206872"
                            }
                        }
                    ],
                    "ports": [
                        {
                            "port": 9090,
                            "protocol": "TCP"
                        }
                    ]
                }
            ]
        },
        "kube-dns": {
            "kind": "Endpoints",
            "apiVersion": "v1",
            "metadata": {
                    "name": "kube-dns",
                    "namespace": "kube-system",
                    "selfLink": "/api/v1/namespaces/kube-system/endpoints/kube-dns",
                    "uid": "19e360af-ba7c-11e7-b775-08002771376b",
                    "resourceVersion": "206958",
                    "creationTimestamp": "2017-10-26T18:33:03Z",
                    "labels": {
                            "addonmanager.kubernetes.io/mode": "Reconcile",
                            "k8s-app": "kube-dns",
                            "kubernetes.io/name": "KubeDNS"
                    }
            },
            "subsets": [
                {
                    "addresses": [
                        {
                            "ip": "172.17.0.6",
                            "nodeName": "minikube",
                            "targetRef": {
                                "kind": "Pod",
                                "namespace": "kube-system",
                                "name": "kube-dns-1326421443-c93zf",
                                "uid": "19d30771-ba7c-11e7-b775-08002771376b",
                                "resourceVersion": "206956"
                            }
                        }
                    ],
                    "ports": [
                        {
                            "name": "dns",
                            "port": 53,
                            "protocol": "UDP"
                        },
                        {
                            "name": "dns-tcp",
                            "port": 53,
                            "protocol": "TCP"
                        }
                    ]
                }
            ]
        },
        "kubernetes": {
            "kind": "Endpoints",
            "apiVersion": "v1",
            "metadata": {
                    "name": "kubernetes",
                    "namespace": "default",
                    "selfLink": "/api/v1/namespaces/default/endpoints/kubernetes",
                    "uid": "0f20af4d-ba7c-11e7-b775-08002771376b",
                    "resourceVersion": "7",
                    "creationTimestamp": "2017-10-26T18:32:45Z"
            },
            "subsets": [
                {
                    "addresses": [
                        {
                            "ip": "10.0.2.15"
                        }
                    ],
                    "ports": [
                        {
                            "name": "https",
                            "port": 8443,
                            "protocol": "TCP"
                        }
                    ]
                }
            ]
        }
    }


@pytest.fixture
def k8s_configmap_response():
    return {
        "envoy-config": {
            "kind": "ConfigMap",
            "apiVersion": "v1",
            "metadata": {
                    "name": "envoy-config",
                    "namespace": "default",
                    "selfLink": "/api/v1/namespaces/default/configmaps/envoy-config",
                    "uid": "b9853f7e-da8c-11e7-85fc-08002771376b",
                    "resourceVersion": "298406",
                    "creationTimestamp": "2017-12-06T13:52:40Z"
            },
            "data": {
                "envoy.config": "listeners: []\nadmin:\n  access_log_path: \"/dev/null\"\n  address: tcp://0.0.0.0:8001\ncluster_manager:\n  cds:\n    cluster:\n      name: envoy-cds\n      connect_timeout_ms: 250\n      type: strict_dns\n      lb_type: round_robin\n      hosts:\n      - url: tcp://envoy-discovery-service:5000\n    refresh_delay_ms: 15000\n  sds:\n    cluster:\n      name: envoy-sds\n      connect_timeout_ms: 250\n      type: strict_dns\n      lb_type: round_robin\n      hosts:\n      - url: tcp://envoy-discovery-service:5000\n    refresh_delay_ms: 15000\n  clusters:\n  - name: envoy-lds\n    connect_timeout_ms: 250\n    type: strict_dns\n    lb_type: round_robin\n    hosts:\n    - url: tcp://envoy-discovery-service:5000\nlds:\n  cluster: envoy-lds\n  refresh_delay_ms: 10000\n"
            }
        },
        "example-envoy-service": {
            "kind": "ConfigMap",
            "apiVersion": "v1",
            "metadata": {
                    "name": "example_config",
                    "namespace": "default",
                    "selfLink": "/api/v1/namespaces/default/configmaps/example_config",
                    "uid": "b9853f7e-da8c-11e7-85fc-08002771376b",
                    "resourceVersion": "298406",
                    "creationTimestamp": "2017-12-06T13:52:40Z"
            },
            "data": {
                "envoy.config": 'filters:\n  - type: tcp_proxy\n    config:\n      access_log:\n        - path: "dev/stdout"\n      stat_prefix: "mongo_27017"\n      route_config:\n        routes:\n          - cluster: "mongo_27017"\n  - type: mongo_proxy\n    config:\n      access_log: "dev/stdout"\n      stat_prefix: "mongo_27017"\n'
            }
        }
    }
