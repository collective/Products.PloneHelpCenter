from zLOG import INFO
from Products.Archetypes.utils import OrderedDict
import Data

def CreateRootPHC( self, portal ):
    self.setRoles(('Manager',))
    portal.invokeFactory( 'HelpCenter', Data.Hc.Id)
    helpCenter = getattr( portal, Data.Hc.Id )
    helpCenter.setTitle(Data.Hc.Title)
    helpCenter.setDescription(Data.Hc.Desc)
    helpCenter.setVersionsVocab(Data.Hc.Versions)
    helpCenter.setSectionsVocab(Data.Hc.Sections)
    portal.portal_workflow.doActionFor( helpCenter, Data.Transition.publish )
    helpCenter.howto = getattr(helpCenter, "how-to")
    helpCenter.howto.sectionsVocab = Data.HowtoFolder.Sections
    helpCenter.tutorial.sectionsVocab = Data.TutorialFolder.Sections
    helpCenter.faq.sectionsVocab = Data.FAQFolder.Sections
    self.setRoles(('Member',))
    return "Created a PHC instance in the root of your Plone site."

def CreateAltPHC( self, portal ):
    self.setRoles(('Manager',))
    portal.invokeFactory( 'HelpCenter', Data.AltHc.Id)
    altHelpCenter = getattr( portal, Data.AltHc.Id )
    altHelpCenter.setTitle(Data.AltHc.Title)
    altHelpCenter.setDescription(Data.AltHc.Desc)
    altHelpCenter.setVersionsVocab(Data.AltHc.Versions)
    portal.portal_workflow.doActionFor( altHelpCenter, Data.Transition.publish )
    altHelpCenter.howto = getattr(altHelpCenter, "how-to")
    altHelpCenter.howto.sectionsVocab = Data.HowtoFolder.Sections
    altHelpCenter.tutorial.sectionsVocab = Data.TutorialFolder.Sections
    altHelpCenter.faq.sectionsVocab = Data.FAQFolder.Sections
    self.setRoles(('Member',))
    return "Created an alternate PHC instance in the root of your Plone site."

def CreateUsers( self, portal ):
    i = 0
    for user in Data.User.list:
        portal.portal_membership.addMember( user.Id, user.Password, user.Roles, [] )
        i += 1
    return "Created %d test users" % i

def CreateTutorials( self, portal ):
    self.setRoles(('Manager',))
    i = 0
    helpCenter = getattr( portal, Data.Hc.Id )
    for content in Data.Tutorial.list:
        helpCenter.tutorial.invokeFactory( 'HelpCenterTutorial', content.Id)
        newTutorial = getattr( helpCenter.tutorial, content.Id )
        newTutorial.setTitle(content.Title)
        newTutorial.setDescription(content.Summary)
        newTutorial.setVersions(content.Versions)
        newTutorial.setSections(content.Sections)
        # portal.plone_utils.changeOwnershipOf( newTutorial, content.Owner.Id, 1 )
        # Attach pages to the tutorial.
        for page in content.Pages:
            newTutorial.invokeFactory( 'HelpCenterLeafPage', page.Id)
            newPage = getattr( newTutorial, page.Id )
            newPage.setTitle(page.Title)
            newPage.setDescription(page.Summary)
            newPage.setText(page.Body)
            portal.plone_utils.editMetadata( newPage, format=page.Format )
            # Each page should be owned by the same owner as the tutorial owner
            # portal.plone_utils.changeOwnershipOf( newPage, content.Owner.Id, 1 )
            if page.Transition:
                portal.portal_workflow.doActionFor( newPage, page.Transition )
        # Update the tutorial's workflow state
        if content.Transition:
            portal.portal_workflow.doActionFor( newTutorial, content.Transition )

        i += 1
    self.setRoles(('Member',))
    return "Created %d PHC Tutorials." % i

def CreateHowtos( self, portal ):
    self.setRoles(('Manager',))
    i = 0
    helpCenter = getattr( portal, Data.Hc.Id )
    for content in Data.Howto.list:
        helpCenter.howto.invokeFactory( 'HelpCenterHowTo', content.Id)
        newHowto = getattr( helpCenter.howto, content.Id )
        newHowto.setTitle(content.Title)
        newHowto.setDescription(content.Summary)
        newHowto.setText(content.Body)
        newHowto.setVersions(content.Versions)
        newHowto.setSections(content.Sections)
        portal.plone_utils.editMetadata( newHowto, format=content.Format )
        newHowto.reindexObject()
        # portal.plone_utils.changeOwnershipOf( newHowto, content.Owner.Id, 1 )
        if content.Transition:
            portal.portal_workflow.doActionFor( newHowto, content.Transition )
        i += 1
    return "Created %d PHC Howtos." % i

def CreateFaqs( self, portal, alt=False ):
    self.setRoles(('Manager',))
    i = 0
    if alt:
        helpCenter = getattr( portal, Data.AltHc.Id )
    else:
        helpCenter = getattr( portal, Data.Hc.Id )
    
    for content in Data.FAQ.list:
        helpCenter.faq.invokeFactory( 'HelpCenterFAQ', content.Id)
        newFaq = getattr( helpCenter.faq, content.Id )
        newFaq.setTitle(content.Title)
        newFaq.setDescription(content.Question)
        newFaq.setText(content.Answer)
        newFaq.setVersions(content.Versions)
        newFaq.setSections(content.Sections)
        newFaq.reindexObject()
        #portal.plone_utils.editMetadata( newFaq, format=content.Format )
        #portal.plone_utils.changeOwnershipOf( newFaq, content.Owner.Id, 1 )
        if content.Transition:
            portal.portal_workflow.doActionFor( newFaq, content.Transition )
        i += 1
    self.setRoles(('Member',))
    return "Created %d PHC FAQs." % i


def CreateErrorRefs( self, portal ):
    i = 0
    return "Created %d PHC Error References." % i

def CreateDefinitions( self, portal ):
    i = 0
    return "Created %d PHC Definitions." % i

def CreateLinks( self, portal ):
    i = 0
    return "Created %d PHC Links." % i

def CreateReferenceManuals( self, portal ):
    i = 0
    return "Created %d PHC ReferenceManuals." % i

def CreateVideos( self, portal ):
    i = 0
    # See CMFPlone/tests/dummy.py for faking a FileField
    return "Created %d PHC Videos." % i

def CreateTestData( self, portal ):
    out = []
    out.append( CreateRootPHC( self, portal ) )
    out.append( CreateUsers( self, portal ) ) 
    out.append( CreateHowtos( self, portal ) )
    out.append( CreateTutorials( self, portal ) )
    out.append( CreateFaqs( self, portal ) )
    out.append( CreateErrorRefs( self, portal ) )
    out.append( CreateDefinitions( self, portal ) )
    out.append( CreateLinks( self, portal ) )
    out.append( CreateReferenceManuals( self, portal ) )
    out.append( CreateVideos( self, portal ) )
    return '  \n'.join( out )

functions = OrderedDict()
functions['Create Test Data'] = CreateTestData
functions['Create Test Users'] = CreateUsers
functions['Create Test PloneHelpCenter'] = CreateRootPHC
functions['Create Test Tutorials'] = CreateTutorials
functions['Create Test Howtos'] = CreateHowtos
functions['Create Test FAQs'] = CreateFaqs
functions['Create Test Error References'] = CreateReferenceManuals
functions['Create Test Definitions'] = CreateDefinitions
functions['Create Test Links'] = CreateLinks
functions['Create Test Reference Manuals'] = CreateReferenceManuals
functions['Create Test Videos'] = CreateVideos
