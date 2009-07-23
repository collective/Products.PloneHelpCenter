#
# Tests for workflow and permissions in the PHC
#

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Products.PloneTestCase.PloneTestCase import default_user

if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Testing import ZopeTestCase
from Products.PloneHelpCenter.tests import PHCTestCase


class TestWorkflow(PHCTestCase.PHCTestCase):
    """Tests for workflow specific issues in the PHC."""

    def afterSetUp(self):
        PHCTestCase.PHCTestCase.afterSetUp(self)
        pm = self.portal.portal_membership
        pm.addMember( 'test_reviewer', 'pw', ['Member', 'Reviewer'], [] )
        pm.addMember( 'test_manager', 'pw', ['Member', 'Manager'], [] )

    def _publishContent(self, item):
        """Moves content created by the default user to the published state."""
        self.portal.portal_workflow.doActionFor(item, 'submit')
        self.login('test_reviewer')
        self.portal.portal_workflow.doActionFor(item, 'publish')
        self.login(default_user)

    def _checkReviewState(self, item, state):
        """Checks that the content item's review_state is equal to state."""
        itemState = self.portal.portal_workflow.getInfoFor(item, 'review_state')
        self.assertEqual(itemState, state)

    # Next several tests: owners can edit content even after it's published
    
    def testEditPublishedHowto(self):
        newBody = 'Changed to this content while published.'
        howto = self._createHowto(getattr(self.folder.hc, 'how-to'), 'howto1')
        self._publishContent(howto)
        howto.edit(text_format='plain', text=newBody)
        self.assertEqual(howto.getRawText(), newBody)

    def testEditPublishedTutorial(self):
        newDescription = 'New Description.'
        tutorial = self._createTutorial(self.folder.hc.tutorial, 'tut1')
        self._publishContent(tutorial)
        tutorial.edit(description=newDescription)
        self.assertEqual(tutorial.Description(), newDescription)
        tutorial.invokeFactory('HelpCenterLeafPage', 'newPage')
        page = getattr(tutorial, 'newPage')
        page.setTitle('New Page')
        page.setDescription('A tutorial page added after tutorial was published')
        page.setText=('')
        self.assertEqual(tutorial.newPage.Title(), 'New Page')
        
    def testEditPublishedTutorialPage(self):
        # Edit a page on a tutorial that has been published.
        newDescription = 'New Description.'
        tutorial = self._createTutorial(self.folder.hc.tutorial, 'tut1')
        tutorial.invokeFactory('HelpCenterLeafPage', 'newPage')
        page = getattr(tutorial, 'newPage')
        page.setTitle('New Page')
        page.setDescription('A tutorial page added after tutorial was published')
        page.setText('')
        self._publishContent(tutorial)
        tutorial.edit(description=newDescription)
        tutorial.newPage.edit(description=newDescription)
        self.assertEqual(tutorial.newPage.Description(), newDescription)

    def testEditPublishedFaq(self):
        newDescription = 'New Description.'
        faq = self._createFAQ(self.folder.hc.faq, 'faq')
        self._publishContent(faq)
        faq.edit(description=newDescription)
        self.assertEqual(faq.Description(), newDescription)

    def testEditPublishedLink(self):
        newUrl = 'http://www.trizpug.org/'
        link = self._createLink(self.folder.hc.link, 'link')
        self._publishContent(link)
        link.edit(url=newUrl)
        self.assertEqual(link.getUrl(), newUrl)

    def testEditPublishedErrorReference(self):
        newBody = 'Changed!'
        errorRef = self._createErrorReference(self.folder.hc.error, 'er')
        self._publishContent(errorRef)
        errorRef.edit(text=newBody)
        self.assertEqual(errorRef.getRawText(), newBody)

    def testEditPublishedDef(self):
        newDefinition = 'Explicit is better than implicit'
        definition = self._createDefinition(self.folder.hc.glossary, 'def')
        self._publishContent(definition)
        definition.edit(description=newDefinition)
        self.assertEqual(definition.Description(), newDefinition)

    # Test a couple of types to make sure that Owners can edit pending
    # and obsolete content, too.

    def testEditPendingHowto(self):
        newBody = 'Changed to this content while published.'
        howto = self._createHowto(getattr(self.folder.hc, 'how-to'), 'howto1')
        self.portal.portal_workflow.doActionFor(howto, 'submit')
        howto.edit(text_format='plain', text=newBody)
        self.assertEqual(howto.getRawText(), newBody)

    def testEditObsoleteHowto(self):
        newBody = 'Changed to this content while published.'
        howto = self._createHowto(getattr(self.folder.hc, 'how-to'), 'howto1')
        self.portal.portal_workflow.doActionFor(howto, 'mark_obsolete')
        howto.edit(text_format='plain', text=newBody)
        self.assertEqual(howto.getRawText(), newBody)
        

    # Next several tests: owners can obsolete their own content at any point

    def testOwnerObsoletesHowto(self):
        howto = self._createHowto(getattr(self.folder.hc, 'how-to'), 'howto1')
        self._publishContent(howto)
        self.portal.portal_workflow.doActionFor(howto, 'mark_obsolete')
        self._checkReviewState(howto, 'obsolete')

    def testOwnerObsoletesTutorial(self):
        tutorial = self._createTutorial(self.folder.hc.tutorial, 'tut1')
        self._publishContent(tutorial)
        self.portal.portal_workflow.doActionFor(tutorial, 'mark_obsolete')
        self._checkReviewState(tutorial, 'obsolete')

    def testOwnerObsoletesFAQ(self):
        faq = self._createFAQ(self.folder.hc.faq, 'faq1')
        self._publishContent(faq)
        self.portal.portal_workflow.doActionFor(faq, 'mark_obsolete')
        self._checkReviewState(faq, 'obsolete')

    def testOwnerObsoletesLink(self):
        link = self._createLink(self.folder.hc.link, 'link1')
        self._publishContent(link)
        self.portal.portal_workflow.doActionFor(link, 'mark_obsolete')
        self._checkReviewState(link, 'obsolete')

    def testOwnerObsoletesErrorReference(self):
        errorRef = self._createErrorReference(self.folder.hc.error, 'er')
        self._publishContent(errorRef)
        self.portal.portal_workflow.doActionFor(errorRef, 'mark_obsolete')
        self._checkReviewState(errorRef, 'obsolete')

    def testOwnerObsoletesDefinition(self):
        definition = self._createDefinition(self.folder.hc.glossary, 'd')
        self._publishContent(definition)
        self.portal.portal_workflow.doActionFor(definition, 'mark_obsolete')
        self._checkReviewState(definition, 'obsolete')

    def testOwnerObsoletesPendingHowto(self):
        howto = self._createHowto(getattr(self.folder.hc, 'how-to'), 'howto1')
        self.portal.portal_workflow.doActionFor(howto, 'submit')
        self.portal.portal_workflow.doActionFor(howto, 'mark_obsolete')
        self._checkReviewState(howto, 'obsolete')

    def testOwnerObsoletesPendingTutorial(self):
        tutorial = self._createTutorial(self.folder.hc.tutorial, 'tut1')
        self.portal.portal_workflow.doActionFor(tutorial, 'submit')
        self.portal.portal_workflow.doActionFor(tutorial, 'mark_obsolete')
        self._checkReviewState(tutorial, 'obsolete')

    def testOwnerObsoletesPendingFAQ(self):
        faq = self._createFAQ(self.folder.hc.faq, 'faq1')
        self.portal.portal_workflow.doActionFor(faq, 'submit')
        self.portal.portal_workflow.doActionFor(faq, 'mark_obsolete')
        self._checkReviewState(faq, 'obsolete')

    def testOwnerObsoletesPendingLink(self):
        link = self._createLink(self.folder.hc.link, 'link1')
        self.portal.portal_workflow.doActionFor(link, 'submit')
        self.portal.portal_workflow.doActionFor(link, 'mark_obsolete')
        self._checkReviewState(link, 'obsolete')

    def testOwnerObsoletesPendingErrorReference(self):
        errorRef = self._createErrorReference(self.folder.hc.error, 'er')
        self.portal.portal_workflow.doActionFor(errorRef, 'submit')
        self.portal.portal_workflow.doActionFor(errorRef, 'mark_obsolete')
        self._checkReviewState(errorRef, 'obsolete')

    def testOwnerObsoletesPendingDefinition(self):
        definition = self._createDefinition(self.folder.hc.glossary, 'd')
        self.portal.portal_workflow.doActionFor(definition, 'submit')
        self.portal.portal_workflow.doActionFor(definition, 'mark_obsolete')
        self._checkReviewState(definition, 'obsolete')

    def testOwnerObsoletesInProgressHowto(self):
        howto = self._createHowto(getattr(self.folder.hc, 'how-to'), 'howto1')
        self.portal.portal_workflow.doActionFor(howto, 'mark_obsolete')
        self._checkReviewState(howto, 'obsolete')

    def testOwnerObsoletesInProgressTutorial(self):
        tutorial = self._createTutorial(self.folder.hc.tutorial, 'tut1')
        self.portal.portal_workflow.doActionFor(tutorial, 'mark_obsolete')
        self._checkReviewState(tutorial, 'obsolete')

    def testOwnerObsoletesInProgressFAQ(self):
        faq = self._createFAQ(self.folder.hc.faq, 'faq1')
        self.portal.portal_workflow.doActionFor(faq, 'mark_obsolete')
        self._checkReviewState(faq, 'obsolete')

    def testOwnerObsoletesInProgressLink(self):
        link = self._createLink(self.folder.hc.link, 'link1')
        self.portal.portal_workflow.doActionFor(link, 'mark_obsolete')
        self._checkReviewState(link, 'obsolete')

    def testOwnerObsoletesInProgressErrorReference(self):
        errorRef = self._createErrorReference(self.folder.hc.error, 'er')
        self.portal.portal_workflow.doActionFor(errorRef, 'mark_obsolete')
        self._checkReviewState(errorRef, 'obsolete')

    def testOwnerObsoletesInProgressDefinition(self):
        definition = self._createDefinition(self.folder.hc.glossary, 'd')
        self.portal.portal_workflow.doActionFor(definition, 'mark_obsolete')
        self._checkReviewState(definition, 'obsolete')

    # Next several tests: reviewers can obsolete any pending content

    def testReviewerObsoletesHowto(self):
        howto = self._createHowto(getattr(self.folder.hc, 'how-to'), 'howto1')
        self._publishContent(howto)
        self.login('test_reviewer')
        self.portal.portal_workflow.doActionFor(howto, 'mark_obsolete')
        self._checkReviewState(howto, 'obsolete')

    def testReviewerObsoletesTutorial(self):
        tutorial = self._createTutorial(self.folder.hc.tutorial, 'tut1')
        self._publishContent(tutorial)
        self.login('test_reviewer')
        self.portal.portal_workflow.doActionFor(tutorial, 'mark_obsolete')
        self._checkReviewState(tutorial, 'obsolete')

    def testReviewerObsoletesFAQ(self):
        faq = self._createFAQ(self.folder.hc.faq, 'faq1')
        self._publishContent(faq)
        self.login('test_reviewer')
        self.portal.portal_workflow.doActionFor(faq, 'mark_obsolete')
        self._checkReviewState(faq, 'obsolete')

    def testReviewerObsoletesLink(self):
        link = self._createLink(self.folder.hc.link, 'link1')
        self._publishContent(link)
        self.login('test_reviewer')
        self.portal.portal_workflow.doActionFor(link, 'mark_obsolete')
        self._checkReviewState(link, 'obsolete')

    def testReviewerObsoletesErrorReference(self):
        errorRef = self._createErrorReference(self.folder.hc.error, 'er')
        self._publishContent(errorRef)
        self.login('test_reviewer')
        self.portal.portal_workflow.doActionFor(errorRef, 'mark_obsolete')
        self._checkReviewState(errorRef, 'obsolete')

    def testReviewerObsoletesDefinition(self):
        definition = self._createDefinition(self.folder.hc.glossary, 'd')
        self._publishContent(definition)
        self.login('test_reviewer')
        self.portal.portal_workflow.doActionFor(definition, 'mark_obsolete')
        self._checkReviewState(definition, 'obsolete')

    # Next several tests: non-reviewers who have the 'Review portal content'
    # permission, such as a manager, can obsolete any pending content
    # XXX: Rather bogus to use a manager here...probably need a normal member
    # who has just that permisson.

    def testManagerObsoletesHowto(self):
        howto = self._createHowto(getattr(self.folder.hc, 'how-to'), 'howto1')
        self._publishContent(howto)
        self.login('test_manager')
        self.portal.portal_workflow.doActionFor(howto, 'mark_obsolete')
        self._checkReviewState(howto, 'obsolete')

    def testManagerObsoletesTutorial(self):
        tutorial = self._createTutorial(self.folder.hc.tutorial, 'tut1')
        self._publishContent(tutorial)
        self.login('test_manager')
        self.portal.portal_workflow.doActionFor(tutorial, 'mark_obsolete')
        self._checkReviewState(tutorial, 'obsolete')

    def testManagerObsoletesFAQ(self):
        faq = self._createFAQ(self.folder.hc.faq, 'faq1')
        self._publishContent(faq)
        self.login('test_manager')
        self.portal.portal_workflow.doActionFor(faq, 'mark_obsolete')
        self._checkReviewState(faq, 'obsolete')

    def testManagerObsoletesLink(self):
        link = self._createLink(self.folder.hc.link, 'link1')
        self._publishContent(link)
        self.login('test_manager')
        self.portal.portal_workflow.doActionFor(link, 'mark_obsolete')
        self._checkReviewState(link, 'obsolete')

    def testManagerObsoletesErrorReference(self):
        errorRef = self._createErrorReference(self.folder.hc.error, 'er')
        self._publishContent(errorRef)
        self.login('test_manager')
        self.portal.portal_workflow.doActionFor(errorRef, 'mark_obsolete')
        self._checkReviewState(errorRef, 'obsolete')

    def testManagerObsoletesDefinition(self):
        definition = self._createDefinition(self.folder.hc.glossary, 'd')
        self._publishContent(definition)
        self.login('test_manager')
        self.portal.portal_workflow.doActionFor(definition, 'mark_obsolete')
        self._checkReviewState(definition, 'obsolete')
    

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestWorkflow))
    return suite

if __name__ == '__main__':
    framework()
