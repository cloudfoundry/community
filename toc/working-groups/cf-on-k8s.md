# Cloud Foundry on Kubernetes: Working Group Charter

## Mission

Bring the ease and simplicity of the Cloud Foundry developer experience to Kubernetes.


## Goals

- End-user developers can deploy existing Cloud Foundry-compatible applications to Kubernetes-based environments using workflows that employ official Cloud Foundry clients (such as the `cf` CLI and the CF Java client) or (v3) Cloud Foundry API calls.
- End-user developers can take advantage of Cloud Foundry via Kubernetes-native APIs using existing Kubernetes tools and clients (such as `kubectl` and `client-go`).
- End-user developers can smoothly migrate their workloads from their existing Cloud Foundry environments to Cloud Foundry environments on Kubernetes.
- End-user operators can reuse their existing Kubernetes infrastructure and related integrations (for example, networking, identity, and observability) in their Cloud Foundry deployments.
- End-users can easily try out and experiment with Cloud Foundry on Kubernetes on their own Kubernetes clusters, with a good out-of-the-box experience.
- Vendors can base their own CF distributions on the core components of Cloud Foundry on Kubernetes.

## Scope

- Develop the necessary components to implement the Cloud Foundry experience on top of Kubernetes.
- Provide basic implementations by default for all Cloud Foundry subsystem integratios (for example, networking, identity, workload execution, and observability).
- Develop a deployment of Cloud Foundry on Kubernetes that is easy to use out-of-the-box without any prior experience with Cloud Foundry.
- Work with other Working Groups to make sure that existing Cloud Foundry clients (such as the `cf` CLI and the CF Java client) work with Cloud Foundry on Kubernetes out-of-the-box.

## Non-Goals

- Provide full compatibility with the existing Cloud Foundry behaviour.

## Roles & Technical Assets

```yaml
name: CF on K8s
execution_leads:
- name: Georgi Sabev
  github: georgethebeatle
technical_leads:
- name: Danail Branekov
  github: danail-branekov
bots:
- name: korifi-bot
  github: korifi-bot
areas:
- name: Korifi
  approvers:
  - name: Andrew Costa
    github: acosta11
  - name: Andrew Wittrock
    github: Birdrock
  - name: Dave Walter
    github: davewalter
  - name: Julian Hjortshoj
    github: julian-hj
  - name: Tim Downey
    github: tcdowney
  - name: Yusmen Zabanov
    github: uzabanov
  - name: Robert Gogolok
    github: gogolok
  repositories:
  - cloudfoundry/cf-k8s-secrets
  - cloudfoundry/korifi
  - cloudfoundry/korifi-ci
```
