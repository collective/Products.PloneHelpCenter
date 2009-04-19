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

TutorialFolderSchema = HelpCenterBaseSchemaFolderish + Schema((
    TextField(
        'description',
        searchable=1,
        required=1,
        accessor="Description",
        default_content_type = 'text/plain',
        allowable_content_types = ('text/plain',),
        storage=MetadataStorage(),
        widget=TextAreaWidget(
                description_msgid="phc_desc_folder_tutorial",
                description="Description for the tutorials section.",
                label_msgid="phc_label_folder_tutorial",
                label="Description",
                i18n_domain = "plonehelpcenter",
                rows=6,
                ),
        ),
    ),) + HelpCenterContainerSchema

class HelpCenterTutorialFolder(PHCFolder, ATContentTypes.content.folder.ATFolder):
    """
        A tutorial container
    """

    implements(IHelpCenterFolder)

    content_icon = 'tutorial_icon.gif'

    schema = TutorialFolderSchema
    archetype_name = 'Tutorial Section'
    meta_type = 'HelpCenterTutorialFolder'
    global_allow = 0
    filter_content_types = 1
    allowed_content_types = ('HelpCenterTutorial', )

    typeDescription= 'A Tutorial Section can contain tutorial-length, multi-page documentation.'
    typeDescMsgId  = 'description_edit_tutorialfolder'


    security = ClassSecurityInfo()


registerType(HelpCenterTutorialFolder, PROJECTNAME)
