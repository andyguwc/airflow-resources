# Kubernetes 

## Why Kubernetes

How to manage all of the containers in test/stage/production 
Docker-compose doesn't handle load balancing

Kubernetes
- package up an app
- not worry about management of containers
- self-heal containers
- robust way to scale and load balance containers 
- update containers without bringing down the application 
- robust networking and persisten storage options 


## Kubernets Concepts 
Automating deployment, scaling, and management of containerized applications
Provides declarative way to define a cluster's state using manifest files (YAML)
Interact with Kubernetes using kubectl 

Features
- load balancing 
- storage orchestration
- automate rollouts / rollbacks
- manage workloads 
- self-healding 
- secrets and configuration management 
- horizontal scaling 

Cluster 
- Master node in charge of worker nodes
- Nodes have pods


## Deployment and Services
Run Kubernetes Locally 
- Use Docker Desktop and enable Kubernetes

Describe desired state 
Replicate pods to scale out 
Support rolling updates and rollbacks 

Service takes care of changing pods IPs

Converting from Docker Compose to Kubernetes
- compose on Kubernetes which runs on Docker desktop 
https://github.com/docker/compose-on-kubernetes


## Kubernetes Commands
$ kubectl version 

$ kubectl get [deployments | services | pods]

$ kubectl run nginx-server --image=nginx:alpine 

$ kubectl apply -f [fileName | folderName]

$ kubectl delete -f [fileName | folderName]
