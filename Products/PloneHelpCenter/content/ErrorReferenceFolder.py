#
# The Plone How-to container.
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

ErrorReferenceFolderSchema = HelpCenterBaseSchemaFolderish + Schema((
    TextField('description',
        searchable=1,
        required=1,
        accessor="Description",
        default_content_type = 'text/plain',
        allowable_content_types = ('text/plain',),
        storage=MetadataStorage(),
        widget=TextAreaWidget(
            description_msgid="description_edit_ErrorReferenceFolder",
            description="Description for the Error Reference section.",
            label_msgid="description_label_ErrorReferenceFolder",
            label="Description",
            i18n_domain = "plonehelpcenter",
            rows=6)
        ),
    ),) + HelpCenterContainerSchema

class HelpCenterErrorReferenceFolder(PHCFolder,BaseFolder):
    """An Error Reference Section can contain references to and explanations of 
    common errors.
    """

    content_icon = 'errorref_icon.gif'

    schema = ErrorReferenceFolderSchema
    archetype_name = 'Error Reference Section'
    meta_type = 'HelpCenterErrorReferenceFolder'
    global_allow = 0
    filter_content_types = 1
    allowed_content_types = ('HelpCenterErrorReference', )

    typeDescription= 'An Error Reference Section can contain references to and explanations of common errors.'
    typeDescMsgId  = 'description_edit_errorreferencefolder'

    security = ClassSecurityInfo()

    # aliases = PHCFolder.aliases.copy()
    # aliases.update({'(Default)' : 'errorreferencefolder_view',
    #                 'view'      : 'errorreferencefolder_view'})

registerType(HelpCenterErrorReferenceFolder, PROJECTNAME)
