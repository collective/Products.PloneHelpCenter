#
# Tests for Howto types in the PHC
#

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Testing import ZopeTestCase
from Products.PloneHelpCenter.tests import PHCTestCase


class TestHowto(PHCTestCase.PHCTestCase):
    """General tests for Howto folder and HOWTO objects."""

    def afterSetUp(self):
        PHCTestCase.PHCTestCase.afterSetUp(self)
        self._createHowto( getattr(self.folder.hc, 'how-to'), 'howto1' )
        self.howto = getattr(self.folder.hc, 'how-to').howto1

    def testVersionsHowto(self):
        versions = ('1.0','2.0','Strange version')
        self.folder.hc.setVersionsVocab(versions)
        newVersions = self.howto.getVersionsVocab()
        self.assertEqual(newVersions, versions)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestHowto))
    return suite

if __name__ == '__main__':
    framework()
