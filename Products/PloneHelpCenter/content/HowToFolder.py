#
# The Plone How-to container.
#
# The main goals of these containers are to restrict the addable types and
# provide a sensible default view out-of-the-box, like the FAQ view.
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

HowToFolderSchema = HelpCenterBaseSchemaFolderish + Schema((
    TextField(
        'description',
        searchable=1,
        required=1,
        accessor="Description",
        default_content_type = 'text/plain',
        allowable_content_types = ('text/plain',),
        storage=MetadataStorage(),
        widget=TextAreaWidget(
                description_msgid="phc_desc_howto_folder",
                description="Description for the How-to section.",
                label_msgid="phc_label_howto_folder",
                label="Description",
                i18n_domain = "plonehelpcenter",
                rows=6,
                )
        ),
    )) + HelpCenterContainerSchema

class HelpCenterHowToFolder(PHCFolder, ATContentTypes.content.folder.ATFolder):
    """A How-to Section can contain how-to documents."""

    implements(IHelpCenterFolder)

    content_icon = 'topic_icon.gif'

    schema = HowToFolderSchema
    archetype_name = 'How-to Section'
    meta_type = 'HelpCenterHowToFolder'
    global_allow = 0
    filter_content_types = 1
    allowed_content_types = ('HelpCenterHowTo', )

    typeDescription= 'A How-to Section can contain how-to documents.'
    typeDescMsgId  = 'description_edit_howtofolder'

    security = ClassSecurityInfo()

    # aliases = PHCFolder.aliases.copy()
    # aliases.update({'(Default)' : 'howtofolder_view',
    #                 'view'      : 'howtofolder_view'})

registerType(HelpCenterHowToFolder, PROJECTNAME)
