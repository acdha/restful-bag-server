RESTful Bag Store
=================

Basic Features
--------------

* Pure HTTP
* Does not address authentication beyond standard HTTP
* Does not require an intelligent server (Apache 1.0 could work)

Controversial Points
--------------------

* Bag are immutable - alternatively, do we create ``versions`` resource instead
  of ``contents``?
* Implementations MUST support JSON representations of resources, MAY support
  XML and other formats


Design
------

This describes the public interface of an endpoint, which could be an entire
service or a project-specific subdirectory on generic content storage system.

The structure intentionally does not require any server support for the common
case of providing access to bag contents, allowing a read-only store to be as
simple as a correctly-structured webroot directory on a standard web server.

Structure
~~~~~~~~~

:/changes:
    Atom feed listing new bags

:/bags/:
    Resource listing available bags

Clients may PUT to /bags/*BAG_ID*/ to perform several operations:
    :commit:
        Complete an upload (see "Creating a bag" below)

        Servers *MUST* not include a bag in any public listings until the bag
        has been committed.

    :validate:
        Request that the server validate the bag contents against the manifest

Under ``/bags/`` <*BAG_ID*> ``/`` will be several resources:

    :copies:
        Atom feed listing alternate locations for this bag by URL

        TODO: specify format

        Mirrors can PUT their location after mirroring this bag. Servers are
        not required to accept these requests.

        TODO: Specify rel types for instances

    :notes:
        Atom feed containing comments from curators

        TODO: Should this be history?

    :manifest:
        Resource enumerating bag contents as hashes with several keys:

        :path:
            The file's full path relative to the bag root, i.e. ``data/foobar.tiff``

        :checksum:
            hash of encoded checksum values using the algorithm as the key

        Example::

            [
                {
                    "path": "data/path/to/example.pdf",
                    "checksum": {
                        "md5": "00fcbdf37a87dced7b969386efe6e132",
                        "sha1": "74a272487eb513f2fb3984f2a7028871fcfb069b"
                    }
                }
            ]

    :contents:
        Direct access to bag contents

    :metadata:
        Arbitrary additional metadata files stored in Java-style reversed
        domain prefixed files

        GET returns a simple file list (Atom feed?), allowing clients to
        decide whether they wish to retrieve a file

        The server promised only that the metadata files will be preserved
        with the same level of durability as the bag contents

        Example::

            [
                'gov.loc.exampleProject.backup_history.xml',
                'com.flickr.commons.userComments.json',
                'org.apache.tika.extractedMetadata.xml'
            ]


Versioning
~~~~~~~~~~

This is a major point of discussion: simply allowing bag contents to change
will substantially complicate the replication process and makes it challenging
to determine whether your copy is the same as an arbitrary remote copy.

Proposal 1

    Don't. Bags are changed by creating a copy with a new ID and, optionally,
    publishing a link to your copy with explanatory metadata.

Proposal 2

    Explicit versioning: the manifest and contents move under a new
    version/_hash_/ structure, with convenience ``version/latest`` which is
    either the only bag (on servers which promise immutability) or the latest
    version as determined by the server.

    Arbitrary symbolic names may be allowed but MUST redirect to the
    appropriate hash value.

    In either case, the server MUST ensure that any addition, modification or
    deletion to the bag contents, including the top-level tag files, will
    result in a new hash being calculated. Metadata files are not versioned
    to avoid local additions breaking replication.

    These semantics support the use of Git or Mercurial as storage backends
    for frequently changing content.