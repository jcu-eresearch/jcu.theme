import unittest
import doctest

from Testing import ZopeTestCase as ztc
from jcu.theme.tests import base


def test_suite():
    return unittest.TestSuite([

        # Integration tests that use PloneTestCase
        ztc.ZopeDocFileSuite(
            'THEMING.txt', package='jcu.theme',
            test_class=base.FunctionalTestCase,
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | \
                        doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
        ),

    ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
