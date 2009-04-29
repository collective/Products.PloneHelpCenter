from zope.interface import implements
from AccessControl import ClassSecurityInfo

try:
    from Products.LinguaPlone.public import *
except ImportError:
    # No multilingual support
    from Products.Archetypes.public import *

import Products.CMFCore.permissions as CMFCorePermissions
from Products import ATContentTypes
from Products.ATContentTypes.content.schemata import finalizeATCTSchema

from Products.PloneHelpCenter.config import *
from schemata import HelpCenterItemSchemaNarrow
from PHCContent import PHCContentMixin
from Products.PloneHelpCenter.interfaces import IHelpCenterNavRoot

TutorialSchema = ATContentTypes.content.folder.ATFolderSchema.copy() + HelpCenterItemSchemaNarrow
if GLOBAL_RIGHTS:
    del TutorialSchema['rights']
finalizeATCTSchema(TutorialSchema, folderish=True, moveDiscussion=False)
TutorialSchema['nextPreviousEnabled'].defaultMethod = None  
TutorialSchema['nextPreviousEnabled'].default = True  


class HelpCenterTutorial(ATContentTypes.content.folder.ATFolder, PHCContentMixin):
    """A tutorial containing TutorialPages, Files and Images."""

    implements(IHelpCenterNavRoot)

    schema = TutorialSchema
    archetype_name = 'Tutorial'
    meta_type = portal_type = 'HelpCenterTutorial'
    content_icon = 'tutorial_icon.gif'

    typeDescription= 'A Tutorial can contain Tutorial Pages, Images and Files. Index order is decided by the folder order, use the normal up/down arrow in the folder content view to rearrange content.'
    typeDescMsgId  = 'description_edit_tutorial'

    security = ClassSecurityInfo()


    security.declareProtected(CMFCorePermissions.View, 'getTutorialDescription')
    def getTutorialDescription(self):
        """ Returns the description of the Tutorial--convenience method for TutorialPage """
        return self.Description()


    security.declareProtected(CMFCorePermissions.View, 'getPages')
    def getPages(self, states=[]):
        """Get items"""
        criteria = contentFilter = \
            {'object_provides' : 
             'Products.PloneHelpCenter.interfaces.IHelpCenterMultiPage',}
        if states:
            criteria['review_state'] = states
        return self.getFolderContents(contentFilter = criteria)


    security.declareProtected(CMFCorePermissions.View, 'getPagePosition')
    def getPagePosition(self, obj, states=[]):
        """Get position in folder of the current context"""
        pages = self.getPages()
        for i in range(len(pages)):
            if pages[i].getId == obj.getId():
                return i
        return None


    security.declareProtected(CMFCorePermissions.View, 'getTOCSelectOptions')
    def getTOCSelectOptions(self, current=None):
        """
        Calls getTOC then cooks the results into a sequence of dicts:
            title: tile of section/page, including numbering
            url:   URL of page
            current: True if current section/page
        This is a convenience for creating an option list.
        """

        res = []
        cid = current.getId()
        for page in self.getPages():
            res.append( {'title':page.Title, 'url':page.getURL, 'current':cid==page.id  } )
        return res


    security.declareProtected(CMFCorePermissions.View, 'getAllPagesURL')
    def getAllPagesURL(self):
        """ return URL for all pages view """

        return "%s/tutorial-all-pages" % self.absolute_url()


        security.declareProtected(CMFCorePermissions.View, 'getNextPreviousParentValue')
        def getNextPreviousParentValue(self):
            """ always true """
            return True


    security.declareProtected(CMFCorePermissions.View, 'Rights')
    def Rights(self):
        """ get rights from parent if necessary """
        if self.Schema().has_key('rights'):
            return self.getRawRights()
        else:
            return self.aq_parent.Rights()


    security.declareProtected(CMFCorePermissions.View, 'Creators')
    def Creators(self):
        """ get rights from parent if necessary """
        if self.Schema().has_key('creators'):
            return self.getRawCreators()
        else:
            return self.aq_parent.Creators()


registerType(HelpCenterTutorial, PROJECTNAME)

