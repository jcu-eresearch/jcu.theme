import unittest2 as unittest
import doctest
from plone.testing import layered
from jcu.theme import testing

DOCFILES = [
    ('README.txt', 'jcu.theme')
]


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(
            doctest.DocFileSuite(
                docfile,
                package=package,
                optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | \
                            doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS),
            layer=testing.JCU_THEME_FUNCTIONAL_TESTING,
        ) for (docfile, package) in DOCFILES
    ])
    return suite
