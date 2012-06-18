import unittest2 as unittest
from jcu.theme import setuphandlers
from jcu.theme.testing import JCU_THEME_FUNCTIONAL_TESTING


class IntegrationTest(unittest.TestCase):

    layer = JCU_THEME_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_cas_installation(self):
        """Test to ensure CAS plugin and settings were configured."""
        self.assertIn('cas', self.portal.acl_users)

        cas = self.portal.acl_users.cas
        self.assertIn('secure.jcu', cas.login_url)
        self.assertIn('secure.jcu', cas.logout_url)
        self.assertIn('secure.jcu', cas.validate_url)

        from plone.registry.interfaces import IRegistry
        from zope.component import getUtility
        from collective.castle.interfaces import ICAS4PASPluginSchema
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ICAS4PASPluginSchema)

        self.assertIn('secure.jcu', settings.login_url)
        self.assertIn('secure.jcu', settings.logout_url)
        self.assertIn('secure.jcu', settings.validate_url)
        self.assertTrue(settings.users_require_role)


    def test_cas_login_url(self):
        self.assertEqual(self.portal.restrictedTraverse('castle_login_url')(),
                         'https://cas.secure.jcu.edu.au/cas/login?service=http%3A%2F%2Fnohost%2Fplone%2Flogged_in%3Fcame_from%3Dhttp%253A%252F%252Fnohost')

    def test_cas_sso_logout(self):
        logout = self.portal.restrictedTraverse('castle_logout')
        logout.request.SESSION = {'__ac': 'foobar'}
        logout()

        #Session cookie is gone and redirection is happening
        self.assertIsNone(logout.request.SESSION['__ac'])
        self.assertEqual(logout.request.response.cookies['__ac']['value'],
                         'deleted')
        self.assertEqual(logout.request.response.status, 302)
        self.assertEqual(logout.request.response['location'],
                         'https://cas.secure.jcu.edu.au/cas/logout?url=http%3A//nohost/plone')





