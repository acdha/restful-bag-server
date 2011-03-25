# encoding: utf-8
from urlparse import urljoin
import json
import logging
import os
import unittest

# TODO: Avoid our one non-stdlib dependency by writing a simple client class
#       which can encapsulate the request methods below
import requests


class ServerTests(unittest.TestCase):
    """
    Validation suite for a RESTful Bag server
    """

    def __init__(self, *args, **kwargs):
        super(ServerTests, self).__init__(*args, **kwargs)

        if "BASE_URL" in os.environ:
            self.base_url = os.environ['BASE_URL']
        else:
            raise RuntimeError("ServerTests must either be prepared with a "
                                "base_url or BASE_URL must be defined in the "
                                "system environment")

    def request(self, url, method="GET", expected_status_code=200, *args,
                **kwargs):
        """
        Perform an HTTP request with status checking

        returns response_obj
        """

        full_url = urljoin(self.base_url, url.lstrip("/"))

        resp = getattr(requests, method.lower())(full_url, *args, **kwargs)
        try:
            self.assertEqual(resp.status_code, expected_status_code)
        except:
            logging.error("%s %s returned %s (expected %s)", method, full_url,
                            resp.status_code, expected_status_code)
            raise

        # TODO: Validate Content-MD5/SHA1 headers if present

        return resp

    def requestJSON(self, url, headers=None, *args, **kwargs):
        """
        Perform a request which expects to receive a JSON response

        Returns a (response_obj, decoded_json) tuple
        """

        if headers is None:
            headers = {}

        headers["Accept"] = "application/json"

        resp = self.request(url, headers=headers, *args, **kwargs)

        self.assertEqual(resp.headers['content-type'], "application/json")

        return resp, json.loads(resp.content)

    def test_changes(self):
        resp, changes = self.requestJSON("/changes")

        self.assertTrue("apiVersion" in changes)
        self.assertEqual(changes["apiVersion"], "1.0")

        self.assertTrue("data" in changes)

        items = changes['data']['items']

        for item in items:
            self.assertTrue("id" in item)
            self.assertTrue("created" in item)  # BUG: Do ISO date validation!
            self.assertTrue("updated" in item)
            self.assertTrue("content" in item)
            self.assertTrue("canonical" in item['content'])

            canonical_url = item['content']['canonical']

            item_resp = self.request(canonical_url)
            item_resp.raise_for_status()

            for alternate in item['content'].get("alternates", []):
                self.assertTrue("access" in alternate)
                self.assertTrue("organization" in alternate)
                # Validation seems error prone here:
                self.assertTrue("href" in alternate)

    def test_bag_list(self):
        resp, bag_list = self.requestJSON("/bags/")

        self.assertTrue("pagination" in bag_list)
        self.assertTrue("objects" in bag_list)

        pagination = bag_list['pagination']
        objects = bag_list['objects']

        self.assertTrue("offset" in pagination)
        self.assertTrue("limit" in pagination)
        self.assertTrue("total_count" in pagination)

        self.assertTrue(pagination['offset'] <= pagination['limit'])
        self.assertTrue(pagination['offset'] <= pagination['total_count'])

        self.assertTrue(len(objects) <= pagination['limit'])

        if "next" in pagination:
            self.request(pagination['next'])
        if "previous" in pagination:
            self.request(pagination['previous'])

        for bag in objects:
            self.assertTrue("id" in bag)
            self.assertTrue("href" in bag)
            self.request(urljoin("/bags/", bag['href']))

    def test_bag_repr(self):
        resp, bags = self.requestJSON("/bags/")

        for bag in bags['objects']:
            resp, bag = self.requestJSON(urljoin("/bags/", bag['href']))

            raise NotImplementedError()
            # :links:
            #     List of links to other resources on this server (see below) using the
            #     following format, as in HTML ``link`` tags (see `RFC 5988
            #     <http://tools.ietf.org/html/rfc5988>`_ for valid rel values).
            #
            #     :rel:
            #         forward link types
            #     :href:
            #         URI for linked resource
            #     :type:
            #         advisory content type
            #
            # :info:
            #     Parsed values from ``bag-info.txt`` returned as a list of key-value
            #     pairs
            #
            # :bagit:
            #     Parsed dictionary from ``bagit.txt``

    def test_bag_validate(self):
        raise NotImplementedError()
        #. Client POSTs operation=validate to ``/bags/`` <*BAG_ID*>
        #. Server returns HTTP 202 Accepted and an initial status resource with
        # the following attributes:
        #
        # :uri:
        # :status:
        #     One of ``In Progress``, ``Failed``, or ``Successful``
        #
        # :progress:
        #     Integer percentage or null if the server does not support
        #     partial status
        #
        # :message:
        #     Human-readable summary message, which may only be available
        #     when the operation has completed

    def test_bag_copies(self):
        raise NotImplementedError()

    def test_bag_notes(self):
        raise NotImplementedError()

    def test_bag_metadata(self):
        # Test list structure
        # Test URLs exist
        raise NotImplementedError()

    def test_bag_manifest(self):
        raise NotImplementedError()

        #         :tag:
        #             List of tag files as defined in the BagIt specification section
        #             1.3 (Terminology)
        #
        #         :payload:
        #             List of payload files as defined in the BagIt specification
        #             section 1.3 (Terminology)
        #
        #         Each list contains dictionaries with the following structure:
        #
        #         :path:
        #             The file's full path relative to the bag root, i.e. ``data/foobar.tiff``
        #
        #         :checksum:
        #             Dictionary of encoded checksum values using the algorithm as the
        #             key. This is optional for tag files.

    def test_bag_contents(self):
        raise NotImplementedError()
        #     :contents:
        #         Root for access to bag contents: for any file path in the manifest,
        #         ``/bags/`` <*BAG_ID*> ``/contents/`` <*BAG_ID*> will return the raw
        #         file.

    def test_bag_creation(self):
        raise NotImplementedError()

    def test_bag_deletion(self):
        raise NotImplementedError()


if __name__ == "__main__":
    logging.basicConfig(format=("%(asctime)s %(levelname)s [%(funcName)s]: "
                                "%(message)s "))
    unittest.main()
