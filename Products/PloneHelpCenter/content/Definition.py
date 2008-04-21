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

DefinitionSchema = HelpCenterBaseSchema + Schema((
    TextField(
        'description',
        default='',
        searchable=1,
        required=1,
        primary=1,
        accessor="Description",
        default_content_type = 'text/plain',
        allowable_content_types = ('text/plain',),
        storage=AttributeStorage(), # Needed for HistoryAwareMixin
        widget = TextAreaWidget(
                    description = 'An explanation of the term.',
                    description_msgid = "phc_desc_definition",
                    label = "Definition",
                    label_msgid = "phc_label_definition",
                    rows = 5,
                    i18n_domain = "plonehelpcenter",
                    )
        ),
    ),) + GenericHelpCenterItemSchema

# For some reason, we need to jump through these hoops to get the fields in the
# the right order
DefinitionSchema.moveField('subject', pos='bottom')
DefinitionSchema.moveField('relatedItems', pos='bottom')

class HelpCenterDefinition(PHCContent,BaseContent):
    """A Definition defines a special term, and will be listed in the glossary.
    """

    __implements__ = (PHCContent.__implements__,
                      BaseContent.__implements__,)

    content_icon = 'glossary_icon.gif'

    schema = DefinitionSchema
    archetype_name = 'Definition'
    meta_type = 'HelpCenterDefinition'
    global_allow = 0
    # allow_discussion = IS_DISCUSSABLE

    typeDescription= 'A Definition defines a special term, and will be listed in the glossary.'
    typeDescMsgId  = 'description_edit_definition'

    # aliases = PHCContent.aliases.copy()
    # aliases.update({'(Default)' : 'definition_view',
    #                 'view'      : 'definition_view'})

registerType(HelpCenterDefinition, PROJECTNAME)
