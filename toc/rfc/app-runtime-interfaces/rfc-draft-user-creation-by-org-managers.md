# Meta
[meta]: #meta
- Name: User Creation by Org Managers
- Start Date: 2024-08-13
- Author(s): stephanme
- Status: Draft <!-- Acceptable values: Draft, Approved, On Hold, Superseded -->
- RFC Pull Request: [#946](https://github.com/cloudfoundry/community/pull/946)


## Summary

Allow Org Managers (and CF Admins) to create users in UAA in order to improve the onboarding procedure for larger developer groups into multi-tenant Cloud Foundry foundations. The users are created by the Cloud Controller on behalf of the Org Manager.

## Problem

In order to assign CF roles to users, the users must be available in the UAA. As of today, the user is created in UAA explicitly by an administrator (origin=uaa) or implicitly when the user authenticates the first time via CF UAA for setups where an external identity provider is used (other origins).

This is an issue for customers that want to onboard larger developer groups into multi-tenant Cloud Foundry foundations. All developers would have to log-in into the foundation before CF roles can be assigned - which is impractical. Customers should be able to automate the complete onboarding e.g. using CF CLI or other CF API clients like a CF terraform provider.

## Proposal

The proposal is to grant Org Managers the right to assign CF roles to users which are not yet known in UAA. The users are created in UAA either explicitly via an enhanced `POST /v3/users` call or implicitly when an Org Manager assigns an organization role using `POST /v3/roles`.

The functionality SHALL be gated by a deployment manifest configuration flag and SHALL be disabled by default.

## Required Changes by Component

### Cloud Controller

#### CAPI Release

Introduce a configuration flag `cc.allow_user_creation_by_org_manager` which is disabled by default .

#### POST /v3/users

Enhance the [POST /v3/users](https://v3-apidocs.cloudfoundry.org/version/3.172.0/index.html#create-a-user) endpoint by the parameters `username` and `origin`. `guid` and `username` parameters are exclusive.
The existing user creation by `guid` SHALL NOT be changed.

Required Parameters for Create User by Name
|Name|Type|Description|
|---|---|---|
|username|string|The username as (to be) registered in UAA.|
|origin|string|The origin / identity provider for the user. `origin=uaa` is not allowed as it requires a password. |


Permitted roles for Create User by Name
- Admin
- OrgManager (if configuration flag `cc.allow_user_creation_by_org_manager` is enabled)

CAPI will call the [POST /Users](https://docs.cloudfoundry.org/api/uaa/version/77.14.0/index.html#create-2) endpoint of the UAA using a CAPI owned UAA client with scope `scim.write` or `uaa.admin` for creating the user if it doesn't exist yet in UAA. The user is then registered in the Cloud Controller database under the user guid returned by UAA.

#### POST /v3/roles

If a role is created by user name and origin (requires feature flag `set_roles_by_username` to be enabled) and the configuration flag `cc.allow_user_creation_by_org_manager` is enabled, the user with the provided name and origin SHALL be created in CF UAA if the users doesn't exist yet in UAA.
In other words: Role assignment shall succeed even if the user is still unknown to CF UAA. The user is created implicitly similar to `POST /v3/users` by username/origin described above.

### CLI

`cf create-user USERNAME [--origin ORIGIN]` (user creation without specifying a password) SHOULD use the CF API `POST /v3/users` instead of calling CF UAA directly so that Org Managers can create users if configuration flag `cc.allow_user_creation_by_org_manager` is enabled.

### UAA

No changes required.
