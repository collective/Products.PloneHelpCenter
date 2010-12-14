from Products.PloneHelpCenter.tests.PHCTestCase import PHCFunctionalTestCase
from Products.PloneHelpCenter.tests import CustomSetup
from Products.PloneHelpCenter.tests import Data


class TestHelpCenterView(PHCFunctionalTestCase):
    """Tests for the Help Center View."""

    def afterSetUp(self):
        super(TestHelpCenterView, self).afterSetUp()
        CustomSetup.CreateTestData(self, self.portal)
        self.hc = getattr(self.portal, Data.Hc.Id)

    def testGetSubTopicsSorting(self):
        """getSubTopics() returns the subtopics in the order defined
        in the PHC or the subfolder.
        """
        hc_view = self.hc.restrictedTraverse('@@hc_view')
        subtopics = hc_view.getSubTopics('Topic2')

        subtopic_titles = [s['title'] for s in subtopics]
        self.assertEqual(subtopic_titles, ['Section Z', 'Section A'])

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestHelpCenterView))
    return suite
