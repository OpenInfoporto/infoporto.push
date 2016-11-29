# -*- coding: utf-8 -*-
from plone.app.testing import TEST_USER_ID
from zope.component import queryUtility
from zope.component import createObject
from plone.app.testing import setRoles
from plone.dexterity.interfaces import IDexterityFTI
from plone import api

from infoporto.push.testing import INFOPORTO_PUSH_INTEGRATION_TESTING  # noqa
from infoporto.push.interfaces import IDevice

import unittest2 as unittest


class DeviceIntegrationTest(unittest.TestCase):

    layer = INFOPORTO_PUSH_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='Device')
        schema = fti.lookupSchema()
        self.assertEqual(IDevice, schema)

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='Device')
        self.assertTrue(fti)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='Device')
        factory = fti.factory
        obj = createObject(factory)
        self.assertTrue(IDevice.providedBy(obj))

    def test_adding(self):
        self.portal.invokeFactory('Device', 'Device')
        self.assertTrue(
            IDevice.providedBy(self.portal['Device'])
        )
