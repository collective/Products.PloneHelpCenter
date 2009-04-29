"""
    PHC General-Purpose Leaf Content
    A simple customization of ATDocument to
    derive most metadata from parents and
    to allow separate marker interfaces.
"""

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

from Products.PloneHelpCenter.config import *
from PHCContent import HideMetadataFields
from Products.PloneHelpCenter.interfaces import \
    IHelpCenterMultiPage, IHelpCenterNavRoot


LeafPageSchema = ATContentTypes.content.document.ATDocumentSchema.copy()
ATContentTypes.content.schemata.finalizeATCTSchema(LeafPageSchema)
HideMetadataFields(LeafPageSchema)
LeafPageSchema['relatedItems'].schemata = 'default'


class HelpCenterLeafPage(ATContentTypes.content.document.ATDocument):
    """A page that delegates metadata handling to a parent."""

    implements(IHelpCenterMultiPage)

    schema = LeafPageSchema

    archetype_name = 'Page'
    meta_type='HelpCenterLeafPage'
    content_icon = 'document_icon.gif'

    typeDescription= 'A Help Center content page.'
    typeDescMsgId  = 'description_leafpage'

    security = ClassSecurityInfo()

    # Satisfy metadata requirements for items with hidden metadata.
    
    def navRootObject(self):
        """ Find the metadata parent """
    
        parent = aq_inner(self).aq_parent
        while parent and not IHelpCenterNavRoot.providedBy(parent):
            parent = parent.aq_parent
        return parent
    
    
    security.declareProtected(CMFCorePermissions.View, 'Subject')
    def Subject(self):
        """ get from parent """
        return self.navRootObject().Subject()
    
    security.declareProtected(CMFCorePermissions.View, 'Rights')
    def Rights(self):
        """ get from parent """
        return self.navRootObject().Rights()
    
    security.declareProtected(CMFCorePermissions.View, 'Creators')
    def Creators(self):
        """ get from parent """
        return self.navRootObject().Creators()
    
    security.declareProtected(CMFCorePermissions.View, 'Contributors')
    def Contributors(self):
        """ get from parent """
        return self.navRootObject().Contributors()
    
    security.declareProtected(CMFCorePermissions.View, 'listCreators')
    def listCreators(self):
        """ List Dublin Core Creator elements - resource authors.
        """
        return self.navRootObject().Creators()
        
registerType(HelpCenterLeafPage, PROJECTNAME)
