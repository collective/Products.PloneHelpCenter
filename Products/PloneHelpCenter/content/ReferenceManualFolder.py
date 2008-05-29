#
# The Plone Reference Manual container.
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


ReferenceManualFolderSchema = HelpCenterBaseSchemaFolderish + Schema((
    TextField(
        'description',
        searchable=1,
        required=1,
        accessor="Description",
        default_content_type = 'text/plain',
        allowable_content_types = ('text/plain',),
        storage=MetadataStorage(),
        widget=TextAreaWidget(
                description_msgid="phc_desc_folder_referencemanual",
                description="Description for the reference manual section.",
                label_msgid="phc_label_folder_referencemanual",
                label="Description",
                i18n_domain = "plonehelpcenter",
                rows=6,
                ),
        ),
    ),) + HelpCenterContainerSchema

class HelpCenterReferenceManualFolder(PHCFolder,OrderedBaseFolder):
    """A simple folderish archetype"""

    __implements__ = (PHCFolder.__implements__,
        OrderedBaseFolder.__implements__)

    content_icon = 'referencemanual_icon.gif'

    schema = ReferenceManualFolderSchema
    archetype_name = 'Reference Manual Section'
    meta_type = 'HelpCenterReferenceManualFolder'
    global_allow = 0
    filter_content_types = 1
    allowed_content_types = ('HelpCenterReferenceManual', )

    typeDescription= 'A Reference Manual Section can contain reference manuals for individual projects and larger documentation efforts.'
    typeDescMsgId  = 'description_edit_referencemanualfolder'


    security = ClassSecurityInfo()


registerType(HelpCenterReferenceManualFolder, PROJECTNAME)
