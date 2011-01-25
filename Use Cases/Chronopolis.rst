Chronopolis
===========

Chronopolis is a distributed repository with a focus on providing long term
access to dark copies of data. Data is ingested at one of the three sites,
then internally replicated between the other sites. Each site operates
independent sets of hardware and monitoring tools to minimize the chance of
catastrophic failure.

Data is organized into a hierarchy based on the submitting organization
(provider) and submission within that collection. Submissions from a provider
are organized into collections. Currently, collections consist of one or more
bags of related data. Authentication is provided on a per-provider and
possibly per-collection basis.

Uses for the bag interface:

1. Provide an API which our data providers can use to ingest data into a QA pool
    - providers should be able to request the creation of new collections.
    - providers will notify Chronopolis of the total number of bags within a
      collection.
    - upon ingest of a collection, providers will receive a receipt confirming
      the bags were received and validated

2. Provider access to ingested data.
    - provide authenticated access to a providers holdings, including listing
      ingested packages and retrieval of data.
    - providers should be able to request retrieval from any chronopolis site.
    - Allow bag manifest retrieval to determine how content in Chronoplis
      varies from local copies.
