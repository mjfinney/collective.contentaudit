# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from collective.contentaudit.testing import COLLECTIVE_CONTENTAUDIT_INTEGRATION_TESTING  # noqa

import unittest


class TestSetup(unittest.TestCase):
    """Test that collective.contentaudit is properly installed."""

    layer = COLLECTIVE_CONTENTAUDIT_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if collective.contentaudit is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'collective.contentaudit'))

    def test_browserlayer(self):
        """Test that ICollectiveContentauditLayer is registered."""
        from collective.contentaudit.interfaces import (
            ICollectiveContentauditLayer)
        from plone.browserlayer import utils
        self.assertIn(ICollectiveContentauditLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_CONTENTAUDIT_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['collective.contentaudit'])

    def test_product_uninstalled(self):
        """Test if collective.contentaudit is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'collective.contentaudit'))

    def test_browserlayer_removed(self):
        """Test that ICollectiveContentauditLayer is removed."""
        from collective.contentaudit.interfaces import \
            ICollectiveContentauditLayer
        from plone.browserlayer import utils
        self.assertNotIn(ICollectiveContentauditLayer, utils.registered_layers())
