# Meta
[meta]: #meta
- Name: CF on KinD
- Start Date: 2025-12-12
- Author(s): @beyhan, @c0d1ngm0nk3y, @loewenstein-sap, @modulo11, @mvach, @nicolasbender, @pbusko
- Status: Draft <!-- Acceptable values: Draft, Approved, On Hold, Superseded -->
- RFC Pull Request: https://github.com/cloudfoundry/community/pull/1389

## Summary

Cloud Foundry local setup with Bosh and cf-deployment is currently cumbersome and has a steep learning curve. This makes it difficult for new users to get started and slows down component development. We propose a simple and fast way to run Cloud Foundry locally, providing a better first-time user experience. Additionally, this enables developers to rapidly prototype, develop, and test new ideas in an inexpensive setup.

## Problem

Setting up Cloud Foundry locally using Bosh and cf-deployment is currently cumbersome which creates a significant barrier to entry.

First-time users encounter significant difficulty when they simply want to try out the `cf push` workflow. Currently, there is no local setup using existing community tools and technologies that can be ready within minutes.

Cloud Foundry component developers face long setup times and complex environments when testing their changes in an integrated environment. This slows down the development process and makes it harder to contribute to the Cloud Foundry ecosystem.

## Proposal

To provide Cloud Foundry on a local machine quickly and easily, we propose installing its components into a KinD cluster ([Kubernetes in Docker](https://kind.sigs.k8s.io/)). This approach leverages KinD's robust community support and widespread adoption within the cloud-native ecosystem, providing a stable and well-maintained foundation for local development.

Most existing Cloud Foundry components require no modifications to run on a Kubernetes cluster. Modifications are only necessary for low-level parts of the container runtime and networking.

Deploying Cloud Foundry to a local Kubernetes cluster will make it possible to quickly and easily validate most Cloud Foundry components in a real environment. This approach also enables cost-effective integration testing in CI pipelines (such as for pull requests). Additionally, it allows users to spin up a Cloud Foundry instance in under five minutes to explore and get an initial impression.
Furthermore, this approach makes it easy for users to try out Cloud Foundry locally, lowering the barrier to entry for developers interested in exploring or experimenting with the platform.

### App Runtime Deployments

As an initial experimental setup for this new local deployment, a new area will be created within App Runtime Deployments WG called `CF Deployment on KinD`. This area will maintain the local deployment, which means it will own the Helm Charts required for CF deployment on KinD, validate that new CF releases work with the local setup executing CATs against it, and create new CF on KinD deployment releases.

## Possible Future Work

If this new local deployment release proves helpful to the CF community and works well, it should graduate into an officially supported local setup and be adopted by the CF community. This means that maintenance of the Helm charts could be adopted by the corresponding working groups, while the App Runtime Deployments WG would own the integration and validation of those charts.

## Long term vision

This RFC is not limited to local development or experimentation scenarios. CF on Kind is intentionally designed to lower the entry barrier for contributors, enable fast feedback cycles, and simplify development and testing workflows.

At the same time, CF on Kind is a foundational step towards a broader CF on Kubernetes vision. If the underlying concepts, architectures, and operational patterns prove to be robust, the long term goal is to evolve these learnings into a community maintained CF on Kubernetes deployment option that can be used in production environments.

In this model, CF on Kind serves as a lightweight and fast feedback environment, while CF on Kubernetes represents the production grade deployment, meeting the required standards for reliability, security, scalability, and operability. Making this distinction explicit ensures that design decisions made in the context of CF on Kind are aligned with a potential future production capable CF on Kubernetes architecture.
