# Meta

- Name: Documenting the CF API with OpenAPI
- Start Date: 2025-07-23
- Author(s): @flothinkspi
- Status: Draft
- RFC Pull Request: [community#1256](https://github.com/cloudfoundry/community/pull/1256)

## Summary

With the acceptance of
[RFC-32](https://github.com/cloudfoundry/community/blob/d7b48620d0da3bcadeea18aaf64f6fa36c329e7f/toc/rfc/rfc-0032-cfapiv2-eol.md),
a problem arises for users of CF who rely on unsupported client
libraries that are not maintained and just work with the deprecated CF V2 API. To ensure the success of
[RFC-32](https://github.com/cloudfoundry/community/blob/d7b48620d0da3bcadeea18aaf64f6fa36c329e7f/toc/rfc/rfc-0032-cfapiv2-eol.md)
and to enable users to better transition to the V3 API, and also future-proof the CF API documentation, this RFC proposes
to document the CF API V3 using the OpenAPI specification.

## Problem

## Motivation

1. Improve the overall CF user experience, increasing the adoption and
popularity of CloudFoundry.

2. Support the adoption of
[RFC-32](https://github.com/cloudfoundry/community/blob/d7b48620d0da3bcadeea18aaf64f6fa36c329e7f/toc/rfc/rfc-0032-cfapiv2-eol.md)
by offering an more user-friendly path for users away from the CF V2 API.

3. Provide a widely adopted documentation format (OpenAPI) that enables many new usecases from programatic access to the CF API docs and schema to generating Documentation pages, automatic tests of documentation vs implementation or also better AI Agent integration.

## Proposal

### Documenting the CF V3 API with OpenAPI

With [OpenAPI](https://www.openapis.org/), APIs can be defined in a
machine-readable format (YAML), enabling the generation of client
libraries for various programming languages and the rendering of
interactive HTML API documentation. The OpenAPI specification is widely
adopted and supported by many tools. A [Proof of Concept
(PoC)](https://github.com/FloThinksPi/cf-api-openapi-poc) and [another Proof of Concept](https://github.com/cloudfoundry-community/capi-openapi-spec) is already
exploring the documentation of the CF V3 API as an OpenAPI spec,
providing a glimpse (currently with incorrect content) of the potential
look and feel of this documentation format.

The CloudFoundry organization MAY document the CF API V3 using the
OpenAPI specification. Which then can be used by CF Maintainers or CF Users to
leverage a huge toolchain around OpenAPI to generate client libraries, documentation pages, and more. This MAY render a transition like for example from a unsupported client library that only supports the CF V2 api towards using the CF V3 api a lot more easier since the available toolchain around OpenAPI is big, valuable, a time saver and then available to CF Users.
Such usecases include for example:

- [Swagger UI](https://swagger.io/tools/swagger-ui/) for interactive API documentation.
- [Swagger Codegen](https://swagger.io/tools/swagger-codegen/) for generating client libraries
- [OpenAPI Generator](https://openapi-generator.tech/) for generating client libraries and server stubs in various languages.
- [Redoc](https://redocly.com/redoc/) for generating static API documentation.
- [Postman](https://www.postman.com/) for API testing and documentation.
- [Dredd](https://dredd.org/en/latest/) for testing API documentation against the implementation.
- [AI Agents](https://github.com/janwilmake/openapi-mcp-server) for improved integration with AI-powered tools.

### Phases

**Implementation** - Convert <https://github.com/cloudfoundry-community/capi-openapi-spec> to a repository in the official cloudfoundry organization.Document the CF API V3 using the OpenAPI specification. Also generate a html documentation to replace the current page. Optionally build up, if possible, a validation(integration test) that validates if the OpenAPI spec is in sync with the actual implementation of the CF API V3.

**Checkpoint** - TOC review and approval of the project, ensuring the
OpenAPI documentation is complete in comparison to the current one and of appropriate quality. Replacement of the current CF API V3 website with representing the OpenAPI spec. Also release the OpenAPI spec for programmatic access to the CF API V3 documentation.

## Impact and Consequences

### Positive

- CF may see an increase in adoption and popularity due to improved
usability and user experience and the use of a documentation format
(OpenAPI) that is widely adopted in the industry and integrates well
with other tools. The time needed to develop against the CF API may
decrease, leading to faster implementation for users and increased statisfaction.

- The OpenAPI documentation format empowers users with unique
requirements to generate their own client libraries or starter
templates, providing an exceptional user experience for specialized
use cases.

- The OpenAPI documentation enables programmatic access to the CF API
documentation and schema, allowing for automatic tests of
documentation vs implementation, and better AI Agent integration. A lot of new usecases and adoption may arise from this.

- May reduce backpressure onto
[RFC-32](https://github.com/cloudfoundry/community/blob/d7b48620d0da3bcadeea18aaf64f6fa36c329e7f/toc/rfc/rfc-0032-cfapiv2-eol.md)
due to better enabling of users to transition to the V3 API.

### Negative

- The CloudFoundry organization will have to invest time and resources
to document the CF API V3 using the OpenAPI specification and work on two documentation formats in parallel until the OpenAPI is so mature that it can fully replace the existing documentation.
