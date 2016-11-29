# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from infoporto.push.testing import INFOPORTO_PUSH_INTEGRATION_TESTING  # noqa
from plone import api

import unittest


class TestSetup(unittest.TestCase):
    """Test that infoporto.push is properly installed."""

    layer = INFOPORTO_PUSH_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if infoporto.push is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'infoporto.push'))

    def test_browserlayer(self):
        """Test that IInfoportoPushLayer is registered."""
        from infoporto.push.interfaces import (
            IInfoportoPushLayer)
        from plone.browserlayer import utils
        self.assertIn(IInfoportoPushLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = INFOPORTO_PUSH_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['infoporto.push'])

    def test_product_uninstalled(self):
        """Test if infoporto.push is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'infoporto.push'))
