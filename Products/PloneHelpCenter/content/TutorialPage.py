from zope.interface import implements

try:
    from Products.LinguaPlone.public import *
except ImportError:
    # No multilingual support
    from Products.Archetypes.public import *
import Products.CMFCore.permissions as CMFCorePermissions

from Products.PloneHelpCenter.config import *
from schemata import HelpCenterBaseSchema
from PHCContent import PHCContent
from Products.PloneHelpCenter.interfaces import IHelpCenterMultiPage

TutorialPageSchema = HelpCenterBaseSchema + Schema((
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
                  description_msgid="phc_desc_tutorial_page",
                  label="Description",
                  label_msgid="phc_label_tutorial_page",
                  rows=5,
                  i18n_domain="plonehelpcenter",
                  ),
        ),

    TextField(
        'body',
        required=1,
        searchable=1,
        primary=1,
        widget=RichWidget(
                description="The body text.",
                description_msgid="phc_desc_body_tutorial",
                label="Body text",
                label_msgid="phc_label_body_tutorial",
                rows=25,
                i18n_domain="plonehelpcenter"
                ),
        **DEFAULT_CONTENT_TYPES
        ),
    ),)

class HelpCenterTutorialPage(PHCContent,BaseContent):
    """Part of a tutorial."""

    implements(IHelpCenterMultiPage)

    __implements__ = (PHCContent.__implements__,
                      BaseContent.__implements__,)

    schema = TutorialPageSchema
    archetype_name = 'Page'
    meta_type='HelpCenterTutorialPage'
    content_icon = 'document_icon.gif'

    global_allow = 0
    # allow_discussion = 1

    typeDescription= 'A Tutorial Page contains the text of a single page of the tutorial.'
    typeDescMsgId  = 'description_edit_tutorialpage'


registerType(HelpCenterTutorialPage, PROJECTNAME)
