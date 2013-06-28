#
# Tests for Link types in the PHC
#

from Products.PloneHelpCenter.tests import PHCTestCase


class TestLink(PHCTestCase.PHCTestCase):
    """General tests for Link Folder and Link objects."""

    def afterSetUp(self):
        PHCTestCase.PHCTestCase.afterSetUp(self)
        self._createLink(self.folder.hc.link, 'l')
        self.link = self.folder.hc.link.l

    def testInitialSections(self):
        # Test that the default section list is correct.
        self.assertEqual(self.link.getSections(), ('General',))

    def testVersionsonLink(self):
        versions = ('1.0', '2.0', 'Strange version')
        self.folder.hc.setVersionsVocab(versions)
        newVersions = self.link.getVersionsVocab()
        self.assertEqual(newVersions, versions)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestLink))
    return suite
