try:
    from Products.LinguaPlone.public import *
except ImportError:
    # No multilingual support
    from Products.Archetypes.public import *
try:
    import Products.CMFCore.permissions as CMFCorePermissions
except ImportError:
    from Products.CMFCore import CMFCorePermissions
from AccessControl import ClassSecurityInfo, ModuleSecurityInfo
from Products.PloneHelpCenter.config import *
from schemata import HelpCenterBaseSchema, GenericHelpCenterItemSchema
from PHCContent import PHCContent

LinkSchema = HelpCenterBaseSchema + Schema((
    TextField(
        'description',
        default='',
        searchable=1,
        required=1,
        accessor="Description",
        default_content_type = 'text/plain',
        allowable_content_types = ('text/plain',),
        storage=MetadataStorage(),
        widget=TextAreaWidget(description_msgid="description_edit_Link",
                description="Description for the Link.",
                label_msgid="description_label_Link",
                label="Description",
                i18n_domain = "plonehelpcenter"),
        ),
    
    StringField(
        'url',
        searchable=1,
        required=1,
        primary=1,
        default='http://',
        languageIndependent=1,
        widget=StringWidget(
                description_msgid='phc_desc_link_url',
                description='Web address.',
                label_msgid='phc_label_link_url',
                label='URL',
                i18n_domain='plonehelpcenter',
                ),
        ),
    ),

    ) + GenericHelpCenterItemSchema

# For some reason, we need to jump through these hoops to get the fields in the
# the right order
LinkSchema.moveField('subject', pos='bottom')
LinkSchema.moveField('relatedItems', pos='bottom')

class HelpCenterLink(PHCContent,BaseContent):
    """A simple archetype"""

    __implements__ = (PHCContent.__implements__,
                      BaseContent.__implements__,)

    content_icon = 'helplink_icon.gif'

    schema = LinkSchema
    archetype_name = 'Link'
    meta_type = 'HelpCenterLink'
    global_allow = 0
    # allow_discussion = IS_DISCUSSABLE

    typeDescription= 'Links are links to other documentation and resources.'
    typeDescMsgId  = 'description_edit_link'

    # aliases = PHCContent.aliases.copy()
    # aliases.update({'(Default)' : 'helplink_view',
    #                 'view'      : 'helplink_view'})


registerType(HelpCenterLink, PROJECTNAME)
