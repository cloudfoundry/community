# Agentic Runtime: Working Group Charter

## Mission

Define and advance a shared vision for running AI agents and LLM-powered workloads as first-class citizens on Cloud Foundry — deployed, managed, secured, scaled, and observed using the same platform-native primitives that developers and operators rely on today.

## Goals

* Establish lifecycle and runtime models for agents running alongside traditional apps on CF
* Define standards for agent identity, authentication, and authorization within CF spaces
* Drive platform extensions for autonomy, orchestration, and inter-agent communication on CF
* Carry CF's core values of security, operability, portability, and developer experience into agentic workloads

## Scope

* Define and evolve architectural, security, and operational models for CF-native agent workloads
* Evaluate technologies in the agentic ecosystem for relevance to CF's runtime model
* Produce design documents, RFCs, and implementations for agentic runtime primitives in CF
* Collaborate with other CF working groups to integrate agent capabilities into the CF platform

## Non-Goals

* General-purpose AI/ML infrastructure not tied to CF's runtime model
* Agent model training, fine-tuning, or inference serving infrastructure
* Agentic runtime work targeting Kubernetes-native approaches outside CF's deployment model
* Exposing GPUs to application containers
* Running LLMs directly on Diego — LLM inference should be deployed via BOSH and exposed to applications through the CF service broker API

## Roles & Technical Assets

Research notes, design documents, and RFCs for agentic workloads on Cloud Foundry.

```yaml
name: Agentic Runtime

execution_leads:
- name: Beyhan Veli
  github: beyhan

technical_leads:
- name: Wayne E. Seguin
  github: wayneeseguin
- name: Ruben Koster
  github: rkoster
- name: Ioannis Tsouvalas
  github: itsouvalas

areas:
- name: Agentic Runtime
  approvers:
  - name: Benjamin Guttmann
    github: benjaminguttmann-avtq
  - name: Aram Price
    github: aramprice
  - name: Vladimir Savchenko
    github: vlast3k
  - name: Arsalan Khan
    github: asalan316
  reviewers:
  - name: Tsvetelina Marinova
    github: ivanovac
  - name: Ned Petrov
    github: neddp
  - name: Ivaylo Ivanov
    github: ivaylogi98
  - name: Saumya Dudeja
    github: dudejas
  - name: Nicolas Herbst
    github: nmaurer23
  repositories:
  - cloudfoundry/agentic-runtime-notes
```
