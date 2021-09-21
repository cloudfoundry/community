# Cloud Foundry on Kubernetes: Working Group Charter

## Mission

Bring the ease and simplicity of the Cloud Foundry developer experience to Kubernetes.


## Goals

- End-user developers can deploy their applications through the same convenient flows provided by their existing Cloud Foundry environments, using their existing clients and tools (like the `cf` CLI or the CF Java client), relying on the same (V3) API.
- End-user developers can take advantage of Cloud Foundry via Kubernetes-native APIs, using their existing tools and clients (e.g. `kubectl`, `client-go`).
- End-user developers can smoothly migrate their workloads from their existing Cloud Foundry environments to Cloud Foundry on Kubernetes.
- End-user operators have a robust way to install Cloud Foundry on their Kubernetes clusters.
- End-user operators can reuse their existing Kubernetes infrastructure (e.g. networking, identity, observability) on Cloud Foundry by leveraging its integration points.
- End-users can easily experiment with Cloud Foundry on Kubernetes by installing it on their Kubernetes clusters and having a good out-of-the-box experience.

## Scope

- Develop the necessary components to implement the Cloud Foundry experience on top of Kubernetes.
- Provide default implementations for all integrations (e.g. networking, identity, workload execution, observability).
- Develop a distribution of Cloud Foundry on Kubernetes that is easy to use, even without any Cloud Foundry-specific experience and works out-of-the-box.
- Work with other Working Groups to make sure that the existing Cloud Foundry clients (e.g. the `cf` CLI, the CF Java client) work with Cloud Foundry on Kubernetes out-of-the-box.

## Non-Goals

- Provide full compatibility with the existing Cloud Foundry behaviour.

## Proposed Membership

Technical and Execution Lead: ?

### Approvers

* @Birdrock
* @acosta11
* @akrishna90
* @danail-branekov
* @davewalter
* @gcapizzi
* @georgethebeatle
* @gnovv
* @kieron-dev
* @matt-royal
* @mnitchev
* @tcdowney

## Technical Assets

* https://github.com/cloudfoundry/cf-crd-explorations ???
* https://github.com/cloudfoundry/cf-k8s-api
* https://github.com/cloudfoundry/cf-k8s-controllers
* https://github.com/cloudfoundry-incubator/eirini-controller
