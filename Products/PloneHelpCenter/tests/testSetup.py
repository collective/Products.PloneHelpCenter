#
# PHC Setup tests
#

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Testing import ZopeTestCase
from AccessControl import Unauthorized
from Products.PloneHelpCenter.tests import PHCTestCase


class TestPortalTypes(PHCTestCase.PHCTestCase):

    def afterSetUp(self):
        self.types = self.portal.portal_types.objectIds()

    def testHelpCenterPortalType(self):
        self.failUnless('HelpCenter' in self.types)

    def testHelpCenterDefinitionType(self):
        self.failUnless('HelpCenterDefinition' in self.types)
        
    def testHelpCenterLinkType(self):
        self.failUnless('HelpCenterLink' in self.types)
        
    def testHelpCenterHowToType(self):
        self.failUnless('HelpCenterHowTo' in self.types)
        
    def testHelpCenterErrorReferenceFolderType(self):
        self.failUnless('HelpCenterErrorReferenceFolder' in self.types)

    def testHelpCenterFaqFolderType(self):
        self.failUnless('HelpCenterFAQFolder' in self.types)

    def testHelpCenterErrorReferenceType(self):
        self.failUnless('HelpCenterErrorReference' in self.types)

    def testHelpCenterTutorialPageType(self):
        self.failUnless('HelpCenterTutorialPage' in self.types)

    def testHelpCenterLeafPageType(self):
        self.failUnless('HelpCenterLeafPage' in self.types)

    def testHelpCenterKnowledgeBase(self):
        self.failUnless('HelpCenterKnowledgeBase' in self.types)

    def testHelpCenterLinkFolderType(self):
        self.failUnless('HelpCenterLinkFolder' in self.types)

    def testHelpCenterTutorialType(self):
        self.failUnless('HelpCenterTutorial' in self.types)

    def testHelpCenterTutorialFolderType(self):
        self.failUnless('HelpCenterTutorialFolder' in self.types)

    def testHelpCenterVideoType(self):
        self.failUnless('HelpCenterInstructionalVideo' in self.types)

    def testHelpCenterVideoFolderType(self):
        self.failUnless('HelpCenterInstructionalVideoFolder' in self.types)

    def testHelpCenterFaqType(self):
        self.failUnless('HelpCenterFAQ' in self.types)

    def testHelpCenterGlossaryType(self):
        self.failUnless('HelpCenterGlossary' in self.types)

    def testHelpCenterHowToFolderType(self):
        self.failUnless('HelpCenterHowToFolder' in self.types)

    def testHelpCenterKnowledgeBase(self):
        self.failUnless('HelpCenterKnowledgeBase' in self.types)


class TestGlobalAllow(PHCTestCase.PHCTestCase):

    def afterSetUp(self):
        pass

    def testCreateHelpCenter(self):
        # Globally allowed
        PHCTestCase.PHCTestCase.afterSetUp(self)
        self.failUnless('hc' in self.folder.objectIds())

    def typeNotGloballyAllowed(self, type):
        try:
            self.folder.invokeFactory(type, id='h')
        except (ValueError, Unauthorized): # diff'nt errors in 2.0 & 2.1
            return True
        else:
            return False

    def testCreateHelpCenterReferenceManual(self):
        self.failIf(self.typeNotGloballyAllowed('HelpCenterReferenceManual'))

    def testHelpCenterKnowledgeBase(self):
        self.failIf(self.typeNotGloballyAllowed('HelpCenterKnowledgeBase'))        

    def testCreateHelpCenterHowto(self):
        self.failUnless(self.typeNotGloballyAllowed('HelpCenterHowTo'))

    def testHelpCenterDefinition(self):
        self.failUnless(self.typeNotGloballyAllowed('HelpCenterDefinition'))
        
    def testHelpCenterLink(self):
        self.failUnless(self.typeNotGloballyAllowed('HelpCenterLink'))
        
    def testHelpCenterErrorReferenceFolder(self):
        self.failUnless(self.typeNotGloballyAllowed('HelpCenterErrorReferenceFolder'))
        
    def testHelpCenterFaqFolder(self):
        self.failUnless(self.typeNotGloballyAllowed('HelpCenterFAQFolder'))
        
    def testHelpCenterErrorReference(self):
        self.failUnless(self.typeNotGloballyAllowed('HelpCenterErrorReference'))
        
    def testHelpCenterTutorialPage(self):
        self.failUnless(self.typeNotGloballyAllowed('HelpCenterTutorialPage'))
        
    def testHelpCenterLinkFolder(self):
        self.failUnless(self.typeNotGloballyAllowed('HelpCenterLinkFolder'))
        
    def testHelpCenterTutorial(self):
        self.failUnless(self.typeNotGloballyAllowed('HelpCenterTutorial'))
        
    def testHelpCenterTutorialFolder(self):
        self.failUnless(self.typeNotGloballyAllowed('HelpCenterTutorialFolder'))
        
    def testHelpCenterFaq(self):
        self.failUnless(self.typeNotGloballyAllowed('HelpCenterFAQ'))
        
    def testHelpCenterGlossary(self):
        self.failUnless(self.typeNotGloballyAllowed('HelpCenterGlossary'))
        
    def testHelpCenterHowToFolder(self):
        self.failUnless(self.typeNotGloballyAllowed('HelpCenterHowToFolder'))


class _TestFolderishContainmentBase(PHCTestCase.PHCTestCase):
    """A base class for holding a bit of common code"""

    def afterSetUp(self):
        PHCTestCase.PHCTestCase.afterSetUp(self)
        self.hc = self.folder.hc

    def checkAllowedContentTypes(self, folderish, typeIdList):
        """Test that folderish folder allows exactly the types
        whose ids are listed in typeIdList"""
        types = folderish.allowedContentTypes()
        self.assertEqual(len(types), len(typeIdList))
        for item in types:
            self.failUnless(item.getId() in typeIdList)


class TestHelpCenterContainment(_TestFolderishContainmentBase):

    def testHelpCenterAllowedContentTypes(self):
        allowed = [
            'HelpCenterFAQFolder',
            'HelpCenterHowToFolder',
            'HelpCenterTutorialFolder',
            'HelpCenterReferenceManualFolder',
            'HelpCenterInstructionalVideoFolder',
            'HelpCenterLinkFolder',
            'HelpCenterErrorReferenceFolder',
            'HelpCenterGlossary',
            'HelpCenterKnowledgeBase',
            'Folder',
        ]
        self.checkAllowedContentTypes(self.hc, allowed)

    def testHelpCenterPrePopulation(self):
        content = self.hc.objectIds()
        initial = [
            'faq',
            'how-to',
            'tutorial',
            'manual',
            # XXX - per the HelpCenter.py initializeArchetype method "Video type is not yet finished"
            # thus, it should not be found in the self.hc objectIds()
            # 'video',
            'error',
            'link',
            'glossary',
        ]
        self.assertEqual(len(content), len(initial))
        for id in initial:
            self.failUnless(id in content)


class TestHowToFolderContainment(_TestFolderishContainmentBase):

    def afterSetUp(self):
        _TestFolderishContainmentBase.afterSetUp(self)
        self.hf = getattr(self.folder.hc, 'how-to')

    def testHowToFolderAllowedContentTypes(self):
        allowed = [
            'HelpCenterHowTo',
        ]
        self.checkAllowedContentTypes(self.hf, allowed)

    def testCreateHowToInHowToFolder(self):
        # Allowed
        self.hf.invokeFactory('HelpCenterHowTo', id='h')
        self.failUnless('h' in self.hf.objectIds())

    def testCreateDocumentInHowToFolder(self):
        # Not allowed
        self.assertRaises(ValueError, self.hf.invokeFactory, 'Document', id='doc')


class TestHelpCenterErrorReferenceFolderContainment(_TestFolderishContainmentBase):

    def afterSetUp(self):
        _TestFolderishContainmentBase.afterSetUp(self)
        self.hf = self.folder.hc.error

    def testErrorReferenceFolderAllowedContentTypes(self):
        allowed = [
            'HelpCenterErrorReference',
        ]
        self.checkAllowedContentTypes(self.hf, allowed)

    def testCreateErrorReferenceInErrorReferenceFolder(self):
        # Allowed
        self.hf.invokeFactory('HelpCenterErrorReference', id='h')
        self.assertEqual(self.hf.objectIds(), ['h'])
    
    def testCreateDocumentInErrorReferenceFolder(self):
        # Not allowed
        self.assertRaises(ValueError, self.hf.invokeFactory, 'Document', id='doc')


class TestHelpCenterFaqFolderContainment(_TestFolderishContainmentBase):

    def afterSetUp(self):
        _TestFolderishContainmentBase.afterSetUp(self)
        self.hf = self.folder.hc.faq

    def testFaqFolderAllowedContentTypes(self):
        allowed = [
            'HelpCenterFAQ',
        ]
        self.checkAllowedContentTypes(self.hf, allowed)

    def testCreateFaqInFaqFolder(self):
        # Allowed
        self.hf.invokeFactory('HelpCenterFAQ', id='h')
        self.assertEqual(self.hf.objectIds(), ['h'])

    def testCreateDocumentInFaqFolder(self):
        # Not allowed
        self.assertRaises(ValueError, self.hf.invokeFactory, 'Document', id='doc')


class TestHelpCenterLinkFolderContainment(_TestFolderishContainmentBase):

    def afterSetUp(self):
        _TestFolderishContainmentBase.afterSetUp(self)
        self.hf = self.folder.hc.link

    def testLinkFolderAllowedContentTypes(self):
        allowed = [
            'HelpCenterLink',
        ]
        self.checkAllowedContentTypes(self.hf, allowed)

    def testCreateLinkInLinkFolder(self):
        # Allowed
        self.hf.invokeFactory('HelpCenterLink', id='h')
        self.assertEqual(self.hf.objectIds(), ['h'])

    def testCreateDocumentInLinkFolder(self):
        # Not allowed
        self.assertRaises(ValueError, self.hf.invokeFactory, 'Document', id='doc')
    

class TestHelpCenterTutorialFolderContainment(_TestFolderishContainmentBase):

    def afterSetUp(self):
        _TestFolderishContainmentBase.afterSetUp(self)
        self.hf = self.folder.hc.tutorial
        
    def testTutorialFolderAllowedContentTypes(self):
        allowed = [
            'HelpCenterTutorial',
        ]
        self.checkAllowedContentTypes(self.hf, allowed)

    def testCreateTutorialInTutorialFolder(self):
        # Allowed
        self.hf.invokeFactory('HelpCenterTutorial', id='h')
        self.assertEqual(self.hf.objectIds(), ['h'])

    def testCreateDocumentInTutorialFolder(self):
        # Not allowed
        self.assertRaises(ValueError, self.hf.invokeFactory, 'Document', id='doc')
    

class TestHelpCenterTutorialContainment(_TestFolderishContainmentBase):

    def afterSetUp(self):
        _TestFolderishContainmentBase.afterSetUp(self)
        self.hf = self.folder.hc.tutorial
        self.hf.invokeFactory('HelpCenterTutorial', id='tf')
        self.tf = self.hf.tf
        
    def testTutorialFolderAllowedContentTypes(self):
        allowed = [
            'Image',
            'File',
            'HelpCenterLeafPage',
        ]
        self.checkAllowedContentTypes(self.tf, allowed)

    def testCreateLeafPageInTutorial(self):
        # Allowed
        self.tf.invokeFactory('HelpCenterLeafPage', id='h')
        self.assertEqual(self.tf.objectIds(), ['h'])

#    XXX Should we test that we can actually add an Image and a File?

    def testCreateDocumentInTutorial(self):
        # Not allowed
        self.assertRaises(ValueError, self.tf.invokeFactory, 'Document', id='doc')
    

class TestHelpCenterGlossaryContainment(_TestFolderishContainmentBase):

    def afterSetUp(self):
        _TestFolderishContainmentBase.afterSetUp(self)
        self.hf = self.folder.hc.glossary
        
    def testGlossaryAllowedContentTypes(self):
        allowed = [
            'HelpCenterDefinition',
        ]
        self.checkAllowedContentTypes(self.hf, allowed)

    def testCreateDefinitionInGlossaryFolder(self):
        # Allowed
        self.hf.invokeFactory('HelpCenterDefinition', id='h')
        self.assertEqual(self.hf.objectIds(), ['h'])

    def testCreateDocumentInGlossaryFolder(self):
        # Not allowed
        self.assertRaises(ValueError, self.hf.invokeFactory, 'Document', id='doc')


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestPortalTypes))
    suite.addTest(makeSuite(TestGlobalAllow))
    suite.addTest(makeSuite(TestHelpCenterContainment))
    suite.addTest(makeSuite(TestHowToFolderContainment))
    suite.addTest(makeSuite(TestHelpCenterErrorReferenceFolderContainment))
    suite.addTest(makeSuite(TestHelpCenterFaqFolderContainment))
    suite.addTest(makeSuite(TestHelpCenterLinkFolderContainment))
    suite.addTest(makeSuite(TestHelpCenterTutorialFolderContainment))
    suite.addTest(makeSuite(TestHelpCenterTutorialContainment))
    suite.addTest(makeSuite(TestHelpCenterGlossaryContainment))
    return suite

if __name__ == '__main__':
    framework()
