# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import infoporto.push


class InfoportoPushLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        self.loadZCML(package=infoporto.push)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'infoporto.push:default')


INFOPORTO_PUSH_FIXTURE = InfoportoPushLayer()


INFOPORTO_PUSH_INTEGRATION_TESTING = IntegrationTesting(
    bases=(INFOPORTO_PUSH_FIXTURE,),
    name='InfoportoPushLayer:IntegrationTesting'
)


INFOPORTO_PUSH_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(INFOPORTO_PUSH_FIXTURE,),
    name='InfoportoPushLayer:FunctionalTesting'
)


INFOPORTO_PUSH_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        INFOPORTO_PUSH_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='InfoportoPushLayer:AcceptanceTesting'
)
