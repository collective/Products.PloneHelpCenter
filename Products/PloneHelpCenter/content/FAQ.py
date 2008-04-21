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

FAQSchema = HelpCenterBaseSchema + Schema((
    TextField(
        'description',
        default='',
        searchable=1,
        required=0,
        accessor="Description",
        default_content_type = 'text/plain',
        allowable_content_types = ('text/plain',),
        storage=MetadataStorage(),
        widget=TextAreaWidget(
                description = 'More details on the question, if not evident from the title.',
                description_msgid = "help_detailed_question",
                label = "Detailed Question",
                label_msgid = "label_detailed_question",
                rows = 5,
                i18n_domain = "plonehelpcenter",
                ),
        ),
        
    TextField(
        'answer',
        required=1,
        searchable=1,
        primary=1,
        widget=RichWidget(
                label_msgid = "label_answer",
                i18n_domain = "plonehelpcenter",
                rows=10),
        **DEFAULT_CONTENT_TYPES
        ),
    ),) + GenericHelpCenterItemSchema

# For some reason, we need to jump through these hoops to get the fields in the
# the right order
FAQSchema.moveField('subject', pos='bottom')
FAQSchema.moveField('relatedItems', pos='bottom')

class HelpCenterFAQ(PHCContent,BaseContent):
    """A Frequently Asked Question defines a common question with an answer - 
    this is a place to document answers to common questions, not ask them.
    """

    __implements__ = (PHCContent.__implements__,
                      BaseContent.__implements__,)

    content_icon = 'faq_icon.gif'

    schema = FAQSchema
    archetype_name = 'FAQ'
    meta_type = 'HelpCenterFAQ'
    global_allow = 0
    # allow_discussion = IS_DISCUSSABLE

    typeDescription= 'A Frequently Asked Question defines a common question with an answer - this is a place to document answers to common questions, not ask them.'
    typeDescMsgId  = 'description_edit_faq'

    # aliases = PHCContent.aliases.copy()
    # aliases.update({'(Default)' : 'faq_view',
    #                 'view'      : 'faq_view'})


registerType(HelpCenterFAQ, PROJECTNAME)
