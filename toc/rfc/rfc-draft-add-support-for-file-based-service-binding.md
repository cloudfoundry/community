# Meta
[meta]: #meta
- Name: Add Support for File based Service Binding Information
- Start Date: 2024-03-11
- Author(s): @beyhan
- Contributing Authors: @stephanme, @loewenstein
- Status: Draft
- RFC Pull Request: (fill in with PR link after you submit it)



## Summary

The current contract between the CF platform and applications for service binding information is based on an environment variable. The Linux Kernel defines size limit per environment variable and there are also other limitations with this approach. That is why, CF should add support for an alternative option to provide service binding information which can address the limitations of the current approach.

## Problem

The CF platform provides service binding Information to hosted applications via the [VCAP_SERVICES environment variable](https://docs.cloudfoundry.org/devguide/services/application-binding.html). There are following challenges with this approach:
- The environment variable length has a hard limit of `131072` bytes per variable which is controlled by the underlying [Linux kernel](https://github.com/torvalds/linux/blob/master/include/uapi/linux/binfmts.h). The environment variable size is defined by `MAX_ARG_STRLEN`, which is a constant with the value `PAGE_SIZE*32` where page size is `4096` bytes. This means that to change the size limit for the CF platform a recompiled kernel with updated value for `MAX_ARG_STRLEN` is required. This limit could be an issue for applications using many services. If the limit is reached by an application, it will fail to stage as discussed in [this issue](https://github.com/cloudfoundry/garden-runc-release/issues/160).
- Updates of the service binding Information require restage. This is not optimal for an eventual support of [Binding rotation](https://github.com/openservicebrokerapi/servicebroker/blob/master/spec.md#binding-rotation) specification from the OSBI API spec.


## Proposal

The CFF community should implement an alternative approach for service binding information based on `tmpfs` file(s). Using a file or files to provide service binding information to applications will address the challenges listed in the problem section because:
- The file size limit can be controlled by the CF platform
- Already today CF uses `tmpfs` for [Instance Identity Credentials](https://docs.cloudfoundry.org/devguide/deploy-apps/instance-identity.html) which are rotated without restarting the application every `24h` by default

The two approaches should be supported in parallel. Users should be able to select which approach Cloud Controller should use to deliver the binding information. Applications with binding information >`130KB` have to go with the file option and adopt it. There are two alternatives regarding service binding file organization:
1. The `VCAP_SERVICES` content is stored in a file which location is specified via the `VCAP_SERVICES_FILE_PATH` env var in the same format as the `VCAP_SERVICES` environment variable
   * Advantages:
      * Less disruptive for applications consuming the `VCAP_SERVICES` env var
      * Less implementation effort for the Cloud Controller
   * Disadvantages:
      * Can’t make use of tools and libraries from the Cloud Native community because K8s specifies a different file structure and format for the service binding information
2. Implement the K8s service binding specification. The environment variable `SERVICE_BINDING_ROOT` defines the location for the service bindings. There is a file per service binding. The name of the file and the format follow the [K8s specification](https://servicebinding.io/):
   * Advantages:
      * CF community could re-use service binding libraries from the Cloud Native community
      * Moving application between CF or K8s deployments will be easier
   * Disadvantages
      * Higher implementation efforts for the Cloud Controller

The 2) alternatives offers more than just addressing the issue of this RFC. It suggests an option to evolve the CF platform towards a different service binding specification defined by the Cloud Native community. This means higher implementation efforts for the CF platform and application developers, but possible benefits from the Cloud Native community. This RFC has a light preference for the 2) alternative because of the listed advantages but the feedback of the CF community is wanted here.

Additionally, the application environment is stored in the `CCDB` and `BBS DB` that is why we should define a limit for the size of it, which makes it possible to be stored in the according DBs and doesn’t impact the performance of the communication between Cloud Controller and the Diego API. That is why this RFC suggests a limit of `1MB`, which is roughly ten times higher than the current one of 130KB. This is subject for evaluation during the implation of this RFC.

> [!NOTE]
> The voting in the CF community selected the option 2). That is why, this RFC focuses on option 2) in the next sections. The voting results are available [here](https://github.com/cloudfoundry/community/pull/804#discussion_r1555938410).

### Implementation Overview

Cloud Controller should introduce a new app feature for activation of the file-based approach. This means that the [App Features API](https://v3-apidocs.cloudfoundry.org/version/3.159.0/index.html#app-features) could be used here and a new feature flag called “file-based-service-bindings" should be introduced.
The [contract](https://github.com/cloudfoundry/bbs/blob/main/doc/actions.md) between Cloud Controller and Diego should be extended so that file name and file content for the application container can be specified. E.g. the run action could look like this when file approach is selected:

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
 Files: []*models.Files{
    {
      Name: "/etc/cf-instance-binding",
      Value: "VALUE",
    },
  },
  ResourceLimits: &models.ResourceLimits{
    Nofile: 1000,
  },
  LogSource: "some-log-source",
  SuppressLogOutput: false,
}
```

## Workstreams

### App Runtime Interfaces WG

Cloud Controller should add a new App Feature for activation of the new file-based service binding option. If the file-based service binding feature is active for an application the Cloud Controller should generate a Run action, which configures the service bindings to be stored as tmpfs file(s) in the application container instead of `VCAP_SERVICES` environment variable. Additionally, Cloud Controlle should set the `SERVICE_BINDING_ROOT` environment variable accordingly. The translation from `VCAP_SERVICES` to file based bindings should follow the CNB translation in `libcnb`. The implementation in `libcnb` could be found [here](https://github.com/buildpacks/libcnb/blob/main/platform.go#L199-L2270) and it does following:

* The `credentials` object is translated into key/value files where key is the file name and value is the file content. If a key in `credentials` has a nested `JSON` value, then the `JSON` is written as the content of the file.
* The `label` from `VCAP_SERVICES` is translated to `type`.
* The top-level key from the `VCAP_SERVICES` is translated to `provider`.

The RFC doesn't mention all attributes documented for [VCAP_SERVICES](https://docs.cloudfoundry.org/devguide/deploy-apps/environment-variable.html#VCAP-SERVICES) but the same approach should be followed for them also. E.g. `syslog_drain_url` should be the file name and the URL the file content. This should be fine with the K8s binding specification because it allows any entry as documented in the [Provisioned Service](https://servicebinding.io/spec/core/1.1.0/#provisioned-service) section.

Additionally, the suggested limit of `1MB` for the size should be implemented.

### App Runtime Platform WG

Diego should add support for the new argument of the Run action to create files with the desired content. Like the [Instance Identity credentials](https://docs.cloudfoundry.org/devguide/deploy-apps/instance-identity.html) implementation, the [Diego Executor](https://github.com/cloudfoundry/executor) should be extended to prepare the `tmpfs` mount and create the required files for an application container. For reference there is a [CredManager](https://github.com/cloudfoundry/executor/blob/db9758c0142ae9c11dad26de672735fb20566105/depot/containerstore/credmanager.go) , InstanceIdentityHandler and the `tmpfs` mount is configured in the [Diego release](https://github.com/cloudfoundry/diego-release/blob/2d7d7c1373f2a61077c74e33a397a5f69b11b131/jobs/rep/templates/setup_mounted_data_dirs.erb#L38-L56) for the current implementation of the Instance Identity Credentials. The files should have security permissions like the Instance Identity Credentilas `644` or even higher `600` owned by the uid running the app if possible.

## Possible Future Work

The App Features API aren’t supported currently in the CF CLI and [app manifest](https://docs.cloudfoundry.org/devguide/deploy-apps/manifest-attributes.html). To make the use of this proposal for CF operators easier this should be addressed.

### App Manifest Attributes Proposal

The CF app manifest is [additive](https://v3-apidocs.cloudfoundry.org/#apply-a-manifest-to-a-space) not declarative. That is why if we want to disable app feature flags via the app manifest a status input like `enabled` or `disabled` will be required. Like:

```
---
applications:
- name: test-app
  features:
  -	file-based-service-bindings: true
```
or as alternative proposal:

```
---
applications:
- name: test-app
  features:
  -	name: file-based-service-bindings
    enabled: true
```

### CF CLI new Commands Proposal

- `app-feature-flags`                   Retrieve list of available app feature flags with status
- `app-feature-flag`                    Retrieve an individual app feature flag with status
- `enable-app-feature-flag`             Allow use of an app feature
- `disable-app-feature-flag`            Disable use of an app feature

