#
# The Plone Instructional Video container.
#
# The main goals of these containers are to restrict the addable types and
# provide a sensible default view out-of-the-box, like the FAQ view.
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

InstructionalVideoFolderSchema = HelpCenterBaseSchemaFolderish + Schema((
    TextField(
        'description',
        searchable=1,
        accessor="Description",
        default_content_type = 'text/plain',
        allowable_content_types = ('text/plain',),
        storage=MetadataStorage(),
        widget=TextAreaWidget(
                description_msgid="phc_desc_video_folder",
                description="Description for the Video section.",
                label_msgid="phc_label_video_folder",
                label="Description",
                i18n_domain = "plonehelpcenter",
                rows=6),
                ),
    ),) + HelpCenterContainerSchema

class HelpCenterInstructionalVideoFolder(PHCFolder,OrderedBaseFolder):
    """A simple folderish archetype"""

    content_icon = 'movie_icon.gif'

    schema = InstructionalVideoFolderSchema
    archetype_name = 'Video Section'
    meta_type = 'HelpCenterInstructionalVideoFolder'
    global_allow = 0
    filter_content_types = 1
    allowed_content_types = ('HelpCenterInstructionalVideo', )

    typeDescription= 'A Video Section can contain instructional Flash videos.'
    typeDescMsgId  = 'description_edit_instructionalvideofolder'

    security = ClassSecurityInfo()

    # aliases = PHCFolder.aliases.copy()
    # aliases.update({'(Default)' : 'ivideofolder_view',
    #                 'view'      : 'ivideofolder_view'})

registerType(HelpCenterInstructionalVideoFolder, PROJECTNAME)
