import unittest2 as unittest
from jcu.theme import setuphandlers
from jcu.theme.testing import JCU_THEME_FUNCTIONAL_TESTING


class DummyContext:

    datafile_value = None

    def __init__(self, datafile_value=None):
        self.datafile_value = datafile_value

    def readDataFile(self, filename):
        return self.datafile_value

class DummySite:
    messages = []
    def plone_log(self, message):
        self.messages.append(message)

class IntegrationTest(unittest.TestCase):

    layer = JCU_THEME_FUNCTIONAL_TESTING

    def test_no_variousdottxt(self):
        """Check that nothing happens when a 'various.txt' file isn't present.

        This function would see errors happen with the fake context otherwise.
        """
        setup_result = setuphandlers.setupVarious(DummyContext(None))
        self.assertIsNone(setup_result)

    def test_borked_configuration(self):
        """This test looks for error messages from the setuphandler config."""
        expected_errors = ['Could not reconfigure MailHost for queuing.',
                           'Could not configure reCAPTCHA keys.',
                           'Could not configure LDAP plugin settings.',
                          ]
        dummysite = DummySite()

        try:
            setuphandlers.setupVarious(DummyContext('foo'), dummysite)
        except AttributeError:
            pass

        self.assertEqual(dummysite.messages, expected_errors)

    def test_upgrades(self):
        portal = self.layer['portal']
        upgrades = ['actions', 'mailhost', 'registry']

        for upgrade in upgrades:
            upgrade_function = getattr(setuphandlers, 'upgrade_%s' % upgrade)
            self.assertIsNotNone(upgrade_function(portal, return_values=True))

