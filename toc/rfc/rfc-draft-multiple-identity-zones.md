# Meta
[meta]: #meta
- Name: User Account Management in Cloud Foundry with Multiple Identity Zones
- Start Date: 2023-08-04
- Authors: @FloThinksPi, @klaus-sap, @philippthun
- Status: Draft
- RFC Pull Request: (fill in with PR link after you submit it)

## Summary

This RFC proposes enhancing Cloud Foundry (CF) to support users from multiple identity zones within the CF User Account and Authentication (UAA) system. The objectives are to enable efficient user management, facilitate data isolation and allow customized security measures.

## Problem

CF operators are currently limited to the default identity zone within the UAA system for user account management. However, the need to store user accounts in different zones may arise from two distinct operational requirements:
1. CF installations servicing multiple customers or tenants (e.g. public PAAS) must ensure absolute isolation of user accounts. Each customer or tenant must have their user accounts securely stored in separate identity zones to prevent unauthorized access to sensitive data. It is crucial that users from one customer cannot view, modify, or access the user accounts of other customers.
1. Even in cases where CF is deployed for a single customer or organization, there may be a need to employ multiple identity zones. This could arise when customers wish to segregate user accounts based on roles, affiliations, or subsidiaries. By creating distinct zones, organizations can enforce specific security measures tailored to different user groups, such as implementing Multi-Factor Authentication (MFA) for certain privileged users.

## Proposal

To address the operational and security requirements outlined above, this RFC proposes enhancing CF to support users from multiple identity zones within the CF UAA system. This requires changes to various components as outlined in this section.

### User Account and Authentication

1. Currently, web-based applications like service dashboards or other client applications like "cf ssh" run the authorization code flow against the default identity zone of UAA, which is advertised by the foundation’s api root (`/`) and info endpoints. This flow shall be extended to work with user accounts from other identity zones, too.
   1. The login page of UAA shall allow switching from the default identity zone (empty subdomain) to another identity zone/subdomain. UAA may store the favorite zone/subdomain in a cookie.
   1. The `/oauth/authorize` endpoint in the default identity zone shall be able to access security sessions from other identity zones and return authorization codes belonging to other identity zones.
   1. The `/oauth/token` endpoint in the default identity zone shall accept authorization codes belonging to other identity zones and return access tokens from the right zone, i.e. tokens with claim `zid` set to the zone ID of the user who has logged in.
   1. The `/check_token` endpoint in the default identity zone should be able to verify tokens from all identity zones, i.e. the claim `zid` must be considered to choose the right identity zone for token verification.
1. With these changes it should be sufficient to create clients with the authorized grant type `authorization_code` in the default zone only. Along with these clients, the OAuth issuer and verification keys of all zones should be taken from the default zone.
1. In addition, it must not be possible for customers to break out from their identity zone. Customers must not be able to assign authorizations to users, which grant access to other identity zones. In the same way it must not be possible to assign administration authorizations like `cloud_controller.admin` to users from a non-default identity zone. Only predefined scopes should be assignable by user administrators in non-default zones.
1. With authorization `uaa.admin` or wildcard scopes across all zones (e.g. `zones.*.scim.read`) it should be possible to list all users from all zones with one single API call.

### Cloud Controller

1. The Cloud Controller (CC) shall authenticate users with tokens from non-default identity zones. The OAuth issuer and verification keys shall be taken from the default zone.
1. User lookups must be performed within the identity zone of the authenticated user. SCIM queries shall be done with the `X-Identity-Zone-Id` header set to the `zid` of the user token. When a user interacts with the CC and requests information about other users who are part of their organization, the following behavior shall be implemented:
   1. For users who reside in the same zone as the authenticated user, the CC shall display their usernames.
   1. For users who belong to a different zone from the authenticated user, the CC must not display their usernames, but only the user GUIDs.
1. Users with a CC admin scope (e.g. `cloud_controller.admin`) can lookup users across all identity zones, i.e. the CC shall display the usernames for all users.

### Command Line Interface

1. The commands "cf login" and "cf auth" must be enhanced by introducing an optional parameter to specify the desired identity zone for authentication. The new parameter should allow users to provide the subdomain of the target zone, not the zone ID. If not provided, the default identity zone will be used for login/authentication.

## Backward Compatibility and Migration Considerations

Given the nature of this feature enhancement, it is designed to be an opt-in, thus preserving backward compatibility by default. This means existing configurations will not be impacted unless operators actively choose to enable multiple identity zones.

However, once multiple identity zones are activated, it's inevitable that some user accounts will require migration to suitable zones based on the organization's specific operational needs. The process of such migration, including its specific operational steps, is beyond the scope of this document.

