try:
    from Products.LinguaPlone.public import *
except ImportError:
    # No multilingual support
    from Products.Archetypes.public import *
from Products.PloneHelpCenter.config import *
try:
    import Products.CMFCore.permissions as CMFCorePermissions
except ImportError:
    from Products.CMFCore import CMFCorePermissions
from schemata import HelpCenterBaseSchema
from PHCContent import PHCContent
from AccessControl import ClassSecurityInfo

ReferenceManualSectionSchema = HelpCenterBaseSchema + Schema((
    TextField(
        'description',
        default='',
        searchable=1,
        required=1,
        accessor="Description",
        default_content_type = 'text/plain',
        allowable_content_types = ('text/plain',),
        storage=MetadataStorage(),
        widget=TextAreaWidget(
                description = "Enter a brief description for this section of the manual.",
                description_msgid = "phc_desc_referencemanual_section",
                label = "Description",
                label_msgid = "phc_label_referencemanual_section",
                rows = 5,
                i18n_domain = "plonehelpcenter",
                )
        ),
    ),)

class HelpCenterReferenceManualSection(PHCContent,OrderedBaseFolder):
    """A section of a reference manual containing ReferenceManualPages and
    other ReferenceManualSections.
    """

    __implements__ = (PHCContent.__implements__,
                      OrderedBaseFolder.__implements__,)

    schema = ReferenceManualSectionSchema
    archetype_name = 'Section'
    meta_type = 'HelpCenterReferenceManualSection'
    content_icon = 'chapter_icon.gif'

    global_allow = 0
    filter_content_types = 1
    allowed_content_types = ('HelpCenterReferenceManualPage', 'Image',
                                'HelpCenterReferenceManualSection')
    # allow_discussion = IS_DISCUSSABLE

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

