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

#### POST /v3/service_credential_bindings

Shall allow the creation of multiple service credential bindings for the same app and service instance under the following conditions:
- service credential bindings are of type `app`
  - bindings of type `key` don't have a reference to an application
  - multiple service keys for a service instance are already supported
- service credential binding name is not changed
  - multiple bindings to the same service instance are intended for credential rotation
  - VCAP_SERVICES structure doesn't allow multiple bindings to the same service instance so different binding names don't make sense

The number of multiple service credential bindings for the same app and service instance should be limited. The limit prevents a DoS threat and eventually reminds users to clean up old, likely outdated bindings.

#### GET /v3/service_credential_bindings

The API `GET /v3/service_credential_bindings` will return all service credential bindings of an application including multiple bindings to the same service instance.

### Mapping of service credential bindings into application containers

When creating the service credential binding information like VCAP_SERVICES or file-based one the CC must select the newest one per service instance only that is in state `succeeded`. This must be based on the `created_at` and `last_operation.state` fields from the credential binding.

An application restart or restage as today will be required to activate the new binding.

### CF CLI

Users can create multiple service credential bindings by invoking the `bind-service` command with a `--strategy multiple` option. The default strategy `single` ensures backward compatibility of the `cf bind-service` command.

Example:
```
cf bind-service myApp myService  # create initial binding
cf bind-service myApp myService  # succeeds with message "App myApp is already bound to service instance myService." No secondary binding is added.
cf bind-service myApp myService --strategy single  # same as previous command, 'single' is the default strategy 

cf bind-service myApp myService --strategy multiple  # adds a secondary binding to the same service instance
cf bind-service myApp myService --strategy multiple  # adds a third binding to the same service instance
```

The exact parameter naming can be finalized at implementation time. A `strategy` parameter allows future extension, e.g. for OSBAPI 2.17 support mention in section "Possible Future Work".

`cf unbind-service myApp myService` shall delete all existing service credential bindings for `myApp` to `myService`.
An additional parameter `cf unbind-service --guid <guid>` should support the deletion of a single service credential binding.

`cf service myService` should list all bindings to apps including their `guid` and `created_at` timestamp. This information is helpful to understand which binding will be mapped into the application container.

The cleanup of old service credential bindings should be supported by a new CF CLI command:
```
cf cleanup-outdated-service-bindings myApp [--service-instance myService] [--keep-last 1]
```
The CLI will use the  CF API `GET /v3/service_credential_bindings?app_guids=:guid` to list the service instance bindings for an application and should delete all old bindings based on the creation date leaving the newest service bindings. With the `keep-last` parameter, users can keep the x newest bindings per app and service instance. If no service instance name is provided, the CLI should delete the old bindings of all services currently bound to the application.
It is in the responsibility of the user to invoke `cf cleanup-outdated-service-bindings myApp` only after a successfully restage/restart of the app, i.e. when old service credential bindings are not used anymore by any app container. 

A full service binding rotation flow with the CF CLI could look like:
```
cf bind-service myApp myService -c {<parameters>} --strategy multiple
cf bind-service myApp myService2 -c {<parameters>} --strategy multiple
cf restage myApp --strategy rolling
cf cleanup-outdated-service-bindings myApp
```

## Possible Future Work

### CC adoption of OSBAPI 2.17

The CC could use the service binding rotation functionality introduced with the OSBAPI 2.17 and introduce a dedicated API endpoint for rotation, e.g. `POST /v3/service_credential_bindings/:guid/actions/duplicate` (good naming to be found).

### Integrate Service Binding Recreation into Rolling Deployment

Here an example how this could look with the CF CLI:
```
cf restage myApp –strategy rolling-with-binding-rotation
```
The result should be that all bindings of the application are recreated after a successful restage.

### Binding Recreation with no App Restart

With the adoption of file-based service bindings in Diego it is technically possible to update a service instance binding for a running application container at runtime without requiring an application restart. Things to consider:
- This will require an extension of the CC and Diego API (https://github.com/cloudfoundry/bbs/blob/main/docs/053-actions.md )
- CF application will need support for service binding credential updates during runtime
- Some service bindings requiring restage can’t be supported
- CC will need a trigger to update the service binding information for the corresponding LRP(s)
