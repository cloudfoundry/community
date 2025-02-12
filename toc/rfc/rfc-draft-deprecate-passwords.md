# Meta
[meta]: #meta
- Name: Deprecate Passwords, Replace it with JWT Bearer Tokens
- Start Date: 2025-02-12
- Author(s): strehle
- Status: Draft 
- RFC Pull Request: (fill in with PR link after you submit it)


## Summary

Why: password grant should be deprecated, because it is not part of newer OAuth or OIDC standards, e.g. https://oauth.net/2.1/
There is a RFC https://datatracker.ietf.org/doc/html/rfc9700#section-2.4 which states
The resource owner password credentials grant [[RFC6749](https://datatracker.ietf.org/doc/html/rfc6749)] MUST NOT be used.

There is an alternative for login which is JWT bearer. Later maybe other token based grant type, but currently it is JWT bearer which can repace it.


An abstract, tl;dr or executive summary of your RFC.

## Problem

Problem is visible if you run "cf login -h" or "cf auth -h"

      WARNING:
         Providing your password as a command line option is highly discouraged
         Your password may be visible to others and may be recorded in your shell history
         Consider using the CF_PASSWORD environment variable instead

So we warn the users that they should be carefully entering their passwords.
For user interactive login or principal propagation we support the passcode login a way to omit passwords in cf login. For pure technical usages there is token based authentication with private_key_jwt (or later mtls) in client_credentials flows.

However, there are mixed scenarios, where technical scenarios need a user. Github action is a good example but there could be other scenarios, typically business scenarios, where a user principal propagation should be supported, but there is no user interactive login.

JWT bearer and generic token exchange can solve the problem, but in CF is it not easy to adopt JWT bearer and for the generic token exchange we have no support yet, e.g. https://www.rfc-editor.org/rfc/rfc8693.html .

The RFC should make you from TOC aware, that we should start with changes in other areas. 

## Proposal

Created https://github.com/cloudfoundry/uaa/issues/3285 in UAA area, but the change is related to 
https://github.com/cloudfoundry/cf-deployment/pull/1232
and 
https://github.com/cloudfoundry/cli/pull/3397

We SHOULD add JWT Bearer, then we SHOULD deprecate the password grant and announce it. After some time we MUST forbid to forward a password within CF tools , e.g. "cf auth".


