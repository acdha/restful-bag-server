Penn State Digital Stewardship Program
======================================

Penn State's `Digital Stewardship Program <http://stewardship.psu.edu/>`_ is an
institutional initiative to address digital content and data management needs in
areas such as digital library collections, scholarly communications, electronic
records archiving, and e-science/e-research data management. Building on
existing services and infrastructure, the program is developing an interoperable
and extensible suite of discovery, preservation, curation, archival, and storage
services.

One of the stewardship program's projects is a prototype web application
providing lightweight curation services.  Objects ingested into this application
will be stored as bags on disk, so we expect to accumulate a sizable number of
bags in the coming years.

Penn State is a member of the MetaArchive Cooperative and has looked
at the functionality provided by its LOCKSS-based network.  While that
model will work for some of our data, the scale and size of our data
may be more than the MetaArchive private LOCKSS network can reasonably
handle.

Previously we have discussed bilateral bag replication services with the
University of North Texas, primarily for far-off-site disaster recovery
purposes.  We see some benefit of tackling cross-institutional replication at
the bag level, rather than at the file level, in case we should ever need to
interoperate with one another's content.  Some of these less clear but
nonetheless attractive services might be around discovery or publishing of bags,
such as detailed in the NDNP use case.

Thus, we're keenly interested in a low-barrier method of replicating bags to and
from partners in a potential bag interop network.
