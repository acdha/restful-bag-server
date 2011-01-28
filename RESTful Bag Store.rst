RESTful Bag Store
=================

Overview
--------

This document briefly describes an approach to making `BagIt
<http://en.wikipedia.org/wiki/BagIt>`_ style containers of content
available on the Web so that content can be easily discovered,
retrieved and otherwise annotated. BagIt style directories, or Bags,
are a lightweight mechanism for documenting a set of files and their
fixities in a manifest, and associating them with some generic
metadata.

Work on an a REST API for Bags grew out of conversations started by
the `Educopia Institute <http://www.educopia.org/>`_ in
late 2010. Before diving into the basic design, a few use cases to
describe the problem space will be described.

Use Cases
---------

* `National Digital Newspaper Program <Use%20Cases/NDNP.rst>`_
* `Chronopolis <Use%20Cases/Chronopolis.rst>`_
* `Penn State <Use%20Cases/PennState.rst>`_

Design
------

This describes the public interface of an endpoint, which could be an entire
service or a project-specific subdirectory on generic content storage system.

The structure intentionally does not require any server support for the common
case of providing access to bag contents, allowing a read-only store to be as
simple as a correctly-structured webroot directory on a standard web server.

Basic Features
--------------

* Pure HTTP
* Does not address authentication beyond standard HTTP
* Does not require an intelligent server (Apache 1.0 could work)

Controversial Points
--------------------

* Bags are immutable - alternatively, do we create ``versions`` resource instead
  of ``contents``?

    :mjgiarlo:
        Adding versioning semantics adds complexity to the bag store service.
        The question is whether it's worth it. Hard to address w/o use cases.
        My hunch is that bags should be mutable with versioning enabled (using
        e.g. git behind the scenes, like PSU is doing via GitPython with its
        "repository").

* Implementations MUST support JSON representations of resources, MAY support
  XML and other formats


Structure
~~~~~~~~~

:/changes:
    Feed listing new bags (should the feed list only new bags, or also e.g.
    deleted and modified bags?)

:/bags/:
    Resource listing available bags.

    Responses are returned with pagination:

        :pagination:
            :offset:
                Offset into the list of bags
            :limit:
                Limit on the number of results
            :total_count:
                Total number of bags
            :next:
                Link to the next page of results, if available
            :previous:
                Link to the previous page of results, if available
        :objects:
            List of bags in the following format:
                :href:
                    Location of the bag
                :id:
                    User-assigned bag ID

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
        Parsed values from ``bag-info.txt`` returned as a list of key-value
        pairs

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
        Feed listing alternate locations for this bag by URL

        TODO: specify format

        Mirrors can PUT their location after mirroring this bag. Servers are
        not required to accept these requests.

        TODO: Specify rel types for instances

    :notes:
        Feed containing comments from curators

        TODO: Should this be history?

    :manifest:
        Resource enumerating bag contents. This is a dictionary with two keys:

        :tag:
            List of tag files as defined in the BagIt specification section
            1.3 (Terminology)

        :payload:
            List of payload files as defined in the BagIt specification
            section 1.3 (Terminology)

        Each list contains dictionaries with the following structure:

        :path:
            The file's full path relative to the bag root, i.e. ``data/foobar.tiff``

        :checksum:
            Dictionary of encoded checksum values using the algorithm as the
            key. This is optional for tag files.

        Example::

            {
                "payload": [
                    {
                        "checksum": {
                            "md5": "00fcbdf37a87dced7b969386efe6e132",
                            "sha1": "74a272487eb513f2fb3984f2a7028871fcfb069b"
                        },
                        "path": "data/path/to/example.pdf"
                    }
                ],
                "tag": [
                    {
                        "path": "bagit.txt"
                    },
                    {
                        "path": "bag-info.txt"
                    },
                    {
                        "path": "manifest-md5.txt"
                    },
                    {
                        "path": "manifest-sha1.txt"
                    }
                ]
            }

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

        Servers *MUST* return 409 Conflict if the ID is already in use

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

