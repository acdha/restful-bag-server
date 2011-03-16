About Archivematica
===================
Archivematica is an open-source digital preservation system that is still undergoing active design and development (http://archivematica.org). Release 0.7-alpha was made available February 18, 2011. Development is led by Artefactual Systems (http://artefactual.com) in collaboration with a number of archives and libraries.

Archivematica's primary design principles are ISO-OAIS functional model compliance, digital curation micro-services, and UNIX pipeline (stdout/stderr). The primary function of Archivematica is to process Submission Information Packages (SIPs), apply media-type preservation plans and create high-quality, repository-independent Archival Information Packages (AIPs) using METS, PREMIS and Bagit (http://archivematica.org/overview). Archivematica also uploads Dissemination Information Packages (DIPs) containing descriptive metadata and web-ready access copies to an online access system (e.g. ICA-AtoM, Dspace, ContentDM, etc.). 


Archivematica and Bagit
=======================
Archivematica is already using Bagit to package Archival Information Packages (AIP). We are now considering whether to standardize on using Bagit to package and transmit SIPs and DIPs as well. This diagram illustrates the SIP, AIP and DIP interfaces that we expect to be functional in the 0.8-beta release (scheduled for December 2011) http://archivematica.org/wiki/images/5/59/Archivematica-0.8-beta-architecture.png

The Archivematica uses cases for a Bagit REST API assume:

(a) SIPs, AIPs and DIPs are all Bags packaged in compliance with the Bagit specification

(b) Archivematica implements the Bagit REST API

(c) The archival storage, backup, and access components as well as any SIP posting systems/tools have a corresponding REST APIs (at the least the subset required for that particular use case)


Archivematica RESTful Bagit API Use Cases
==========================================

(1) Archivematica responds to a POST SIP request from (a) Archivematica pre-ingest tools or (b) external system/service

(2) Archivematica responds (success/error) to a GET request for a SIP receipt/integrity check

(3) Archivematica sends a POST AIP request to primary archival storage 

(4) Archival storage responds (success/error) to an Archivematica GET request for AIP receipt/integrity check

(5) Archival storage or Archivematica sends a POST AIP request to one or more backup storage locations

(6) Backup storage responds (success/error) to an Archivematica GET request for AIP receipt/integrity check

(7) Archival storage and backup respond to a (periodic) Archivematica GET request for AIPs integrity check information

(8) Archival storage responds to a GET AIP request from Archivematica (e.g. a 'read' action) 

(9) Archivematica sends a PUT AIP request to archival storage (e.g. after Archivematica performs an 'update' action)

(10) Archivematica sends a POST DIP request to an access system

(11) Access system responds (success/error) to an Archivematica GET request for DIP receipt/integrity check

(12) Archivematica sends a PUT DIP request to an access system (e.g. after Archivematica updates AIP metadata or generates a new access copy)

(13) Archivematica responds to a a PUT AIP request from an access system (e.g. after an access system updates metadata which should be synced in the AIP)

-----------------

NOTE: There is likely some overlap/duplication in these use cases. A Bag does not care if it is being used as SIP, AIP or DIP, i.e the Bag REST API response may be identical if it is responding to a SIP or AIP receipt/integrity check request.

NOTE: Each use case may in fact have more than one request/response transaction. Further analysis is required.
