# Meta
[meta]: #meta
- Name: Deprecate Passwords, Replace it with JWT Bearer Tokens
- Start Date: 2025-02-12
- Author(s): strehle
- Status: Draft 
- RFC Pull Request: https://github.com/cloudfoundry/community/pull/1085


## Summary

The cf login / cf auth uses the [password grant (RFC6749)](https://datatracker.ietf.org/doc/html/rfc6749#section-1.3.3) towards UAA. This grant type is deprecated in newer OAuth2 or OIDC standards, e.g. https://oauth.net/2.1/
There is now (Begin of 2025) a RFC https://datatracker.ietf.org/doc/html/rfc9700#section-2.4 which states


      The resource owner password credentials grant [RFC6749](https://datatracker.ietf.org/doc/html/rfc6749) MUST NOT be used.


There are alternatives, e.g. [JWT bearer for users grants](https://datatracker.ietf.org/doc/html/rfc7523#section-2.1) or Token Exchange using [RFC 8693](https://www.rfc-editor.org/rfc/rfc8693.html), but cf client needs to adopt these and CF UAA needs to support them.
Currenlty CF UAA supports JWT bearer, therefore we should start with this usage.

## Problem

Problem is visible if you run "cf login -h" or "cf auth -h"

      WARNING:
         Providing your password as a command line option is highly discouraged
         Your password may be visible to others and may be recorded in your shell history
         Consider using the CF_PASSWORD environment variable instead

So we warn the users that they should be carefully entering their passwords.
For user interactive login or principal propagation we support the passcode login (option --sso), a way to omit passwords in cf login. 

However, non-interactive logins still need a password. Github action is a good example but there could be other scenarios, typically business scenarios, where a user principal propagation should be supported within a script or embedded process. 
Running github action means, in a PR you can receive an id_token from Github in order to perform principal propagation, but with standard CF client tools you cannot use this token to authentication to CF in order to perform a cf push.
Currently you add a secret in Github action to pass it via environment to cf.

JWT bearer (either for user or client grants) and generic token exchange can solve the problem, but in CF is it not easy to adopt JWT bearer and for the generic token exchange we have no support yet, e.g. https://www.rfc-editor.org/rfc/rfc8693.html .

The RFC should make you from TOC aware, that we should start with changes in other areas. 

## Proposal

#### CF Deployment
The manifest for deploying the Cloud Foundry Application Runtime. This defines the default behaviour. Here we have currently the cf client with
password grant type. We SHOULD add JWT Bearer as default in CF landscape to cf client, see https://github.com/cloudfoundry/cf-deployment/pull/1232.

#### CF CLI 
The Cloud Foundry CLI perform the login. There are 2 commands, cf login and cf auth.
We should change cf login and/or cf auth in order to support the token based login, see https://github.com/cloudfoundry/cli/pull/3397.
With this you can do both the password and token login to CF.

#### UAA 
The User Account and Authentication system in CF receives request from cf cli. UAA support the JWT bearer since some years, so no change needed.
Created https://github.com/cloudfoundry/uaa/issues/3285 in UAA area to track changes from other components.   

## Extension
In more complex landscapes - and in SAP we have these landscapes - we SHOULD add the forward of JWT bearer from UAA towards corporate IdPs. 
There can be situations, where customers run their own IDP, but connect CF UAA only to this IdP. If customers authentication, they authenticate against their corp.IdP. 
This is done with password grant and therefore it should be possible with JWT bearer. The use case is, that a customer should control if she/he trusts the token, e.g. github action token.
These steps allow to have same behaviour for token based logins then we support currently with passwords.

## Timeline

### Phase 1
Add JWT bearer grant in CF Deployment in [standard cf client](https://github.com/cloudfoundry/cf-deployment/pull/1232) and release new [cf-cli version](https://github.com/cloudfoundry/cli/pull/3397).
In UAA issue [#3286](https://github.com/cloudfoundry/uaa/issues/3286) should be solved so that CF administrators can create separate oauth clients in their CF landscape in order to test and verify the new login.
Corporate CF usages with a central OIDC IdP should be able to forward token request. UAA needs to solve issue [#3289](https://github.com/cloudfoundry/uaa/issues/3289)

### Phase 2
Add deprecation note in CF docs for UAA and cli to announce the end of live. UAA issue [#3290](https://github.com/cloudfoundry/uaa/issues/3290).
Allow this parallel usage around 2 years.

### Phase 3
Remove password grant from CF Deployment and remove support in cf cli. Dependening on preasure support both usage for an extended usage.

### Phase 4
Remove password grant from UAA. After that there is no way back, because then cf cli cannot use it anymore. An exception should be the passcode login.
This login means a password grant towards UAA but the passcode is sent and in UAA we see the difference and SHOULD allow it, e.g. https://docs.cloudfoundry.org/api/uaa/version/77.26.0/index.html#one-time-passcode.
