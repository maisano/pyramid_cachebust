import unittest

from pyramid import testing


class TestIntegration(unittest.TestCase):
    def setUp(self):
        import os
        from pyramid_cachebust import includeme

        self.config = testing.setUp()
        includeme(self.config)

    def tearDown(self):
        testing.tearDown()

    def test_methods_exist(self):
        introspector = self.config.registry.introspector

        cburl = introspector.get('request extensions', 'cachebusted_url')
        cbpath = introspector.get('request extensions', 'cachebusted_path')

        self.assertIsNotNone(cburl)
        self.assertIsNotNone(cbpath)

        type_match = cburl.type_name == cbpath.type_name == 'request method'

        self.assertTrue(type_match)
