# Meta
[meta]: #meta
- Name: Bindable Secrets
- Start Date: 2024-10-08
- Author(s): @tcdowney @gerg
- Status: Draft
- RFC Pull Request: (fill in with PR link after you submit it)

## Summary

**tl;dr** Kubernetes-style Secrets for Cloud Foundry

This RFC proposes adding a `secret` resource to the V3 Cloud Foundry API, similar in design and purpose to the Kubernetes [Secret resource](https://kubernetes.io/docs/concepts/configuration/secret/). Cloud Foundry Secrets will store arbitrary data in [CredHub](https://docs.cloudfoundry.org/credhub/) inject it into app containers via `tmpfs`-mounted files at a given path, using the same mechanism as [RFC 0030 - Add Support for File based Service Binding Information](https://github.com/cloudfoundry/community/blob/main/toc/rfc/rfc-0030-add-support-for-file-based-service-binding.md).

## Problem

Cloud Foundry currently supports app configuration via environment variables. Other application platforms, such as Kubernetes, support app configuration at runtime [via volume-mounted files](https://kubernetes.io/docs/concepts/configuration/secret/#using-secrets-as-files-from-a-pod). Many apps are adopting this file-based configuration approach, since environment variables have length limits and files can be updated without having to recreate the container. This RFC proposes introducing file-based configuration to support these sorts of apps on Cloud Foundry — without requiring app code changes.

### What About User-Provided Services?

Why can't developers use user-provided service instances (UPSIs) and service bindings for file-based app configuration? Some apps may have file-based config that don't naturally fit into the service binding model. For example, if an app relies on a config file at a certain path, that plath may not be configurable to `$SERVICE_BINDING_ROOT`. This is especially the case for commercial off-the-shelf software (COTS).

## Proposal

Add two new resources to the V3 Cloud Foundry API: `secret` and the `secret_binding`, along with associated CRUD API endpoints.

### Why Top-Level Resources?

Why not represent secrets as sub-resources of apps like environment variables? Two reasons:

1. Secrets may be larger than environment variables. Modeling them separately lets us naturally keep them in a separate database table and even use separate services, like CredHub, to store their contents.
2. Secrets may be shared across multiple apps. For example, a "logical app" may actually be several Cloud Foundry apps resources that need to share certain configuration, certificates, or other credentials. By scoping the `secret` at the `space` level, we can easily support this. Similarly, an app using the blue-green deployment pattern can easily share configuration between versions.

### `secret` and `secret_binding` Resources
The `secret` will be a `space`-scoped resource (similar to a `route` or a `service_instance`) that can be bound to one or more `app`s in the `space` using a `secret_binding`.

#### Example `secret` Object

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

The `type` field corresponds with a [CredHub credential type](https://docs.cloudfoundry.org/credhub/credential-types.html). To start, `secret`s will support the `value` and `json` credential types. In the future, this can be expanded to other CredHub-supported types like `certificate`, to support additional use cases.

#### Example `secret_binding` Object

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

The `mount_path` field defines the `tmpfs` directory that will contain files for the `secret`'s content. If a credential has subkeys (such as a [`json` type credential](https://docs.cloudfoundry.org/api/credhub/version/main/#_find_a_credential_by_id_type_json) or [`certificate` type](https://docs.cloudfoundry.org/api/credhub/version/main/#_find_a_credential_by_id_type_certificate)), then files will be made for each key.

For example, consider a `json`-type `secret` with the following `value`:

```json
"value": {
  "application.yml" : "---\napplication:\n ...",
  "secret.txt": "my-secret"
}
```

The above `secret` would mount files named `application.yml` and `secret.txt` at the path configured in the binding.

For a `value`-type `secret`, the file name be the `secret_binding`'s name.

### Creating a `secret`

To create a `secret`, users will use a new CLI command: `cf create-secret`.

```console
cf create-secret SECRET_NAME SECRET_TYPE -p <CREDENTIALS_INLINE_OR_FILE>
```

If `SECRET_TYPE` is `value` then contents of `-p` will not be parsed. If `SECRET_TYPE` is `json`, `certificate`, or some other CredHub credential type, then the contents of `-p` MUST be valid JSON and may be parsed.

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

### Reading a `secret` and Its Value
Users that have permission to view environment variables for an app will be able to view `secret` values within a `space`. We will introduce a separate endpoint for retrieving these (similar to how app environment variables and service instance credentials are retrieved): `GET /v3/secrets/:guid/value`.

```console
curl "https://api.example.org/v3/secrets/[guid]/value" \
  -X GET \
  -H "Authorization: bearer [token]"
  
"value" : {
  "some-json-key" : "some-json-value"
}
```

To support this, Cloud Controller will need to have both read and write permissions for the `secret`'s corresponding credential in CredHub.

### Creating a `secret_binding`
To create `secret_bindings`, users will use a new CLI command: `cf bind-secret`. This will create a `POST` request to `/v3/secret_bindings`.

```console
cf bind-secret APP_NAME SECRET_NAME BINDING_NAME
```

### CLI Changes
Work will need to be done to implement the following commands:
- `cf create-secret`
- `cf bind-secret`
- `cf secrets`
- `cf secret`
- `cf delete-secret`
- `cf unbind-secret`

In addition, modifications may be made to existing CLI commands to surface `secrets` and `secret_bindings`. For example, adding bound `secret`s to `cf app` output.

### Cloud Controller Changes
New database tables will need to be created to store `secret`s and `secret_binding`s. CRUD APIs will need to be created for these resources. We will also need an API to support viewing a `secret`'s value.

### BBS changes
BBS was recently updated to support `ServiceBindingFiles` as part of RFC 0030. A `secret`'s value may result in one or more files being created in the `tmpfs` mounted directory defined by the `MountPath` parameter.

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

### Launcher Changes?
The launcher (or something else) will need to be updated to retrieve credentials from CredHub for `Secret Bindings`. It currently already does this for CredHub references contained within `VCAP_SERVICES` using the app container's instance identity credentials. Is there something other than the launcher that should have this responsibility?

### Other Considerations

#### Not Using CredHub
Although Cloud Foundry comes with CredHub by default, it is not a required component. We could support `value` and `json` type `secret`s directly in Cloud Controller as a fallback.

#### CredHub Maximum Secret Size
Kubernetes Secrets and ConfigMaps have a [maximum size of 1 MiB](https://kubernetes.io/docs/concepts/configuration/configmap/#motivation). The [maximum size of a CredHub credential is 64Kb](https://docs.cloudfoundry.org/credhub/credential-types.html). If we plan on using CredHub, we will need to limit our Secrets to 64KB or increase the CredHub limit.

#### (Future) Rotatable Secrets
If we make the `*Files` parameters on the `DesiredLRP` mutable in BBS, then Cloud Controller could update the `secret`s in the `DesiredLRP`, without requiring container recreation.

For certain CredHub credential types such as `certificate` or `password`, we may be able to expose CredHub credential rotation/[regeneration](https://docs.cloudfoundry.org/api/credhub/version/main/#_regenerate_credentials_endpoint) functionality.
