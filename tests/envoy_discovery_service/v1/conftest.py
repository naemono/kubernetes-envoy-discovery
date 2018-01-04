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
                            "ip": "10.0.2.15",
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


@pytest.fixture
def k8s_get_node_response():
    return {
        "kind": "Node",
        "apiVersion": "v1",
        "metadata": {
                "name": "ip-172-18-1-157",
                "selfLink": "/api/v1/nodes/ip-172-18-1-157",
                "uid": "819e6d8f-da11-11e7-84c2-123f55055d54",
                "resourceVersion": "5067716",
                "creationTimestamp": "2017-12-05T23:10:38Z",
                "labels": {
                        "beta.kubernetes.io/arch": "amd64",
                        "beta.kubernetes.io/os": "linux",
                        "kubernetes.io/hostname": "ip-172-18-1-157"
                },
            "annotations": {
                    "node.alpha.kubernetes.io/ttl": "0",
                    "volumes.kubernetes.io/controller-managed-attach-detach": "true"
                }
        },
        "spec": {
            "externalID": "ip-172-18-1-157",
            "providerID": "aws:////i-028049a53bbd39a5a"
        },
        "status": {
            "capacity": {
                "cpu": "2",
                "memory": "7657864Ki",
                "pods": "110"
            },
            "allocatable": {
                "cpu": "2",
                "memory": "7555464Ki",
                "pods": "110"
            },
            "conditions": [
                {
                    "type": "OutOfDisk",
                    "status": "False",
                    "lastHeartbeatTime": "2018-01-04T20:11:43Z",
                    "lastTransitionTime": "2017-12-05T23:10:38Z",
                    "reason": "KubeletHasSufficientDisk",
                    "message": "kubelet has sufficient disk space available"
                },
                {
                    "type": "MemoryPressure",
                    "status": "False",
                    "lastHeartbeatTime": "2018-01-04T20:11:43Z",
                    "lastTransitionTime": "2017-12-05T23:10:38Z",
                    "reason": "KubeletHasSufficientMemory",
                    "message": "kubelet has sufficient memory available"
                },
                {
                    "type": "DiskPressure",
                    "status": "False",
                    "lastHeartbeatTime": "2018-01-04T20:11:43Z",
                    "lastTransitionTime": "2017-12-05T23:10:38Z",
                    "reason": "KubeletHasNoDiskPressure",
                    "message": "kubelet has no disk pressure"
                },
                {
                    "type": "Ready",
                    "status": "True",
                    "lastHeartbeatTime": "2018-01-04T20:11:43Z",
                    "lastTransitionTime": "2017-12-29T03:18:52Z",
                    "reason": "KubeletReady",
                    "message": "kubelet is posting ready status. AppArmor enabled"
                }
            ],
            "addresses": [
                {
                    "type": "InternalIP",
                    "address": "172.18.1.157"
                },
                {
                    "type": "Hostname",
                    "address": "ip-172-18-1-157"
                }
            ],
            "daemonEndpoints": {
                "kubeletEndpoint": {
                    "Port": 10250
                }
            },
            "nodeInfo": {
                "machineID": "7d58a647025f4f859239a26dbd382626",
                "systemUUID": "EC2F6EF4-F3A5-CF72-F1E8-37AB470E4AFD",
                "bootID": "ad33d245-9cf5-4794-b558-40b911c52d85",
                "kernelVersion": "4.4.0-1041-aws",
                "osImage": "Ubuntu 16.04.3 LTS",
                "containerRuntimeVersion": "docker://1.13.1",
                "kubeletVersion": "v1.8.6",
                "kubeProxyVersion": "v1.8.6",
                "operatingSystem": "linux",
                "architecture": "amd64"
            },
            "images": [
                {
                    "names": [
                        "mongo@sha256:c78f6debfb5b10fe2ed390105a729123f3365a33e5aada6f5539922d1d7c75dc",
                        "mongo:latest"
                    ],
                    "sizeBytes": 365626069
                },
                {
                    "names": [
                        "gcr.io/google_containers/nginx-ingress-controller@sha256:c9d2e67f8096d22564a6507794e1a591fbcb6461338fc655a015d76a06e8dbaa",
                        "gcr.io/google_containers/nginx-ingress-controller:0.9.0-beta.13"
                    ],
                    "sizeBytes": 116899281
                },
                {
                    "names": [
                        "mmontg1/kubernetes-envoy-discovery@sha256:555cacaf490bd1a8644d104303d6c550c987b3508dddbe0ed503c9b6d4c487ea",
                        "mmontg1/kubernetes-envoy-discovery:0.2.23"
                    ],
                    "sizeBytes": 97968351
                },
                {
                    "names": [
                        "mmontg1/kubernetes-envoy-discovery@sha256:63f0cbe8cf62577a07bd0c26700067deb4ebc524cdacb9d753671b9b5be9da35",
                        "mmontg1/kubernetes-envoy-discovery:0.2.24"
                    ],
                    "sizeBytes": 97965128
                },
                {
                    "names": [
                        "mmontg1/kubernetes-envoy-discovery@sha256:d4379f09250dc1335d03431a1167f13da32d8302deedbf7cb894c422728e4b27",
                        "mmontg1/kubernetes-envoy-discovery:0.2.22"
                    ],
                    "sizeBytes": 97965080
                },
                {
                    "names": [
                        "alanrack/testing@sha256:fb34a167a5c14257d11d0f2794ecb34171a01eb9569a2a069ad77d3b8d80cfd1",
                        "alanrack/testing:backend"
                    ],
                    "sizeBytes": 85374473
                },
                {
                    "names": [
                        "gcr.io/google_containers/heapster-amd64@sha256:8e04183590f937c274fb95c1397ea0c6b919645c765862e2cc9cb80f097a8fb4",
                        "gcr.io/google_containers/heapster-amd64:v1.4.3"
                    ],
                    "sizeBytes": 73412845
                },
                {
                    "names": [
                        "lachlanevenson/k8s-kubectl@sha256:9ef2e2ffa63fc22705d7f453a1fe46b36cd9e44901e123933c68f4fb3c0cda13",
                        "lachlanevenson/k8s-kubectl:latest"
                    ],
                    "sizeBytes": 57032575
                },
                {
                    "names": [
                        "gcr.io/google_containers/addon-resizer@sha256:dcec9a5c2e20b8df19f3e9eeb87d9054a9e94e71479b935d5cfdbede9ce15895",
                        "gcr.io/google_containers/addon-resizer:1.7"
                    ],
                    "sizeBytes": 38983736
                },
                {
                    "names": [
                        "alanrack/testing@sha256:a99ea95f4ff6db727a3e265ca285bc3afa6c850c3f5b7823982db5976823a9e2",
                        "alanrack/testing:frontend"
                    ],
                    "sizeBytes": 17716206
                },
                {
                    "names": [
                        "dontrebootme/microbot@sha256:ec71565e9cad762bdbd3ecc382b26162f07cea81a803861bc1e5099758e46ee0",
                        "dontrebootme/microbot:v1"
                    ],
                    "sizeBytes": 6807909
                },
                {
                    "names": [
                        "gcr.io/google_containers/pause-amd64@sha256:163ac025575b775d1c0f9bf0bdd0f086883171eb475b5068e7defa4ca9e76516",
                        "gcr.io/google_containers/pause-amd64:3.0"
                    ],
                    "sizeBytes": 746888
                }
            ]
        }
    }
