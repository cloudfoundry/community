# Meta
[meta]: #meta
- Name: Service Credential Binding Rotation for Applications
- Start Date: 2025-06-10
- Authors: @beyhan, @stephanme
- Status: Draft <!-- Acceptable values: Draft, Approved, On Hold, Superseded -->
- RFC Pull Request: (fill in with PR link after you submit it)

## Summary

Cloud Controller does not support creating a second binding between an application and a service instance, which prevents seamless rotation of credential bindings.  As a result, the only current method to rotate service credential bindings is through blue-green deployments, a process that many developers are hesitant to use solely for credential rotation. That is why, this RFC proposes to add support for multiple service credential bindings per service instance and application. To simplify the rotation process the RFC suggests a new CF API endpoint and CF CLI extensions.

## Problem

Cloud Controller does not support creation of a second binding for a service instance and application which would enable seamless binding credential rotation. Attempting to create a second binding using the CF CLI results in the following error:

```
cf bind-service myApp myService --binding-name second-binding
Binding service instance myService to app myApp in org myOrg / space mySpace as ...
App myApp is already bound to service instance myService.
OK
```
This limitation is not due to the CF CLI but rather a restriction in the CC API, which prevents multiple bindings for the same application. Attempting to create the binding directly via the CF API results in a similar error:

```
cf curl -X POST "/v3/service_credential_bindings" -d '{
    "name": "test-second-binding",
    "relationships": {
        "app": {
            "data": {
                "guid": "<myApp-guid>"
            }
        },
        "service_instance": {
            "data": {
                "guid": "<mySerivce-guid>"
            }
        }
    },
    "type": "app"
}'

{"errors":[{"detail":"The app is already bound to the service instance","title":"CF-UnprocessableEntity","code":10008}]}
```
As a result, the only way to rotate service credential bindings currently is by performing blue-green deployments. However, many CF application developers are reluctant to push a new version of their application solely for the purpose of credential rotation.

## Proposal

The CC should allow multiple service credential bindings per service instance and application. Only the newest one should be visible in the application VCAP_SERVICES env var (or file-based service binding information) so that existing applications don’t need to change.

### CF Cloud Controller

The CC should introduce a new CF API `POST /v3/service_credential_bindings/:guid/actions/recreate` which can be used to recreate a service binding and will require following optional parameter:
| Name       | Type   | Description                                      |
|------------|--------|--------------------------------------------------|
| parameters | object | A JSON object that is passed to the service broker|


The result of calling this API is a new service binding with a new guid for the same application and service instance. The initial implementation with the current support of [OSBAPI 2.15](https://github.com/openservicebrokerapi/servicebroker/blob/v2.15/spec.md) in CC can just create a new service binding and with [OSBAPI 2.17](https://github.com/openservicebrokerapi/servicebroker/blob/v2.17/spec.md) adoption in CC it could use the binding rotation support. `POST /v3/service_credential_bindings/:guid/actions/recreate` is just a shortcut for `POST /v3/service_credential_bindings` which would require to specify the app and service instance references which could be used from the specified service binding  guid in the URL path. Following requirements should applied to this API:
- It should support only managed service instances and shall fail for user-provided service instances
- It should also fail for service credential bindings from type key
- Service binding credentials names remain unique per app but multiple credential bindings to the same service instance can share the same name

The API `GET /v3/service_credential_bindings` should be extended to return all service credential bindings of an application including the recreated ones.
When creating the service credential binding information like VCAP_SERVICES or file-based one the CC must select the newest one only. This must be based on the `created_at` field from the credential binding.  An application restart or restage as today will be required to activate the new binding.

### CF CLI

The CF CLI should introduce a new flag called `--recreate` for the `bind-service` command. Example:
```
cf bind-service myApp myService --recreate
```
When the flag `--recreate` is provided the CLI should use the new `POST /v3/service_credential_bindings/:guid/actions/recreate` to recreate the service credential binding. In case there is no service instance binding yet this will fail.

The cleanup of old inactive service binding should be supported by a new CF CLI command:
```
cf cleanup-outdated-service-bindings myApp [myService]
```
The CLI will use the  CF API `GET /v3/service_credential_bindings?app_guids=:guid ` to list the service instance bindings for an application and should delete all old bindings based on the creation date leaving the newest service binding. If no service instance name is provided, the CLI should delete the old bindings of all services currently bound to the application. A full-service binding recreation flow with the CF CLI could look like:
```
cf bind-service myApp myService -c {<parameters>} --recreate
cf bind-service myApp myService2 -c {<parameters>} --recreate
cf restage myApp --strategy rolling
cf cleanup-outdated-service-bindings myApp
```
## Possible Future Work

### CC adoption of OSBAPI 2.17

The CC could use the service binding rotation functionality introduced with the OSBAPI 2.17 to improve the implementation of the `POST /v3/service_credential_bindings/:guid/actions/recreate` API endpoint.

### Integrate Service Binding Recreation into Rolling Deployment

Here an example how this could look with the CF CLI:
```
Cf restage myApp –strategy rolling-with-binding-rotation
```
The result should be that all bindings of the application are recreated after a successful restage.

### Binding Recreation with no App Restart

With the adoption of file-based service bindings in Diego it is technically possible to update a service instance binding for a running application container at runtime without requiring an application restart. Things to consider:
- This will require an extension of the CC and Diego API (https://github.com/cloudfoundry/bbs/blob/main/docs/053-actions.md )
- CF application will need support for service binding credential updates during runtime
- Some service bindings requiring restage can’t be supported
- CC will need a trigger to update the service binding information for the corresponding LRP(s)
