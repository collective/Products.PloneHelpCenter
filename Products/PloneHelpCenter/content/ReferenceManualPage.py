from zope.interface import implements
from AccessControl import ClassSecurityInfo
from Acquisition import aq_inner

try:
    from Products.LinguaPlone.public import *
except ImportError:
    # No multilingual support
    from Products.Archetypes.public import *

import Products.CMFCore.permissions as CMFCorePermissions

from Products import ATContentTypes
from Products.ATContentTypes.interfaces import IATDocument
from Products.ATContentTypes.content.schemata import finalizeATCTSchema

from Products.PloneHelpCenter.config import *
from Products.PloneHelpCenter.content.PHCContent import HideOwnershipFields
from Products.PloneHelpCenter.interfaces import IHelpCenterMultiPage, IHelpCenterContent


HelpCenterReferenceManualPageSchema = ATContentTypes.content.document.ATDocumentSchema.copy()
HideOwnershipFields(HelpCenterReferenceManualPageSchema)
# Support specified content formats
for key, attr in DEFAULT_CONTENT_TYPES.items():
    setattr(HelpCenterReferenceManualPageSchema['text'], key, attr)


class HelpCenterReferenceManualPage(ATContentTypes.content.document.ATDocumentBase):
    """Part of a reference manual."""
    
    __implements__ = (ATContentTypes.content.document.ATDocumentBase.__implements__,
                      IATDocument)

    schema = HelpCenterReferenceManualPageSchema

    portal_type = meta_type = 'HelpCenterReferenceManualPage'
    archetype_name = 'Manual Page'

    security = ClassSecurityInfo()


    # Satisfy metadata requirements for items with deleted ownership.
    # It would be great to do this in a mixin or adapter,
    # but the structure of Archetypes prevents that.
    
    security.declareProtected(CMFCorePermissions.View, 'Rights')
    def Rights(self):
        """ get from parent """
        return aq_inner(self).aq_parent.Rights()
    
    security.declareProtected(CMFCorePermissions.View, 'Creators')
    def Creators(self):
        """ get from parent """
        return aq_inner(self).aq_parent.Creators()
    
    security.declareProtected(CMFCorePermissions.View, 'Contributors')
    def Contributors(self):
        """ get from parent """
        return aq_inner(self).aq_parent.Contributors()
        
    security.declareProtected(CMFCorePermissions.View, 'listCreators')
    def listCreators(self):
        """ List Dublin Core Creator elements - resource authors.
        """
        return self.Creators()
        

registerType(HelpCenterReferenceManualPage, PROJECTNAME)

