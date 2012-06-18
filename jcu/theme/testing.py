from plone.app.testing import PloneSandboxLayer, PLONE_FIXTURE, login, logout
from plone.app.testing import IntegrationTesting, FunctionalTesting
from plone.app.testing.interfaces import SITE_OWNER_NAME
from plone.testing.z2 import installProduct


class JCUThemeLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        installProduct(app, 'Products.CAS4PAS')
        # Load ZCML
        import jcu.theme
        self.loadZCML(package=jcu.theme, context=configurationContext)
        self.loadZCML('overrides.zcml', package=jcu.theme, context=configurationContext)

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'jcu.theme:default')
        login(portal, SITE_OWNER_NAME)
        portal.invokeFactory('Document', 'front-page', title=u"My front page!")
        portal.setDefaultPage('front-page')
        portal.invokeFactory('Folder', 'Members', title=u"Users")
        logout()


JCU_THEME_FIXTURE = JCUThemeLayer()
JCU_THEME_INTEGRATION_TESTING = IntegrationTesting(
    bases=(JCU_THEME_FIXTURE,),
    name="JCUTheme:Integration"
)
JCU_THEME_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(JCU_THEME_FIXTURE,),
    name="JCUTheme:Functional"
)
