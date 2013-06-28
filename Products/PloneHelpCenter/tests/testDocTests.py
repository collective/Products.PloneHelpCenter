"""PloneHelpCenter functional doctests.  This module collects all *.txt
files in the tests directory and runs them. (stolen from Plone)
"""

import doctest
import glob
import os
import unittest

from App.Common import package_home
from Testing.ZopeTestCase import FunctionalDocFileSuite as Suite

from Products.PloneHelpCenter.config import GLOBALS

# Load products
from Products.PloneHelpCenter.tests.PHCTestCase import PHCFunctionalTestCase

OPTIONFLAGS = (doctest.REPORT_ONLY_FIRST_FAILURE |
               doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE)


def list_doctests():
    home = package_home(GLOBALS)
    return [filename for filename in
            glob.glob(os.path.sep.join([home, 'tests', '*.txt']))]


def test_suite():
    filenames = list_doctests()

    return unittest.TestSuite(
        [Suite(os.path.basename(filename),
               optionflags=OPTIONFLAGS,
               package='Products.PloneHelpCenter.tests',
               test_class=PHCFunctionalTestCase)
         for filename in filenames]
        )
