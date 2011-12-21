import unittest2 as unittest
from jcu.theme.testing import JCU_THEME_FUNCTIONAL_TESTING

class IntegrationTest(unittest.TestCase):

    layer = JCU_THEME_FUNCTIONAL_TESTING

    def test_theme_for_context(self):
        from jcu.theme.browser.layout import getThemeForContext

        fake_context = 'Not a context - this is a string'
        result = getThemeForContext(fake_context)

        self.assertEqual(result['context'], None)
        self.assertEqual(result['theme_name'], '')


