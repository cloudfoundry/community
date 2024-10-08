# Meta
[meta]: #meta
- Name: Bindable Secrets
- Start Date: 2024-10-08
- Author(s): @tcdowney @gerg
- Status: Draft
- RFC Pull Request: (fill in with PR link after you submit it)

## Summary

This RFC proposes a new resource to the V3 Cloud Foundry APIs called the `Secret` that is similar in design and purpose to the Kubernetes [Secret resource](https://kubernetes.io/docs/concepts/configuration/secret/). Cloud Foundry Secrets will support arbitrary data that is stored in [CredHub](https://docs.cloudfoundry.org/credhub/) and made available to apps via `tmpfs` mounted files using the same mechanism as [RFC 0030 - Add Support for File based Service Binding Information](https://github.com/cloudfoundry/community/blob/main/toc/rfc/rfc-0030-add-support-for-file-based-service-binding.md).

## Problem

The Cloud Foundry platform currently prefers for applications to accept configuration through environment variables. Other application platforms, such as Kubernetes, support other mechanisms for providing configuration at runtime [as volume-mounted files](https://kubernetes.io/docs/concepts/configuration/secret/#using-secrets-as-files-from-a-pod). Many modern applications are adopting this file-based configuration approach since these files are not subject to the size limits of environment variables and can be updated without having to recreate the container. This RFC proposes introducing a similar mechanism in order to support these sorts of applications on Cloud Foundry -- without requiring code changes.

### Why can't apps just use user-provided service instances (UPSIs) and service binding files?
Some apps may have config they want as files provided at runtime that don't naturally fit into the service binding model. For example, if an app relies on a config file that needs to live at a certain path, it may not be able to be updated to find it at another path such as `$SERVICE_BINDING_ROOT`. This is especially the case for commercial off-the-shelf software (COTS).

## Proposal

We introduce two new resources to the V3 Cloud Foundry APIs: the `Secret` and the `Secret Binding` along with their associated CRUD API endpoints.

### Why a separate `Secret` resource? Why not just store them under apps like environment variables?
Several reasons here.

1. Secrets may be larger than environment variables. Modeling them separately lets us naturally keep them in a separate database table and even use separate services, like CredHub, to store their contents.
2. `Secrets` may be shared across multiple apps. For example, if an "app" may actually be several actual Cloud Foundry apps that need to share certain configuration, certificates, or other credentials. By scoping the `Secret` at the `Space` level we can easily support this. Or an app may simply be using the blue-green deployment pattern and be several CF apps for that reason.

### `Secret` and `Secret Binding` Resources
The `Secret` will be a `Space`-scoped resource (similar to a `Route` or a `Service Instance`) that can be bound to one or more `Apps` using a `Secret Binding`.

#### Example `Secret` Object

```json
{
  "guid": "4f00b75b-3455-48f1-ba4a-f3b82ebad943",
  "created_at": "2020-03-10T15:49:29Z",
  "updated_at": "2020-03-10T15:49:29Z",
  "name": "my-secret",
  "type": "json",
  "credhub_credential_id": "b6380fe8-1636-441b-a81f-43d21e3ac5c7",
  "relationships": {
    "space": {
      "data": {
        "guid": "5a84d315-9513-4d74-95e5-f6a5501eeef7"
      }
    }
  },
  "metadata": {
    "labels": {},
    "annotations": {}
  },
  "links": {
    "self": {
      "href": "https://api.example.org/v3/service_instances/c89b3280-fe8d-4aa0-a42e-44465bb1c61c"
    },
    "space": {
      "href": "https://api.example.org/v3/spaces/5a84d315-9513-4d74-95e5-f6a5501eeef7"
    },
    "secret_bindings": {
      "href": "https://api.example.org/v3/secret_bindings?secret_guids=4f00b75b-3455-48f1-ba4a-f3b82ebad943"
    },
    "value": {
      "href": "https://api.example.org/v3/secrets/4f00b75b-3455-48f1-ba4a-f3b82ebad943/value"
    }
  }
}
```

The `type` parameter corresponds with a [CredHub credential type](https://docs.cloudfoundry.org/credhub/credential-types.html). To start we will focus on supporting the `value` and `json` credential types, but can expand to others like the `certificate` type as these may pave the way to future enhancements and use cases.

#### Example `Secret Binding` Object

```json
{
  "guid": "dde5ad2a-d8f4-44dc-a56f-0452d744f1c3",
  "created_at": "2015-11-13T17:02:56Z",
  "updated_at": "2016-06-08T16:41:26Z",
  "name": "secret-binding-name",
  "mount_path": "/etc/my-conf/",
  "metadata": {
    "annotations": {},
    "labels": {}
  },
  "relationships": {
    "app": {
      "data": {
        "guid": "74f7c078-0934-470f-9883-4fddss5b8f13"
      }
    },
    "secret": {
      "data": {
        "guid": "4f00b75b-3455-48f1-ba4a-f3b82ebad943"
      }
    }
  },
  "links": {
    "self": {
      "href": "https://api.example.org/v3/service_credential_bindings/dde5ad2a-d8f4-44dc-a56f-0452d744f1c3"
    },
    "secret": {
      "href": "https://api.example.org/v3/secrets/4f00b75b-3455-48f1-ba4a-f3b82ebad943"
    },
    "app": {
      "href": "https://api.example.org/v3/apps/74f7c078-0934-470f-9883-4fddss5b8f13"
    }
  }
}
```

The `mount_path` parameter defines the `tmpfs` directory that will contain files for the `Secret`'s content. If a credential has subkeys (such as a [`json` type credential](https://docs.cloudfoundry.org/api/credhub/version/main/#_find_a_credential_by_id_type_json) or [`certificate` type](https://docs.cloudfoundry.org/api/credhub/version/main/#_find_a_credential_by_id_type_certificate)) then files will be made for each key.

So for a `json` type credential whose value is:

```json
"value": {
  "application.yml" : "---\napplication:\n ...",
  "secret.txt": "my-secret"
}
```

We would have a file called `application.yml` created under `/etc/my-conf`.

For a `value` type credential the file would simply take the same name as the `Secret Binding`.

### Creating a `Secret`

To create a `Secret` we will introduce a new CLI command: `cf create-secret`.

```console
cf create-secret SECRET_NAME SECRET_TYPE -p <CREDENTIALS_INLINE_OR_FILE>
```

If `SECRET_TYPE` is `value` then contents of `-p` will not be parsed. If `SECRET_TYPE` is `json`, `certificate`, or some other CredHub credential type then the contents of `-p` MUST be valid JSON and may be parsed.

This command will ultimately create a `POST` request to `/v3/secrets` that looks like this:

```console
curl "https://api.example.org/v3/secrets" \
  -X POST \
  -H "Authorization: bearer [token]" \
  -H "Content-type: application/json" \
  -d '{
    "type": "json",
    "name": "my-app-secrets",
    "value": {
      "application.yml" : "---\napplication:\n ...",
      "secret.txt": "my-secret"
    }
    "metadata": {
      "annotations": {},
      "labels": {}
    },
    "relationships": {
      "space": {
        "data": {
          "guid": "7304bc3c-7010-11ea-8840-48bf6bec2d78"
        }
      }
    }
  }'
```

### Reading a `Secret` and its value
Users that have permission to view Environment Variables for an App will be able to view `Secret` values within a `Space`. We will introduce a separate endpoint for retrieving these (similar to how app environment variables and service instance credentials are retrieved): `GET /v3/secrets/:guid/value`

```console
curl "https://api.example.org/v3/secrets/[guid]/value" \
  -X GET \
  -H "Authorization: bearer [token]"
  
"value" : {
  "some-json-key" : "some-json-value"
}
```

To support this Cloud Controller will need to have both read and write permissions for the `Secret`'s corresponding credential in CredHub.

### Creating a `Secret Binding`
We will introduce a new CLI command to allow users to create `Secret Bindings`: `cf bind-secret`. This will create a `POST` request to `/v3/secret_bindings`.

```console
cf bind-secret APP_NAME SECRET_NAME BINDING_NAME
```

### CLI changes
Work will need to be done to implement `cf create-secret`, `cf bind-secret`, and the associated update/delete commands in the CLI.

### Cloud Controller changes
New database tables will need to be created to store `Secrets` and `Secret Bindings` and CRUD APIs will need to be created for these resources. We will also need an API to support viewing a `Secret`'s value.

### BBS changes
BBS was recently updated to support `ServiceBindingFiles` as part of RFC 0030. A `Secret`'s value may result in one or more files being created in the `tmpfs` mounted directory defined by the `MountPath` parameter.

```
action := &models.RunAction{
  Path: "/path/to/executable",
  Args: []string{"some", "args to", "pass in"},
  Dir: "/path/to/working/directory",
  User: "username",
  EnvironmentVariables: []*models.EnvironmentVariable{
    {
      Name: "ENVNAME",
      Value: "ENVVALUE",
    },
  },
 ServiceBindingFiles: []*models.Files{
    {
      Name: "/etc/cf-instance-binding",
      Value: "VALUE",
    },
  },
  Secrets: []*models.Secret{
    {
      Name: "SECRETNAME",
      MountPath: "/etc/conf/",
      Value: "credhub-credential-id:<CREDHUB_CREDENTIAL_ID>",
    },
  },
  ResourceLimits: &models.ResourceLimits{
    Nofile: 1000,
  },
  LogSource: "some-log-source",
  SuppressLogOutput: false,
}
```

### Launcher changes?
The launcher (or something else) will need to be updated to retrieve credentials from CredHub for `Secret Bindings`. It currently already does this for CredHub references contained within `VCAP_SERVICES` using the app container's instance identity credentials. Is there something other than the launcher that should have this responsibility?

### Other Considerations

#### Not using CredHub
Although Cloud Foundry comes with CredHub by default, it is not a required component. We could support `value` and `json` type `Secrets` directly in Cloud Controller as a fallback.

#### CredHub Maximum Secret size
Kubernetes Secrets and ConfigMaps have a [maximum size of 1 MiB](https://kubernetes.io/docs/concepts/configuration/configmap/#motivation). The [maximum size of a CredHub credential is 64Kb](https://docs.cloudfoundry.org/credhub/credential-types.html). If we plan on using CredHub we will need to limit our Secrets to 64KB or get CredHub to increase the limit.

#### (Future) Rotatable Secrets
If we make the `*Files` parameters on the `DesiredLRP` mutable fields in BBS then theoretically Cloud Controller could update the `DesiredLRP` when `Secret` contents change and this could be propagated to the container without requiring container recreation.

For certain CredHub credential types such as `certificate` or `password` we may even be able to expose CredHub credential rotation/[regeneration](https://docs.cloudfoundry.org/api/credhub/version/main/#_regenerate_credentials_endpoint) functionality.