# Task 1
```shell
[nix-shell:~/code/DevOps]$ nix-shell -p kubernetes-helm

[nix-shell:~/code/DevOps]$ which helm
/nix/store/8pcwyp9faqdz015mzca78k1pvi2m86rz-kubernetes-helm-3.19.1/bin/helm

[nix-shell:~/code/DevOps]$ helm version
version.BuildInfo{Version:"v3.19.1", GitCommit:"v3.19.1", GitTreeState:"", GoVersion:"go1.25.5"}

[nix-shell:~/code/DevOps]$ helm show chart prometheus-community/prometheus
annotations:
  artifacthub.io/license: Apache-2.0
  artifacthub.io/links: |
    - name: Chart Source
      url: https://github.com/prometheus-community/helm-charts
    - name: Upstream Project
      url: https://github.com/prometheus/prometheus
apiVersion: v2
appVersion: v3.10.0
dependencies:
- condition: alertmanager.enabled
  name: alertmanager
  repository: https://prometheus-community.github.io/helm-charts
  version: 1.34.*
- condition: kube-state-metrics.enabled
  name: kube-state-metrics
  repository: https://prometheus-community.github.io/helm-charts
  version: 7.2.*
- condition: prometheus-node-exporter.enabled
  name: prometheus-node-exporter
  repository: https://prometheus-community.github.io/helm-charts
  version: 4.52.*
- condition: prometheus-pushgateway.enabled
  name: prometheus-pushgateway
  repository: https://prometheus-community.github.io/helm-charts
  version: 3.6.*
description: Prometheus is a monitoring system and time series database.
home: https://prometheus.io/
icon: https://raw.githubusercontent.com/prometheus/prometheus.github.io/master/assets/prometheus_logo-cb55bb5c346.png
keywords:
- monitoring
- prometheus
kubeVersion: '>=1.19.0-0'
maintainers:
- email: gianrubio@gmail.com
  name: gianrubio
  url: https://github.com/gianrubio
- email: zanhsieh@gmail.com
  name: zanhsieh
  url: https://github.com/zanhsieh
- email: miroslav.hadzhiev@gmail.com
  name: Xtigyro
  url: https://github.com/Xtigyro
- email: naseem@transit.app
  name: naseemkullah
  url: https://github.com/naseemkullah
- email: rootsandtrees@posteo.de
  name: zeritti
  url: https://github.com/zeritti
name: prometheus
sources:
- https://github.com/prometheus/alertmanager
- https://github.com/prometheus/prometheus
- https://github.com/prometheus/pushgateway
- https://github.com/prometheus/node_exporter
- https://github.com/kubernetes/kube-state-metrics
type: application
version: 28.14.1
```

# Task 2
```shell
[nix-shell:~/code/DevOps/k8s/mychart]$ helm lint .
==> Linting .
[INFO] Chart.yaml: icon is recommended

1 chart(s) linted, 0 chart(s) failed

[nix-shell:~/code/DevOps/k8s/mychart]$ helm template mychart .
---
# Source: infoservice/templates/serviceaccount.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: mychart-infoservice
  labels:
    helm.sh/chart: infoservice-0.1.0
    app.kubernetes.io/name: infoservice
    app.kubernetes.io/instance: mychart
    app.kubernetes.io/version: "1.16.0"
    app.kubernetes.io/managed-by: Helm
automountServiceAccountToken: true
---
# Source: infoservice/templates/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: infoservice-service

spec:
  type: NodePort
  selector:
    app: infoservice
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
      nodePort: 30080
---
# Source: infoservice/templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: infoservices
  labels:
    app: infoservice

spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0

  replicas: 3
  selector:
    matchLabels:
      app: infoservice

  template:
    metadata:
      labels:
        app: infoservice
    spec:
      containers:
      - name: infoservice
        image: ub3rch/infoservice:go-latest
        imagePullPolicy: "Always"

        resources:
        livenessProbe: map[httpGet:map[initialDelaySeconds:10 path:/health periodSeconds:5 port:8000]]
        readinessProbe: map[httpGet:map[initialDelaySeconds:10 path:/health periodSeconds:5 port:8000]]
---
# Source: infoservice/templates/tests/test-connection.yaml
apiVersion: v1
kind: Pod
metadata:
  name: "mychart-infoservice-test-connection"
  labels:
    helm.sh/chart: infoservice-0.1.0
    app.kubernetes.io/name: infoservice
    app.kubernetes.io/instance: mychart
    app.kubernetes.io/version: "1.16.0"
    app.kubernetes.io/managed-by: Helm
  annotations:
    "helm.sh/hook": test
spec:
  containers:
    - name: wget
      image: busybox
      command: ['wget']
      args: ['mychart-infoservice:80']
  restartPolicy: Never
[nix-shell:~/code/DevOps/k8s/mychart]$ helm install --dry-run --debug test-release .
install.go:225: 2026-04-02 10:48:22.587617915 +0300 MSK m=+0.027976450 [debug] Original chart version: ""
install.go:242: 2026-04-02 10:48:22.587653483 +0300 MSK m=+0.028012008 [debug] CHART PATH: /home/uber/code/DevOps/k8s/mychart

Error: INSTALLATION FAILED: Kubernetes cluster unreachable: Get "https://192.168.49.2:8443/version": dial tcp 192.168.49.2:8443: connect: no route to host
helm.go:92: 2026-04-02 10:48:25.669685879 +0300 MSK m=+3.110044445 [debug] Get "https://192.168.49.2:8443/version": dial tcp 192.168.49.2:8443: connect: no route to host
Kubernetes cluster unreachable
helm.sh/helm/v3/pkg/kube.(*Client).IsReachable
	helm.sh/helm/v3/pkg/kube/client.go:137
helm.sh/helm/v3/pkg/action.(*Install).RunWithContext
	helm.sh/helm/v3/pkg/action/install.go:236
main.runInstall
	helm.sh/helm/v3/cmd/helm/install.go:317
main.newInstallCmd.func2
	helm.sh/helm/v3/cmd/helm/install.go:156
github.com/spf13/cobra.(*Command).execute
	github.com/spf13/cobra@v1.10.1/command.go:1015
github.com/spf13/cobra.(*Command).ExecuteC
	github.com/spf13/cobra@v1.10.1/command.go:1148
github.com/spf13/cobra.(*Command).Execute
	github.com/spf13/cobra@v1.10.1/command.go:1071
main.main
	helm.sh/helm/v3/cmd/helm/helm.go:91
runtime.main
	runtime/proc.go:285
runtime.goexit
	runtime/asm_amd64.s:1693
INSTALLATION FAILED
main.newInstallCmd.func2
	helm.sh/helm/v3/cmd/helm/install.go:158
github.com/spf13/cobra.(*Command).execute
	github.com/spf13/cobra@v1.10.1/command.go:1015
github.com/spf13/cobra.(*Command).ExecuteC
	github.com/spf13/cobra@v1.10.1/command.go:1148
github.com/spf13/cobra.(*Command).Execute
	github.com/spf13/cobra@v1.10.1/command.go:1071
main.main
	helm.sh/helm/v3/cmd/helm/helm.go:91
runtime.main
	runtime/proc.go:285
runtime.goexit
	runtime/asm_amd64.s:1693
```
