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

GETing ``/bags/`` <*BAG_ID*> ``/`` will return a response containing the
following metadata:

:links:
    List of links to other resources on this server (see below) using the
    following format, as in HTML ``link`` tags (see `RFC 5988
    <http://tools.ietf.org/html/rfc5988>`_ for valid rel values). 

    :rel:
        forward link types
    :href:
        URI for linked resource
    :type:
        advisory content type

:info:
    Parsed dictionary from ``bag-info.txt``

:bagit:
    Parsed dictionary from ``bagit.txt``

Clients may POST to ``/bags/`` <*BAG_ID*> ``/`` to perform several operations:
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
        Root for access to bag contents: for any file path in the manifest,
        ``/bags/`` <*BAG_ID*> ``/contents/`` <*BAG_ID*> will return the raw
        file.

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

Good HTTP Citizenship
~~~~~~~~~~~~~~~~~~~~~

* Servers *SHOULD* generate Cache-Control headers; clients *MUST* honor them
* Servers *MAY* use HTTP redirects to direct clients to HTTP-accessible
  backend storage for performance reasons
* If available, servers *SHOULD* return ``Content-MD5`` or ``Content-SHA1``
  headers using the hash value from the manifest; clients *SHOULD* validate
  these values if present
* Servers *SHOULD* support entity tags and ``If-None-Match``
* Servers *SHOULD* support HTTP Range to allow clients to resume transfers
* Clients *SHOULD* honor HTTP 500.13 Server Busy responses using exponential
  back-off

Operations
~~~~~~~~~~

For this discussion, it is assumed that servers may return standard HTTP
response code such as 401/403 to indicate that the client needs to
authenticate or lacks permissions to make changes.

Creating a new bag
^^^^^^^^^^^^^^^^^^

    #. Create the container:
        Client POSTs to ``/bags`` with the ID
        Server returns 201 pointing to the new bag's location

        Servers must return 409 Conflict if the ID is already in use

    #. Client PUTs ``bagit.txt`` and ``bag-info.txt``

    #. Client PUTs one or more manifest files under ``/contents/``

        Clients *MUST* provide the manifest files before uploading data

    #. Client PUTs data files under ``contents/data/``

        Servers *MUST* return HTTP 400 if the file is not listed in the
        manifest or the received contents fail checksum validation

    #. Client POSTs ``commit`` to the bag location

Deleting a bag
^^^^^^^^^^^^^^

    #. Client DELETEs bag location

Replicating a bag
^^^^^^^^^^^^^^^^^

    #. Client GETs ``manifest``
    #. Client GETs each listed content file
    #. Optionally, client performs an AtomPub POST to ``copies`` with the
       public URL of a copy conforming to this specification.

Requesting Server Validation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    #. Client POSTs operation=validate to ``/bags/`` <*BAG_ID*>
    #. Server returns HTTP 202 Accepted and an initial status resource with
       the following attributes:

       :uri:
           Unique URI which the client can GET to retrieve the current
           status

       :status:
           One of ``In Progress``, ``Failed``, or ``Successful``

       :progress:
           Integer percentage or null if the server does not support
           partial status

       :message:
           Human-readable summary message, which may only be available
           when the operation has completed

