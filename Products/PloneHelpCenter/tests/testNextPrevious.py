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

        # place an image and a file inside sec 2
        # these types mustn't show up in the next/previous links
        manual.section2.invokeFactory('Image', 'image')
        manual.section2.invokeFactory('File', 'file')
                
        self.setRoles(['Member'])
 
    def testNextPreviousItems(self):
        manual = self.hc.manual_folder.manual
        section1  = manual.section1
        section2  = manual.section2
        section3  = manual.section3
        
        # set up the adapter for the sec2
        adapter = INextPreviousProvider(section2)

        # forwards from 2.2.
        next = adapter.getNextItem(section2.page2)
        self.failUnlessEqual(next["title"], '2.3. ')
        
        # backwards
        previous = adapter.getPreviousItem(section2.page2)
        self.failUnlessEqual(previous["title"], '2.1. ')
        
        # backwards from 2.1.
        previous = adapter.getPreviousItem(section2.page1)
        self.failUnlessEqual(previous["title"], '2. ')

        # forwards from 2.3., ignoring the image and the file
        next = adapter.getNextItem(section2.page3)
        self.failUnlessEqual(next["title"], '3. ')

        adapter = INextPreviousProvider(manual)
        # forwards from 2.
        next = adapter.getNextItem(section2)
        self.failUnlessEqual(next["title"], '2.1. ')

        # backwards
        previous = adapter.getPreviousItem(section2)
        self.failUnlessEqual(previous["title"], '1.3. ')

        # 1. has no previous item
        previous = adapter.getPreviousItem(section1)
        self.failUnlessEqual(previous, None)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestNextPrevious))
    return suite
