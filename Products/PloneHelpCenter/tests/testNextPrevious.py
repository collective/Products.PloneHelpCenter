from plone.app.layout.nextprevious.interfaces import INextPreviousProvider
from Products.PloneHelpCenter.tests.PHCTestCase import PHCTestCase

class TestNextPrevious(PHCTestCase):
    """PHC use cases and tests for next/previous navigation
    """
     
    def afterSetUp(self):
        super(TestNextPrevious, self).afterSetUp()
        self.hc = self.folder.hc
        self.populateSite()

    # set up a lot of content - can be reused in each (sub)test
    def populateSite(self):
        self.setRoles(['Manager'])
        self.hc.invokeFactory('HelpCenterReferenceManualFolder', 'manual_folder')
        manual_folder = getattr(self.hc, 'manual_folder')
        manual_folder.invokeFactory('HelpCenterReferenceManual', 'manual')
        manual = getattr(manual_folder, 'manual')
        for section_counter in range(1, 4):
            manual.invokeFactory('HelpCenterReferenceManualSection',
                                 'section%d' % section_counter)
            section = getattr(manual, 'section%d' % section_counter)
            for leaf_page_counter in range(1, 4):
                section.invokeFactory('HelpCenterLeafPage', 
                                      'page%d' % leaf_page_counter)
        self.setRoles(['Member'])
 
    def testNextPreviousItems(self):
        manual = self.hc.manual_folder.manual
        section1  = manual.section1
        section2  = manual.section2
        section3  = manual.section3
        
        # set up the adapter for the sec2
        adapter = INextPreviousProvider(section2)

        # test the next item of page 2
        next = adapter.getNextItem(section2.page2)
        self.failUnlessEqual(next["id"], 'page3')
        
        # test the previous item of page2
        previous = adapter.getPreviousItem(section2.page2)
        self.failUnlessEqual(previous["id"], 'page1')
        
        # page 1 of sec 2 should have the 1st section as previous item
        previous = adapter.getPreviousItem(section2.page1)
        self.failUnlessEqual(previous["id"], 'section1')

        # page 3 of sec 2 should have the 3rd section as next item
        next = adapter.getNextItem(section2.page3)
        self.failUnlessEqual(next["id"], 'section3')

        adapter = INextPreviousProvider(manual)
        # sec 2 should have the 3rd section as next item
        next = adapter.getNextItem(section2)
        self.failUnlessEqual(next["id"], 'section3')

        # sec 2 should have the 1st section as prev item
        previous = adapter.getPreviousItem(section2)
        self.failUnlessEqual(previous["id"], 'section1')

        # sec 1 should have no previous item
        previous = adapter.getPreviousItem(section1)
        self.failUnlessEqual(previous, None)

        # sec 3 should have no next item
        next = adapter.getNextItem(section3)
        self.failUnlessEqual(next, None)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestNextPrevious))
    return suite
