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
- name: Giuseppe Capizzi
  github: gcapizzi
technical_leads:
- name: Giuseppe Capizzi
  github: gcapizzi
- name: George
  github: georgethebeatle
areas:
- name: CF on k8s
  approvers:
  - name: Andrew Wittrock
    github: Birdrock
  - name: Andrew Costa
    github: acosta11
  - name: Ashwin Krishna
    github: akrishna90
  - name: Danail Branekov
    github: danail-branekov
  - name: Dave Walter
    github: davewalter
  - name: Akira Wong
    github: gnovv
  - name: Kieron Browne
    github: kieron-dev
  - name: Matt Royal
    github: matt-royal
  - name: Mario Nitchev
    github: mnitchev
  - name: Tim Downey
    github: tcdowney
  repositories:
  - cloudfoundry/cf-k8s-controllers
  - cloudfoundry-incubator/eirini-controller
```
