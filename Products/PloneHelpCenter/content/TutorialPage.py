from zope.interface import implements
from AccessControl import ClassSecurityInfo
from Acquisition import aq_inner

try:
    from Products.LinguaPlone.public import *
except ImportError:
    # No multilingual support
    from Products.Archetypes.public import *
import Products.CMFCore.permissions as CMFCorePermissions

import Products.CMFCore.permissions as CMFCorePermissions
from Products import ATContentTypes
from Products.ATContentTypes.interfaces import IATDocument

from Products.PloneHelpCenter.config import *
from PHCContent import HideOwnershipFields
from Products.PloneHelpCenter.interfaces import IHelpCenterMultiPage

TutorialPageSchema = ATContentTypes.content.document.ATDocumentSchema.copy()
HideOwnershipFields(TutorialPageSchema)
# Support specified content formats
for key, attr in DEFAULT_CONTENT_TYPES.items():
    setattr(TutorialPageSchema['text'], key, attr)

class HelpCenterTutorialPage(ATContentTypes.content.document.ATDocumentBase):
    """Part of a tutorial."""

    implements(IHelpCenterMultiPage)

    __implements__ = ATContentTypes.content.document.ATDocumentBase.__implements__, IATDocument

    schema = TutorialPageSchema

    archetype_name = 'Page'
    meta_type='HelpCenterTutorialPage'
    content_icon = 'document_icon.gif'

    typeDescription= 'A Tutorial Page contains the text of a single page of the tutorial.'
    typeDescMsgId  = 'description_edit_tutorialpage'

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
        
registerType(HelpCenterTutorialPage, PROJECTNAME)
