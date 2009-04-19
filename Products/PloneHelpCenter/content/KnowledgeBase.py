from zope.interface import implements
from AccessControl import ClassSecurityInfo, ModuleSecurityInfo

try:
    from Products.LinguaPlone.public import *
except ImportError:
    # No multilingual support
    from Products.Archetypes.public import *

import Products.CMFCore.permissions as CMFCorePermissions

from Products.Archetypes import atapi

from Products.ATContentTypes.content import folder, schemata

from Products.PloneHelpCenter.config import PROJECTNAME
from Products.PloneHelpCenter.interfaces import IHelpCenterFolder
from schemata import HelpCenterContainerSchema
from PHCFolder import PHCFolder

KnowledgeBaseSchema = folder.ATBTreeFolderSchema.copy() + HelpCenterContainerSchema    
schemata.finalizeATCTSchema(KnowledgeBaseSchema, moveDiscussion=False, folderish=True)

class HelpCenterKnowledgeBase(PHCFolder, folder.ATBTreeFolder):
    """
        A Single-Folder KnowledgeBase that can organize a large number of how-tos and tutorials by topic and audience.
    """

    implements(IHelpCenterFolder)

    archetype_name = 'Knowledge Base'
    meta_type = "HelpCenterKnowledgeBase"
    
    schema = KnowledgeBaseSchema

    filter_content_types = 1
    allowed_content_types = ('HelpCenterTutorial', 'HelpCenterHowTo', 'Topic')

    typeDescription= 'A Single-Folder KnowledgeBase that can organize a large number of how-tos and tutorials by topic and audience.'
    typeDescMsgId  = 'description_edit_knowledgebase'

    content_icon = 'helpcenter_icon.gif'

    security = ClassSecurityInfo()


atapi.registerType(HelpCenterKnowledgeBase, PROJECTNAME)
