# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import collective.contentaudit


class CollectiveContentauditLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=collective.contentaudit)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.contentaudit:default')


COLLECTIVE_CONTENTAUDIT_FIXTURE = CollectiveContentauditLayer()


COLLECTIVE_CONTENTAUDIT_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_CONTENTAUDIT_FIXTURE,),
    name='CollectiveContentauditLayer:IntegrationTesting'
)


COLLECTIVE_CONTENTAUDIT_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_CONTENTAUDIT_FIXTURE,),
    name='CollectiveContentauditLayer:FunctionalTesting'
)


COLLECTIVE_CONTENTAUDIT_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_CONTENTAUDIT_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='CollectiveContentauditLayer:AcceptanceTesting'
)
