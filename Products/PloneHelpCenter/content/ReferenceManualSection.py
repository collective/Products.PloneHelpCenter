from zope.interface import implements
from AccessControl import ClassSecurityInfo
from Acquisition import aq_parent, aq_inner

try:
    from Products.LinguaPlone.public import *
except ImportError:
    # No multilingual support
    from Products.Archetypes.public import *
import Products.CMFCore.permissions as CMFCorePermissions

from Products import ATContentTypes
from Products.ATContentTypes.content.schemata import finalizeATCTSchema

from Products.PloneHelpCenter.config import *
from Products.PloneHelpCenter.content.PHCContent import HideMetadataFields
from Products.PloneHelpCenter.interfaces import IHelpCenterMultiPage


HelpCenterReferenceManualSectionSchema = ATContentTypes.content.folder.ATFolderSchema.copy()
HideMetadataFields(HelpCenterReferenceManualSectionSchema)


class HelpCenterReferenceManualSection(ATContentTypes.content.folder.ATFolder):
    """A section of a reference manual containing ReferenceManualPages and
    other ReferenceManualSections.
    """

    implements(IHelpCenterMultiPage)
    
    schema = HelpCenterReferenceManualSectionSchema

    archetype_name = 'Section'
    meta_type = 'HelpCenterReferenceManualSection'

    typeDescription= 'A Reference Manual Section can contain Reference Manual Pages, and other Reference Manual (Sub-)Sections. Index order is decided by the folder order, use the normal up/down arrow in the folder content view to rearrange content.'
    typeDescMsgId  = 'description_edit_referencemanualsection'

    security = ClassSecurityInfo()

    security.declareProtected(CMFCorePermissions.View, 'getSectionDescription')
    def getSectionDescription(self):
        """ Returns the description of the section --
        convenience method for ReferenceManualPage
        """
        return self.Description()

        
    security.declareProtected(CMFCorePermissions.View, 'Rights')
    def Rights(self):
        """ get from parent """
        return aq_parent(aq_inner(self)).Rights()
    
    security.declareProtected(CMFCorePermissions.View, 'Creators')
    def Creators(self):
        """ get from parent """
        return aq_parent(aq_inner(self)).Creators()
    
    security.declareProtected(CMFCorePermissions.View, 'Contributors')
    def Contributors(self):
        """ get from parent """
        return aq_parent(aq_inner(self)).Contributors()

    security.declarePublic('contentIds')
    def contentIds(self, filter=None):
        """
             List IDs of contentish and folderish sub-objects.
             (method is without docstring to disable publishing)
             
             Fix for https://bugs.launchpad.net/zope-cmf/+bug/661834
        """
        return ATContentTypes.content.folder.ATFolder.contentIds(self, filter)

registerType(HelpCenterReferenceManualSection, PROJECTNAME)

