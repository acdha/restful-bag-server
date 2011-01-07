RESTful Bag Store
=================

Basic Features
--------------

* Pure HTTP
* Does not address authentication: use HTTP auth if needed

Controversial Features
----------------------

* Bag imutability - alternatively, do we create a ``versions`` resource and subdir under ``contents``?
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
            
            Mirrors can use a PUT request after mirroring this bag
            
            TODO: decide how to deem something the "canonical" copy
    
        ``notes``
            Atom feed containing comments from curators
    
        ``manifest``
            Resource enumerating bag contents as hashes with several keys:
            
            ``path``
                The file's full path relative to the bag root, i.e. ``data/foobar.tiff`` 
            
            ``checksums``
                hash of encoded checksum values using the algorithm as the key

        ``contents``
            Direct access to bag contents