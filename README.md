# kubernetes-envoy-discovery

Kubernetes Envoy Discovery Service

This flask application implements V1 of Envoy's Discovery Services

  * [Listener Discovery Service](https://www.envoyproxy.io/docs/envoy/latest/api-v1/listeners/lds)
  * [Cluster Discovery Service](https://www.envoyproxy.io/docs/envoy/latest/api-v1/cluster_manager/cds)
  * [Service Discovery Service](https://www.envoyproxy.io/docs/envoy/latest/api-v1/cluster_manager/sds.html#config-cluster-manager-sds-api)

The intent is to have this service running inside of Kubernetes, and Envoy running as an Edge Proxy outside of Kubernetes.

Example yaml for deployment of discovery service:

```
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  labels:
    name: envoy-discovery-service
  name: envoy-discovery-service
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      name: envoy-discovery-service
  strategy:
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 1
    type: RollingUpdate
  template:
    metadata:
      creationTimestamp: null
      labels:
        name: envoy-discovery-service
    spec:
      containers:
      - image: mmontg1/kubernetes-envoy-discovery:0.2.21
        imagePullPolicy: IfNotPresent
        name: envoy-discovery-service
        ports:
        - containerPort: 5000
          protocol: TCP
        env:
          - name: INTERNAL_K8S_ENVOY  # Is envoy going to be running inside kubernetes?
            value: "false"
          # - name: SERVICE_IP_OVERRIDE  # This is intended for dev environments (such as minikube), where you need to override the exposed ip.
          #   value: "192.168.99.101"
        resources:
          limits:
            cpu: 500m
            memory: 2500Mi
          requests:
            cpu: 100m
            memory: 100Mi
      restartPolicy: Always
      securityContext: {}
      terminationGracePeriodSeconds: 30

---
apiVersion: v1
kind: Service
metadata:
  name: envoy-discovery-service
  namespace: default
spec:
  ports:
  - port: 5000
    protocol: TCP
    targetPort: 5000
  selector:
    name: envoy-discovery-service
  type: LoadBalancer

```

Requirements to expose a service within Kubernetes using Envoy:

  1. Service exists within Kubernetes that has a label `envoyEnabled: 'true'`

  ```
      apiVersion: v1
      kind: Service
      metadata:
        name: your-service-name
        namespace: default
        labels:
          name: your-service-name
          envoyEnabled: 'true'
      spec:
        ports:
        - port: 8080
          protocol: TCP
          targetPort: 8080
        selector:
          name: your-service-name
        type: NodePort
  ```

  2. ConfigMap exists within Kubernetes, named the same as the service, with a key named `envoy.config` that defines the proper filters for the service:  (Any filters are supported, such as: http filters, tcp_proxy, mongo_proxy, redis_proxy)

  ```
      apiVersion: v1
      data:
        envoy.config: |
          filters:
          - type: tcp_proxy
            config:
              access_log:
                - path: "/dev/stdout"
              stat_prefix: "your-service-name_8080"
              route_config:
                routes:
                  - cluster: "your-service-name_8080"
                    source_ip_list:
                      - "8.8.8.8/32"
          - type: mongo_proxy
            config:
              access_log: "/dev/stdout"
              stat_prefix: "your-service-name_8080"
      kind: ConfigMap
      metadata:
        name: your-service-name
        namespace: default

  ```

---
Full Example

```
apiVersion: v1
kind: Namespace
metadata:
  name: default
  labels:
    name: default
---
apiVersion: apps/v1beta1
kind: Deployment
metadata:
  labels:
    name: your-service-name
  name: your-service-name
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      name: your-service-name
  strategy:
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 1
    type: RollingUpdate
  template:
    metadata:
      creationTimestamp: null
      labels:
        name: your-service-name
    spec:
      containers:
      - name: nginx
        image: nginx:1.7.9
        ports:
        - containerPort: 80
          protocol: TCP
          targetPort: 8080

---
apiVersion: v1
kind: Service
metadata:
  name: your-service-name
  namespace: default
  labels:
    name: your-service-name
    envoyEnabled: 'true'
spec:
  ports:
  - port: 8080
    protocol: TCP
    targetPort: 8080
  selector:
    name: your-service-name
  type: NodePort
---
apiVersion: v1
data:
  envoy.config: |
    filters:
    - type: tcp_proxy
      config:
        access_log:
          - path: "/dev/stdout"
        stat_prefix: "your-service-name_8080"
        route_config:
          routes:
            - cluster: "your-service-name_8080"
              source_ip_list:
                - "8.8.8.8/32"
kind: ConfigMap
metadata:
  name: your-service-name
  namespace: default
```
