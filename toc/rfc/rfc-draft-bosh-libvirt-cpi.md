# Meta
[meta]: #meta
- Name: Golang-based libvirt CPI for BOSH with Multi-Runtime Support
- Start Date: 2025-06-30
- Author(s): ZPascal
- Status: Draft
- RFC Pull Request: [community#1227](https://github.com/cloudfoundry/community/pull/1227)

## Summary

This proposal introduces a new **Cloud Provider Interface (CPI)** for **BOSH**, implemented in **Go** and based on **libvirt**. It is intended as a modern, maintainable, and extensible alternative to the current **VirtualBox CPI**, supporting multiple virtualization backends, including **VirtualBox**, **QEMU/KVM**, and **container runtimes (e.g., containerd)**. This libvirt-based CPI will serve as a **centralized and runtime-agnostic integration layer** for local or development BOSH deployments, with the initial milestone being to **replace the existing VBox CPI**.

## Problem

The existing VirtualBox CPI:
- Is minimally maintained and tied to a single backend (VBox).
- Has limited extensibility and runtime support.
- Is written in Ruby, with a legacy codebase that is harder to modernize.

Meanwhile, [libvirt](https://libvirt.org/) offers:
- A standard API for interacting with various virtualization technologies.
- Broad backend support, including **QEMU/KVM**, **VirtualBox**, **LXC**, and **containerd** via libvirt plugins.
- Better resource isolation and VM/network emulation capabilities.
- Go client libraries (e.g., [libvirt/libvirt-go](https://gitlab.com/libvirt/libvirt-go)) well-aligned with modern infrastructure tools.

Benefits for the community:
- **Unified, reusable codebase** for local CPI development.
- **Cost reduction** by avoiding duplicated maintenance of multiple special-purpose CPIs.
- **Improved security and performance** through direct integration with native virtualization layers (e.g., KVM).
- **Better testability** and maintainability by adopting Go instead of Ruby.

## Proposal

### Overview

1. **Developing a new Golang-based CPI** using libvirt-go to interface with local hypervisors or containers via libvirt.
2. Supporting multiple backends (initially: VirtualBox, QEMU/KVM, containerd).
3. Replacing the **VirtualBox CPI** as the first deliverable and reference implementation.
4. Maintaining compatibility with the standard BOSH CPI contract interfaces (e.g., `create_vm`, `delete_vm`, `attach_disk`, etc.).
5. Enabling backend configuration via BOSH runtime configs, selectable per environment.
6. Publishing the CPI as an open-source component under the Cloud Foundry or BOSH community GitHub organization.