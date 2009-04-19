#
#  This is the Plone Help Center folderish Glossary type, which
#  is a simple container that has Definitions.
#

from zope.interface import implements

try:
    from Products.LinguaPlone.public import *
except ImportError:
    # No multilingual support
    from Products.Archetypes.public import *
import Products.CMFCore.permissions as CMFCorePermissions

from AccessControl import ClassSecurityInfo, ModuleSecurityInfo
from Products.PloneHelpCenter.config import *
from schemata import HelpCenterBaseSchemaFolderish, HelpCenterContainerSchema
from Products import ATContentTypes
from PHCFolder import PHCFolder
from Products.PloneHelpCenter.interfaces import IHelpCenterFolder

GlossarySchema = HelpCenterBaseSchemaFolderish + Schema((
    TextField(
        'description',
        searchable=1,
        required=1,
        primary=1,
        accessor="Description",
        default_content_type = 'text/plain',
        allowable_content_types = ('text/plain',),
        storage=MetadataStorage(),
        widget=TextAreaWidget(
                description="Description of the Glossary.",
                description_msgid="phc_desc_folder_glossary",
                label_msgid="phc_label_folder_glossary",
                label="Description",
                i18n_domain = "plonehelpcenter",
                rows= 6,
                )
        ),
    ),) + HelpCenterContainerSchema

class HelpCenterGlossary(PHCFolder, ATContentTypes.content.folder.ATFolder):
    """A Glossary can be used to hold definitions of common terms, listing them 
    in a dictionary-like manner.
    """

    implements(IHelpCenterFolder)

    content_icon = 'glossary_icon.gif'

    schema = GlossarySchema
    archetype_name = 'Glossary'
    meta_type = 'HelpCenterGlossary'
    global_allow = 0
    filter_content_types = 1
    allowed_content_types = ('HelpCenterDefinition', )

    typeDescription= 'A Glossary can be used to hold definitions of common terms, listing them in a dictionary-like manner.'
    typeDescMsgId  = 'description_edit_glossary'

    security = ClassSecurityInfo()

    # aliases = PHCFolder.aliases.copy()
    # aliases.update({'(Default)' : 'glossary_view',
    #                 'view'      : 'glossary_view'})

registerType(HelpCenterGlossary, PROJECTNAME)
