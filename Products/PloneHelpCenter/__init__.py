from AccessControl import allow_module
from Globals import package_home
from Products.Archetypes.public import process_types, listTypes
from Products.CMFCore import utils as CMFCoreUtils
from Products.CMFCore.DirectoryView import registerDirectory
import os, os.path, sys

# Get all the content types in the types directory
from Products.PloneHelpCenter import content

# Ensure that pickles refering to the old 'types' module now find 'content'
sys.modules['Products.PloneHelpCenter.types'] = content

from config import *

registerDirectory(SKINS_DIR, GLOBALS)

# MonkeyPatch CMFDefault.DiscussionItemContainer
import Patch

def initialize(context):

    # Make the utils module importable TTW
    allow_module('Products.PloneHelpCenter.utils')

    contentTypes, constructors, ftis = process_types(
        listTypes(PROJECTNAME),
        PROJECTNAME)

    # Initialise. Note that the ADD_CONTENT_PERMISSION is only used in contained
    # images and files; for our special folders and content types, we have
    # defined a custom factory with either ADD_CENTER_PERMISSION,
    # ADD_HELP_AREA_PERMISSION, ADD_DOCUMENTATION_PERMISSION
    CMFCoreUtils.ContentInit(
        PROJECTNAME + ' Content',
        content_types      = contentTypes,
        permission         = ADD_CONTENT_PERMISSION,
        extra_constructors = constructors,
        fti                = ftis,
        ).initialize(context)

    # Extract constructors for items, areas and the root help center so that
    # they can be given different permissions.
    
    itemConstructors = {}
    areaConstructors = {}
    rootConstructors = {}
    for i in range(0, len(contentTypes)):
        if contentTypes[i].meta_type in ('HelpCenterDefinition', 
                                         'HelpCenterFAQ', 
                                         'HelpCenterTutorial',
                                         'HelpCenterReferenceManual',
                                         'HelpCenterReferenceManualSection',
                                         'HelpCenterLeafPage',
                                         'HelpCenterReferenceManualPage',
                                         'HelpCenterInstructionalVideo',
                                         'HelpCenterLink',
                                         'HelpCenterHowTo',
                                         'HelpCenterErrorReference',):
            itemConstructors[contentTypes[i].meta_type] = constructors[i]
        elif contentTypes[i].meta_type in ('HelpCenterGlossary',
                                           'HelpCenterFAQFolder',
                                           'HelpCenterTutorialFolder',
                                           'HelpCenterReferenceManualFolder',
                                           'HelpCenterInstructionalVideoFolder',
                                           'HelpCenterLinkFolder',
                                           'HelpCenterHowToFolder',
                                           'HelpCenterErrorReferenceFolder',
                                           'HelpCenterKnowledgeBase'):
            areaConstructors[contentTypes[i].meta_type] = constructors[i]
        elif contentTypes[i].meta_type in ('HelpCenter',):
            rootConstructors[contentTypes[i].meta_type] = constructors[i]

    # Set custom add permission for items and the help center root
    for meta_type, constructor in itemConstructors.items():
        context.registerClass(
            meta_type = meta_type,
            constructors = (constructor,),
            permission = ADD_DOCUMENTATION_PERMISSION,
            )
    for meta_type, constructor in areaConstructors.items():
        context.registerClass(
            meta_type = meta_type,
            constructors = (constructor,),
            permission = ADD_HELP_AREA_PERMISSION,
            )
    for meta_type, constructor in rootConstructors.items():
        context.registerClass(
            meta_type = meta_type,
            constructors = (constructor,),
            permission = ADD_CENTER_PERMISSION,
            )

