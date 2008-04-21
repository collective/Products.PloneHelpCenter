#
# Tests for ErrorReference types in the PHC
#

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Testing import ZopeTestCase
from Products.PloneHelpCenter.tests import PHCTestCase


class TestErrorReference(PHCTestCase.PHCTestCase):
    """General tests for ErrorReference Folder and ErrorReference objects."""

    def afterSetUp(self):
        PHCTestCase.PHCTestCase.afterSetUp(self)
        self._createErrorReference(self.folder.hc.error, 'e')
        self.errorRef = self.folder.hc.error.e

    def testInitialTitle(self):
        # Test that the default title is correct.
        self.assertEqual(self.errorRef.title, 'Default Testing Title')

    def testInitialDescription(self):
        # Test that the default description is correct.
        self.assertEqual(self.errorRef.Description(), 'An error reference for unit tests.')

    def testInitialSections(self):
        # Test that the default section list is correct.
        self.assertEqual(self.errorRef.getSections(), ('General',))

    def testInitialVersions(self):
        # Test that the default version list is correct.
        self.assertEqual(self.errorRef.getVersions(), ('Version 2.0',))

    def testVersionsonErrorReference(self):
        versions = ('1.0','2.0','Strange version')
        self.folder.hc.setVersionsVocab(versions)
        newVersions = self.errorRef.getVersionsVocab()
        self.assertEqual(newVersions, versions)



def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestErrorReference))
    return suite

if __name__ == '__main__':
    framework()
