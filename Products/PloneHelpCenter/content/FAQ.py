from AccessControl import ClassSecurityInfo, ModuleSecurityInfo

try:
    from Products.LinguaPlone.public import *
except ImportError:
    # No multilingual support
    from Products.Archetypes.public import *

import Products.CMFCore.permissions as CMFCorePermissions

from Products import ATContentTypes
from Products.ATContentTypes.content.document import ATDocumentBase
from Products.ATContentTypes.content.schemata import finalizeATCTSchema

from Products.PloneHelpCenter.config import *
from schemata import HelpCenterItemSchemaNarrow
from PHCContent import PHCContentMixin, HideOwnershipFields


FAQSchema = ATContentTypes.content.document.ATDocumentSchema.copy() + HelpCenterItemSchemaNarrow
FAQSchema['description'].widget = \
       TextAreaWidget(
        description = 'More details on the question, if not evident from the title.',
        description_msgid = "help_detailed_question",
        label = "Detailed Question",
        label_msgid = "label_detailed_question",
        rows = 5,
        i18n_domain = "plonehelpcenter",
        )
FAQSchema['text'].widget.label = "Answer"
FAQSchema['text'].widget.label_msgid = "label_answer"
FAQSchema['text'].widget.i18n_domain = "plonehelpcenter"
for key, attr in DEFAULT_CONTENT_TYPES.items():
    setattr(FAQSchema['text'], key, attr)
    
finalizeATCTSchema(FAQSchema, folderish=False, moveDiscussion=False)


class HelpCenterFAQ(ATDocumentBase,PHCContentMixin):
    """A Frequently Asked Question defines a common question with an answer - 
    this is a place to document answers to common questions, not ask them.
    """

    __implements__ = (ATDocumentBase.__implements__,)

    content_icon = 'faq_icon.gif'

    schema = FAQSchema
    archetype_name = 'FAQ'
    meta_type = 'HelpCenterFAQ'

    typeDescription= 'A Frequently Asked Question defines a common question with an answer - this is a place to document answers to common questions, not ask them.'
    typeDescMsgId  = 'description_edit_faq'


registerType(HelpCenterFAQ, PROJECTNAME)
