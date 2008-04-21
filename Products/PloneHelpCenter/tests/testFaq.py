#
# Tests for FAQ types in the PHC
#

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Testing import ZopeTestCase
from Products.PloneHelpCenter.tests import PHCTestCase


class TestFaq(PHCTestCase.PHCTestCase):
    """General tests for FAQ Folder and FAQ objects."""

    def afterSetUp(self):
        PHCTestCase.PHCTestCase.afterSetUp(self)
        self._createFAQ(self.folder.hc.faq, 'f')
        self.faq = self.folder.hc.faq.f

    def testInitialSections(self):
        # Test that the default section list is correct.
        self.assertEqual(self.faq.getSections(), ('General',))

    def testVersionsonFaq(self):
        versions = ('1.0','2.0','Strange version')
        self.folder.hc.setVersionsVocab(versions)
        newVersions = self.faq.getVersionsVocab()
        self.assertEqual(newVersions, versions)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestFaq))
    return suite

if __name__ == '__main__':
    framework()
