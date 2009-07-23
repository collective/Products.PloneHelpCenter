from Testing import ZopeTestCase
from Products.CMFPlone.tests import PloneTestCase

from Products.Five import fiveconfigure
from Products.Five import zcml
from Products.PloneTestCase.layer import onsetup
import Products.PloneHelpCenter
from Products.PloneHelpCenter.config import ADD_CENTER_PERMISSION, \
  ADD_HELP_AREA_PERMISSION

# from Products.Five.testbrowser import Browser

ZopeTestCase.installProduct('PloneHelpCenter')

@onsetup
def setup_product():
    fiveconfigure.debug_mode = True
    zcml.load_config('configure.zcml', Products.PloneHelpCenter)
    fiveconfigure.debug_mode = False

setup_product()
PloneTestCase.setupPloneSite(products=['PloneHelpCenter'])


class PHCTestCase(PloneTestCase.PloneTestCase):

    defaultTitle = 'Default Testing Title'
    defaultVersions = ( 'Version 1.0', 'Version 2.0', 'Different Version1.0', )
    defaultBodyRst = """
    Bogus reST body
    ===============
    
    Here's fake body content for unit tests.
    
    * Looks like a list.
    * Smells like a list.
    * It's a list!
    
    Final content after the list.
    """

    class Session(dict):
        def set(self, key, value):
            self[key] = value

    def _setup(self):
        PloneTestCase.PloneTestCase._setup(self)
        self.app.REQUEST['SESSION'] = self.Session()

    def afterSetUp(self):
        self.portal.manage_permission(ADD_CENTER_PERMISSION,
                                      ['Manager', 'Owner'])
        self.portal.manage_permission(ADD_HELP_AREA_PERMISSION,
                                      ['Manager', 'Owner'])
        self._createHelpCenter(self.folder)

    def _createHelpCenter(self, folder, id='hc', title=defaultTitle, versions=defaultVersions):
        """Creates and returns a refence to a PHC HelpCenter.
        This method publishes a HelpCenter instance under folder.  It fills in
        all of the standard properties."""
        folder.invokeFactory('HelpCenter', id)
        helpCenter = getattr(folder, id)
        helpCenter.setTitle(title)
        helpCenter.setDescription('A HelpCenter instance for unit tests.')
        helpCenter.setVersionsVocab(versions)
        self.portal.portal_workflow.doActionFor(helpCenter, 'submit')
        return helpCenter

    def _createHowto(self, howtoFolder, id, title=defaultTitle):
        """Creates and returns a refence to a PHC Howto.
        This method creates a Howto instance under a folder.  It fills in
        all of the standard properties."""
        howtoFolder.invokeFactory('HelpCenterHowTo', id)
        howto = getattr(howtoFolder, id)
        howto.setTitle(title)
        howto.setDescription('A PHC Howto for unit tests.')
        howto.setText(self.defaultBodyRst) 
        howto.setVersions( ('Version 2.0',) )
        howto.setSections( ('General',) )
        self.portal.plone_utils.editMetadata(howto, format='text/x-rst')
        return howto

    def _createTutorial(self, tutorialFolder, id, title=defaultTitle, numPages=2):
        """Creates and returns a reference to a PHC Tutorial.
        This method creates a Tutorial instance under a folder.  It fills in
        all of the standard properties."""
        tutorialFolder.invokeFactory('HelpCenterTutorial', id)
        tutorial = getattr(tutorialFolder, id)
        tutorial.setTitle(title)
        tutorial.setDescription('A PHC Tutorial for unit tests.')
        tutorial.setVersions( ('Version 2.0',) )
        tutorial.setSections( ('General',) )
        # attach pages
        for i in range(numPages):
            pageNum = i + 1
            id='page%d' % pageNum
            tutorial.invokeFactory('HelpCenterLeafPage', id)
            newPage = getattr(tutorial, id)
            newPage.setTitle('Test Tutorial Page %d' % pageNum)
            newPage.setDescription('A PHC Tutorial Page (%d) for unit tests.' % pageNum)
            newPage.setText(self.defaultBodyRst)
            self.portal.plone_utils.editMetadata(newPage,format='text/x-rst')
        return tutorial
                                   
    def _createFAQ(self, faqFolder, id, title=defaultTitle):
        """Creates and returns a reference to a PHC FAQ.
        This method creates an FAQ instance under a folder.  It fills in
        all of the standard properties."""
        faqFolder.invokeFactory('HelpCenterFAQ', id=id)
        faq = getattr(faqFolder, id)
        faq.setTitle=(title)
        faq.setDescription('An FAQ for unit tests.  Did you know that this field is supposed to be the questionfaq.set?')
        faq.setText('No one knows; it is one of the great mysteries.')
        faq.setVersions( ('Version 2.0',) )
        faq.setSections( ('General',) )
        self.portal.plone_utils.editMetadata(faq, format='text/plain')
        return faq

    def _createLink(self, linkFolder, id, title=defaultTitle):
        linkFolder.invokeFactory('HelpCenterLink', id)
        link = getattr(linkFolder, id)
        link.setTitle( title )
        link.setDescription( 'A Link for unit tests.' )
        link.setUrl('http://www.plone.org/')
        link.setVersions( ('Version 2.0',) )
        link.setSections( ('General',) )
        return link

    def _createErrorReference(self, errorRefFolder, id, title=defaultTitle):
        errorRefFolder.invokeFactory('HelpCenterErrorReference', id)
        errorRef = getattr(errorRefFolder, id)
        errorRef.setTitle( title )
        errorRef.setDescription( 'An error reference for unit tests.' )
        errorRef.setText( self.defaultBodyRst )
        errorRef.setVersions( ('Version 2.0',) )
        errorRef.setSections( ('General',) )
        self.portal.plone_utils.editMetadata(errorRef, format='text/x-rst')
        return errorRef

    def _createDefinition(self, glossaryFolder, id, title=defaultTitle):
        glossaryFolder.invokeFactory('HelpCenterDefinition', id)
        definition = getattr(glossaryFolder, id)
        definition.setTitle(title)
        definition.setDescription('A definition for unit tests.')
        definition.setVersions( ('Version 2.0',) )
        definition.setSections( ('General',) )
        return definition

    def _createReferenceManual(self, glossaryFolder, id, title=defaultTitle):
        pass

    def _createVideo(self, videoFolder, id, title=defaultTitle):
        pass

class PHCFunctionalTestCase(PloneTestCase.FunctionalTestCase):
    
    class Session(dict):
        def set(self, key, value):
            self[key] = value

    def _setup(self):
        PloneTestCase.FunctionalTestCase._setup(self)
        self.app.REQUEST['SESSION'] = self.Session()

