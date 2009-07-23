#
# Tests for FAQ types in the PHC
#

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Testing import ZopeTestCase
from Products.PloneHelpCenter.tests import PHCTestCase

try:
    from Products import LinguaPlone
    LINGUAPLONE = True
except ImportError:
    LINGUAPLONE = False
    print "LinguaPlone not found... skipping multilingual tests."
    

class TestMultilingual(PHCTestCase.PHCTestCase):
    """General tests for multilingual objects."""

    def afterSetUp(self):
        PHCTestCase.PHCTestCase.afterSetUp(self)
        self._createFAQ(self.folder.hc.faq, 'f')
        self.enFaq = self.folder.hc.faq.f
        self.enFaq.addTranslation('fr')
        self.frFaq = self.enFaq.getTranslation('fr')
        
    def testIndependentVersions(self):
        versions = ('1.0','2.0','Strange version')
        self.folder.hc.setVersionsVocab(versions)
        enVersions = self.enFaq.getVersionsVocab()
        frVersions = self.frFaq.getVersionsVocab()
        self.assertEqual(enVersions, frVersions)

    def testUniqueDescription(self):
        enDescription = 'An English description'
        frDescription = 'Not English ;)'
        self.enFaq.setDescription(enDescription)
        self.frFaq.setDescription(frDescription)
        self.failIfEqual(self.enFaq.Description(), self.frFaq.Description())
        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    if LINGUAPLONE:
        suite.addTest(makeSuite(TestMultilingual))
    return suite

if __name__ == '__main__':
    framework()
