UC San Diego Libraries
======================

`UCSD Libraries <http://libraries.ucsd.edu>`_ have about 300,000 digital objects
(`publicly available subset <http://libraries.ucsd.edu/digital/>`_).  We have
stored a majority of our digital objects in a preservation repository, and have
been experimenting with using bags to package our digital objects.  The RESTful
Bag Server promises to be a standard way to move bags between our system and
the preservation systems, managing updates, etc.  Having a standard way to
transport bags and coordinate updates would make it easier to use multiple
repositories, instead of having to implement a new process for each repository.

Use Cases
=========

(1) Initial Deposit
    - Transfer all 300K objects (12 TB) to a repository.

(2) Periodic Updates
    - Transfer new and/or updated objects to a repository.

(3) Integrity Checking
    - Retrieve checksums for all stored files to verify they match expected
      values.

(4) Disaster Recovery
    - Retrieve objects from repository in case of accidental deletion,
      corruption, etc.  This could range from a single object, small groups of
      objects, or the entire dataset, depending on the nature of the problem.

Open Questions
==============

(1) Push vs. Pull: We could either push our content to a repository running a
    bag server, or we could run a bag server and let the repository pull data
    from it.
    - Push would require more work by the repository, but would then provide a
      good API for us to monitor our content and push updates.
    - Pull would be more work on our part (including access control), and would
      require more active monitoring of updates by the repository.

(2) Zipped Bags: We've been working with tar or zip-archived bags to reduce the
    overhead of transfering many small files (our digital objects typically
    include one or more master files, plus several small metadata files and
    derivatives).  The main problem we've encountered so far is support for
    files larger than 8GB, but these seem to be resolvable.  Are there any
    plans to support zipped bags, or any alternative to improve performance of
    sending many small files?

(3) Checksumming Overhead: Calculating checksums on large files is very time
    consuming.  It would dramatically improve performance if we can read data
    files (when serving or creating bags remotely) before serving/creating
    bag-info.txt to prevent redundant data reads.
