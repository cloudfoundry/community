# Governance Evolution
Improved transparency is the root of the governance evolution. 

We publish the current written and lived governance rules, principles and guidelines to a special repository in the cloudfoundry GitHub organization, namely “cloudfoundry/community”. This will be the single source of truth. Any change to the current governance will be done as pull requests to this repository.

While this information is at least partly available on e.g. cloudfoundry.org or spread through repositories, it is essential that the repository is the source of truth. It will clearly reflect who made which changes at which point in time. It should make it easily discoverable how the CloudFoundry community works, who is who and how to get involved.

To drive the effort of introducing and evolving such a repository a new PMC is created. Let’s call it PMC Community. The charter of that PMC would be to create the initial content, collect feedback and ensure that all PMCs follow the new guidelines. Later it would further evolve the content continuously looking into how the community can become more inclusive and welcoming. The PMC could rename itself into a new community group type, if it makes sense.

How would that PMC/group to be setup?

## Stages

### Stage 0

Add all information that is currently available, but spread (cloudfoundry.org, Github, etc.) to the community repository, e.g.:
* The current Development Governance Policy and Development Operations Policy documents converted to a Markdown structure
* All PMCs that exist each with
  * Currently known roles in that PMC and who is assigned
  * Current Meeting structure
  * Current Communication Channels
* Community Calendar
* The current repository lifecycle
* The current community roles
* The PMC council and its structure and its rights
* The CloudFoundry Board
* Current escalation path
* What about the “Kubernetes SIG” ;)
* What about the Community Advisory Board?

### Stage 1

Introduce first changes to the status quo:

* Any evolution has to be done via PRs to give the community the change to understand what has been changed at which point time and who has approved it (and has the chance to comment)
  * Who can decide to merge such a PR?
  * Even if there would be a time for feedback and review, decisions might feel like already done offline (clarity without influence)
* For each PMC and potentially projects within that PMC
  * A list of repositories the PMC owns
  * A Proposals and Decisions folder either in the community project with proposals in Markdown format or link to a CFF owned Google Drive
    * From here these documents have to be provided early in the public
    * The folder should also describe how the decisions are currently made
  * A link to the roadmap (markdown, document or GitHub Projects)
  * The Community Group guidelines will require that all these artifacts must be kept up-to-date
    * If the PMC Community has many people, who would actually ensure, that this happens

### Stage 2

Propose the following changes to the decision process, roadmaps, PMC/Community Group rules in the PMC Community proposal folder. This might actually require more stages.

* Roadmap
  * Additions to the roadmap should be introduced well ahead of actual implementation work to be started to allow input and discussion within the community
    * Feature proposals 
      * should be detailed according to the size (to reduce the overhead for small things). Could be as small as a single Github issue, an epic or even a bigger topic that will require multiple epics to be implemented.
      * should state what is proposed, why it is proposed, what consequences it has and how it could be implemented
      * should state who is prepared to take on the work (both implementation and maintenance)
  * Removal from the roadmap / Changing priority/milestone
    * should state why it should be removed
    * should allow other community members to take on the work instead
  * The links between project and PMC roadmaps should be transparent
    * To what roadmap items does concrete project work belong?
* Voting
  * We should keep trying to reach consensus
  * In case a vote is required, in addition to a majority of Governance by contribution as it is defined today, we should add a requirement to have a majority of member companies participate (at least we cannot afford a single member company to overwhelm any votings)
  * Governance by contribution should be counted across projects and PMCs
    * No need to spread contributors across projects to influence decisions in other parts of the community
* Community Groups
  * The central governing body (currently the PMC Council) can delegate responsibility
  * Closed door groups
    * Security response
    * Licensing (Example: Istio version bump 1.4 -> 1.6)
    * Interested members should be able to get behind the closed doors
  * An additional group type could be proposed at this stage
    * The next level of authority would here as well be the PMC Council, where the name might need to change to e.g. just Council
      * SIG Community
      * SIG Roadmap
* Path to membership/committer:
  * Make the Distributed Committer Model a second pillar that every PMC/Project must accept
    * This would require continuous contributions and good communication
      * We could introduce a certain contributor status that would also be listed for a PMC/project in the community project
      * This contributor status could be a requirement for requesting to become a committer
    * A project or PMC can then decide to promote the person to be a committer on request
      * The community repository should provide a template for such a request
      * What aspects of this could be behind closed doors?
    * Requires transparency provided by the community repository to easily discover what work would help the community and who to contact
