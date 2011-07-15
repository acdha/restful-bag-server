National Digital Newspaper Program
==================================

`NDNP <http://www.loc.gov/ndnp/>`_ is an NEH funded project to digitize the
microfilm of historic American newspapers.
Digitization happens around the country at 23 institutions according to
specific imaging and metadata
`specifications <http://www.loc.gov/ndnp/techspecs.html>`_, afterwhich the data
is bundled up on hard drives and shipped to the Library of Congress (LC). Each
"batch" of content is bagged on receipt and then loaded into
`Chronicling America <http://chroniclingamerica.loc.gov/>`_, a public facing
web application for researcher access, and where it is also made available in
`bulk <http://chroniclingamerica.loc.gov/data/>`_.

The reason for making the bags of newspaper content available in bulk has been
two-fold:

* To support projects like
  `Digging into Data Challenge <http://www.diggingintodata.org/>`_ by
  providing bulk access to the data for local computation. LC wants to enable
  others to repurpose the content in ways that are unanticipated by the NDNP
  project.

* To enable digital preservation by making it possible for partner
  institutions and other interested parties to mirror the content for
  their own purposes, hoping that lots of copies will keep stuff a bit safer.

While this approach of simply mounting the bags on the Web has allowed
simple retrieval of content with web harvesting tools like
`wget <http://www.metaarchive.org/>`_, there is a perceived need to support:

* Discovery of what bagged content is available for harvesting and where
  to harvest it from (preferably a URL). Both the complete set of bags, as
  well a mechanism for discovering when new bags are available needs to
  be supported.

* An update mechanism for NDNP Awardees and other parties to let LC know
  when a particular set of content has been successfully harvested and
  what URL it is available from. It would be essential that LC be able
  to then use that URL to see if the content was in fact there, on an
  ongoing basis.

This last issue is very important to enable digital preservation scenarios
where the NDNP program would like to know when and where backup copies are
available if the inevitable happens, and content is lost.
