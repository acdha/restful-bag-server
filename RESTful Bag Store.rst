RESTful Bag Store
=================

Basic Features
--------------

* Pure HTTP
* Does not address authentication: use HTTP auth if needed

Controversial Points
--------------------

* Bag are imutable - alternatively, do we create ``versions`` resource instead
  of ``contents``?
* Implementations MUST support JSON, MAY support XML


Design
------

This describes the public interface of an endpoint, which could be an entire
service or a project-specific subdirectory on generic content storage system.

Structure
~~~~~~~~~


``/changes``
    Atom feed listing new bags

``/bags/``
    Resource listing available bags

Under ``/bags/`` <*BAG_ID*> ``/`` will be several resources:

    ``copies``
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

        GET returns a simple file list, allowing clients to decide whether
        they wish to retrieve a file

        Example::

            [
                'gov.loc.exampleProject.backup_history.xml',
                'com.flickr.commons.userComments.json',
            ]