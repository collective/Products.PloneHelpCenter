#
# Tests for Tutorial types in the PHC
#

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Testing import ZopeTestCase
from Products.PloneHelpCenter.tests import PHCTestCase


class TestTutorial(PHCTestCase.PHCTestCase):
    """General tests for Tutorial Folder and Tutorial objects."""

    def afterSetUp(self):
        PHCTestCase.PHCTestCase.afterSetUp(self)
        self._createTutorial(self.folder.hc.tutorial, 't')
        self.tutorial = self.folder.hc.tutorial.t

    def testInitialSections(self):
        # Test that the default section list is correct.
        self.assertEqual(self.tutorial.getSections(), ('General',))

    def testVersionsonTutorial(self):
        versions = ('1.0','2.0','Strange version')
        self.folder.hc.setVersionsVocab(versions)
        newVersions = self.tutorial.getVersionsVocab()
        self.assertEqual(newVersions, versions)



def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestTutorial))
    return suite

if __name__ == '__main__':
    framework()
