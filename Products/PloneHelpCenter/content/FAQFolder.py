#
#  This is the Plone Help Center FAQ Folder type, with enhanced features
#  like dividing the FAQ into Sections, and Display relevant
#  versions.
#

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
from schemata import HelpCenterBaseSchemaFolderish, HelpCenterContainerSchema
from PHCFolder import PHCFolder

FAQFolderSchema = HelpCenterBaseSchemaFolderish + Schema((
    TextField('description',
        searchable=1,
        required=1,
        accessor="Description",
        default_content_type = 'text/plain',
        allowable_content_types = ('text/plain',),
        storage=MetadataStorage(),
        widget=TextAreaWidget(
                description="Description of the FAQ Container.",
                description_msgid="phc_desc_folder",
                label_msgid="phc_label_folder",
                label="Description",
                i18n_domain = "plonehelpcenter",
                rows=6,)
        ),
    ),) + HelpCenterContainerSchema

class HelpCenterFAQFolder(PHCFolder,OrderedBaseFolder):
    """An FAQ Section can hold frequently asked questions with answers."""

    content_icon = 'faq_icon.gif'

    schema = FAQFolderSchema
    archetype_name = 'FAQ Section'
    meta_type = 'HelpCenterFAQFolder'
    global_allow = 0
    filter_content_types = 1
    allowed_content_types = ('HelpCenterFAQ', )

    security = ClassSecurityInfo()

    typeDescription= 'An FAQ Section can hold frequently asked questions with answers.'
    typeDescMsgId  = 'description_edit_faqfolder'

    # aliases = PHCFolder.aliases.copy()
    # aliases.update({'(Default)' : 'faqfolder_view',
    #                 'view'      : 'faqfolder_view'})

registerType(HelpCenterFAQFolder, PROJECTNAME)
