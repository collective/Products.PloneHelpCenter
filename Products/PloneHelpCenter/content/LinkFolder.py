#
#  This is the Plone Help Center FAQ Folder type, with enhanced features
#  like dividing the FAQ into Sections, and Display relevant
#  versions.
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

LinkFolderSchema = HelpCenterBaseSchemaFolderish + Schema((
    TextField(
        'description',
        searchable=1,
        required=1,
        accessor="Description",
        default_content_type = 'text/plain',
        allowable_content_types = ('text/plain',),
        storage=MetadataStorage(),
        widget=TextAreaWidget(
                description_msgid="description_description_LinkFolder",
                description="Description for the Link section.",
                label_msgid="label_description_LinkFolder",
                label="Description",
                i18n_domain = "plonehelpcenter",
                rows=6,
                )
        ),
    ),) + HelpCenterContainerSchema

class HelpCenterLinkFolder(PHCFolder, ATContentTypes.content.folder.ATFolder):
    """A simple folderish archetype"""

    implements(IHelpCenterFolder)

    content_icon = 'link_icon.gif'

    schema = LinkFolderSchema
    archetype_name = 'Link Section'
    meta_type = 'HelpCenterLinkFolder'
    global_allow = 0
    filter_content_types = 1
    allowed_content_types = ('HelpCenterLink', )

    typeDescription= 'A Link Section can contain links to other documentation.'
    typeDescMsgId  = 'description_edit_linkfolder'

    security = ClassSecurityInfo()

    # aliases = PHCFolder.aliases.copy()
    # aliases.update({'(Default)' : 'helplinkfolder_view',
    #                 'view'      : 'helplinkfolder_view'})

registerType(HelpCenterLinkFolder, PROJECTNAME)
