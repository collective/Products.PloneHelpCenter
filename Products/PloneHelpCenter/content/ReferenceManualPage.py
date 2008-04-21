try:
    from Products.LinguaPlone.public import *
except ImportError:
    # No multilingual support
    from Products.Archetypes.public import *
try:
    import Products.CMFCore.permissions as CMFCorePermissions
except ImportError:
    from Products.CMFCore import CMFCorePermissions
from Products.PloneHelpCenter.config import *
from schemata import HelpCenterBaseSchema
from PHCContent import PHCContent

ReferenceManualPageSchema = HelpCenterBaseSchema + Schema((
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
                description="Enter a brief description.",
                description_msgid="phc_desc_referencemanual_page",
                label="Description",
                label_msgid="phc_label_referencemanual_page",
                rows=5,
                i18n_domain="plonehelpcenter",
                )
        ),

    TextField(
        'body',
        required=1,
        searchable=1,
        primary=1,
        widget=RichWidget(
                description = "The body text.",
                description_msgid = "phc_desc_body_referencemanual",
                label = "Body text",
                label_msgid = "phc_label_body_referencemanual",
                rows = 25,
                i18n_domain = "plonehelpcenter"
                ),
        **DEFAULT_CONTENT_TYPES
        )
    ),)

class HelpCenterReferenceManualPage(PHCContent,BaseContent):
    """Part of a reference manual."""

    __implements__ = (PHCContent.__implements__,
                      BaseContent.__implements__,)

    schema = ReferenceManualPageSchema
    archetype_name = 'Page'
    meta_type='HelpCenterReferenceManualPage'
    content_icon = 'document_icon.gif'

    global_allow = 0
    # allow_discussion = 1

    typeDescription= 'A Reference Manual Page contains the text of one of the pages of the the reference manual, usually confined to a single topic.'
    typeDescMsgId  = 'description_edit_referencemanualpage'


registerType(HelpCenterReferenceManualPage, PROJECTNAME)

