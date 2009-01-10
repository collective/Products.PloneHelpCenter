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
from Products.PloneHelpCenter.interfaces import IHelpCenterMultiPage


class HelpCenterReferenceManualSection(ATContentTypes.content.folder.ATFolder):
    """A section of a reference manual containing ReferenceManualPages and
    other ReferenceManualSections.
    """

    implements(IHelpCenterMultiPage)

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

registerType(HelpCenterReferenceManualSection, PROJECTNAME)

