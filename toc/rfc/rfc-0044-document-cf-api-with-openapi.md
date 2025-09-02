# Meta

- Name: Documenting the CF API with OpenAPI
- Start Date: 2025-07-23
- Author(s): @flothinkspi
- Status: Accepted
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

This RFC proposes a phased approach to mitigate risks and allow for early feedback.

**Phase 1: Proof of Concept (PoC)**

The initial phase focuses on demonstrating the feasibility and defining the process for creating and maintaining the OpenAPI spec. The goal is to evaluate different approaches for converting the existing implementation into an OpenAPI spec, and to understand how CAPI developers would work with it. One non-trivial endpoint should be implemented completely as part of the PoC.

The PoC MAY be located at <https://github.com/cloudfoundry/cf-openapi> where everyone is invited to try out and contribute different experiments.

Key questions to be answered in this phase:

- How can the initial spec be generated from existing API documentation or source code?
- What does the development process for updating the spec look like?
- How can the spec be integrated into the existing CI and CAPI release processes?
- How can we test the spec against the implementation to ensure they are in sync?
- If generating the spec from source code, how can metadata like examples and manually written descriptions be maintained within the sources?

**Phase 2: Implementation and Checkpoint**

Based on the findings of the PoC, the next phase is to complete the implementation of the OpenAPI spec for the entire CF API V3.

A checkpoint with the ARI WG is required before proceeding. This checkpoint will evaluate if the spec is complete, usable, and meets the required quality standards.
The OpenAPI effort should be stopped if the expected spec quality cannot be achieved.

**Phase 3: Rollout and Deprecation**

Once the OpenAPI spec is deemed complete and of good quality, the following steps will be taken:

- The generated HTML documentation will replace the current API documentation website.
- The OpenAPI spec will be published alongside the existing documentation.
- The old API documentation will be archived and made available for reference and all older versions that were released before using the openapi spec.

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

- The CloudFoundry organization, and specifically the App Runtime Interfaces (ARI) Working Group, will have to invest time and resources to document the CF API V3 using the OpenAPI specification. This will require working on two documentation formats in parallel until the OpenAPI specification is mature enough to fully replace the existing documentation.

## Future Improvements

This RFC focuses on the initial implementation of the OpenAPI specification for the CF API V3. However, there are several potential future improvements that could be explored once the initial implementation is complete. These MAY be explored as part of this RFCs PoC. However no plans are concretely defined to use/support generation based client libraries.
