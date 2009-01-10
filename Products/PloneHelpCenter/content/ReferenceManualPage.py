from zope.interface import implements

try:
    from Products.LinguaPlone.public import *
except ImportError:
    # No multilingual support
    from Products.Archetypes.public import *

import Products.CMFCore.permissions as CMFCorePermissions

from Products import ATContentTypes
from Products.ATContentTypes.content.schemata import finalizeATCTSchema

from Products.PloneHelpCenter.config import *
from Products.PloneHelpCenter.interfaces import IHelpCenterMultiPage, IHelpCenterContent


class HelpCenterReferenceManualPage(ATContentTypes.content.document.ATDocument):
    """Part of a reference manual."""
    
    implements(IHelpCenterMultiPage)

    schema = ATContentTypes.content.document.ATDocumentSchema.copy()

    portal_type = meta_type = 'HelpCenterReferenceManualPage'
    archetype_name = 'Manual Page'

registerType(HelpCenterReferenceManualPage, PROJECTNAME)

