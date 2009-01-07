#
# The Plone Help Center container.
#
# A Help Center is pre-populated with the following folders:
#
# /faq - contains the FAQ objects
# /how-to - contains the How-tos
# /tutorial - contains the tutorials
# /reference - contains the reference manuals
# /error - contains the error references
# /link - contains the links to other documentation
# /glossary - contains the definitions
# /video - contains video files for training/instruction
# /manual - contains reference manuals
#
# The main goals of these folders are to restrict the addable types and
# provide a sensible default view out-of-the-box, like the FAQ view.
#

try:
    from Products.LinguaPlone.public import *
except ImportError:
    # No multilingual support
    from Products.Archetypes.public import *

import transaction

try:
    import Products.CMFCore.permissions as CMFCorePermissions
except ImportError:
    from Products.CMFCore import CMFCorePermissions

from zope.interface import implements
from Products.PloneHelpCenter.interfaces import IHelpCenterContent

from Products.CMFCore.WorkflowCore import WorkflowException
from Products.CMFCore.utils import getToolByName
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin, fti_meta_type
from AccessControl import ClassSecurityInfo
from Products.PloneHelpCenter.config import *
from Products.CMFPlone.utils import _createObjectByType

import os
from Globals import package_home

try:
    set
except NameError:
    from sets import Set as set

HCRootSchema = BaseFolderSchema + Schema((
    TextField(
        'description',
        searchable=1,
        required=1,
        accessor="Description",
        default_content_type = 'text/plain',
        allowable_content_types = ('text/plain',),
        storage=MetadataStorage(),
        widget=TextAreaWidget(
                description_msgid="phc_desc_helpcenter",
                description="Description for the Help Center.",
                label_msgid="phc_label_desc_helpcenter",
                label="Description",
                i18n_domain = "plonehelpcenter",
                rows=6,
                ),
        ),

    LinesField(
        'audiencesVocab',
        accessor='getAudiencesVocab',
        edit_accessor='getRawAudiencesVocab',
        mutator='setAudiencesVocab',
        required=0,
        languageIndependent=1,
        widget=LinesWidget(
                description_msgid="phc_audience_helpcenter",
                description="One type of audience on each line. If you leave this blank, audience information will not be used. Audience is typically 'End user', 'Developer' and similar.",
                label="Documentation Audiences",
                label_msgid="phc_label_audience_helpcenter",
                i18n_domain = "plonehelpcenter",
                ),
        ),

    LinesField(
        'versionsVocab',
        accessor='getVersionsVocab',
        edit_accessor='getRawVersionsVocab',
        mutator='setVersionsVocab',
        required=0,
        languageIndependent=1,
        widget=LinesWidget(
                description_msgid="phc_version_helpcenter",
                description="One version on each line, if you're documenting different versions of software. If you leave this blank, version information will not be used.",
                label="Versions",
                label_msgid="phc_label_version_helpcenter",
                i18n_domain = "plonehelpcenter",
                ),
        ),

    LinesField(
        'currentVersions',
        required=0,
        multiValued=1,
        languageIndependent=1,
        vocabulary='getVersionsVocab',
        widget=MultiSelectionWidget(
            description_msgid="phc_current_versions_helpcenter",
            description="Readers will be informed when content relates to versions not in this list, as it may be outdated.",
            label="Current Versions",
            label_msgid="phc_label_current_versions_helpcenter",
            i18n_domain = "plonehelpcenter",
            ),
        ),

    LinesField(
        'sectionsVocab',
        accessor='getSectionsVocab',
        edit_accessor='getRawSectionsVocab',
        mutator='setSectionsVocab',
        widget=LinesWidget(
           label="Sections",
           description="One section on each line. Used for grouping items. May be overriden in individual help center folders.",
           description_msgid = "phc_topsections_vocab",
           label_msgid = "phc_label_sections-vocab",
           i18n_domain="plonehelpcenter",
           rows=6,
           )
        ),

    TextField(
        'rights',
        accessor="Rights",
        widget=TextAreaWidget(
                label='Copyright',
                description="Copyright info for all content in the helpcenter.",
                label_msgid="phc_label_copyrights_helpcenter",
                description_msgid="phc_copyrights_helpcenter",
                i18n_domain="plonehelpcenter"
                ),
        ),

    BooleanField(
        'constrainSearches',
        default=1,
        required=0,
        languageIndependent=1,
        widget=BooleanWidget(
                label='Constrain Searches',
                description="""Constrain the results of Help Center searches to this document area.
                    Turn this off to search the entire site.
                    This affects only the Help Center's search facility, not the global search.
                """,
                label_msgid="phc_label_constrainSearches_helpcenter",
                description_msgid="phc_constrainSearches_helpcenter",
                i18n_domain="plonehelpcenter"
            ),
        ),
    ),)


class HelpCenter(BrowserDefaultMixin, OrderedBaseFolder):
    """A simple folderish archetype"""

    implements(IHelpCenterContent)

    __implements__ = (BrowserDefaultMixin.__implements__,
        OrderedBaseFolder.__implements__)

    schema = HCRootSchema

    content_icon = 'helpcenter_icon.gif'

    # Not really needed any longer, and is causing
    # problems when schema updates.
    # _properties = OrderedBaseFolder._properties +  (
    #     {'id'    : 'right_slots',
    #      'type'  : 'lines',
    #      'mode'  : 'rw',
    #      'label' : 'Right slots'
    #      },
    #      )

    archetype_name = 'Help Center'
    meta_type = 'HelpCenter'
    filter_content_types = 1
    _at_rename_after_creation = True

    allowed_content_types = ('HelpCenterFAQFolder',
                             'HelpCenterHowToFolder',
                             'HelpCenterTutorialFolder',
                             'HelpCenterReferenceManualFolder',
                             'HelpCenterLinkFolder',
                             'HelpCenterErrorReferenceFolder',
                             'HelpCenterGlossary',
                             'HelpCenterInstructionalVideoFolder',
                             'HelpCenterKnowledgeBase',
                             )

    security = ClassSecurityInfo()

    default_view = 'helpcenter_view'
    suppl_views = ('helpcenter_topicview', 'helpcenter_topicview_main',)

    actions = (
        {'id'          : 'view',
         'name'        : 'View',
         'action'      : 'string:${object_url}',
         'permissions' : (CMFCorePermissions.View,)
         },
        {'id'          : 'edit',
         'name'        : 'Edit',
         'action'      : 'string:${object_url}/edit',
         'permissions' : (CMFCorePermissions.ModifyPortalContent,),
         },
        {'id'          : 'metadata',
         'name'        : 'Properties',
         'action'      : 'string:${object_url}/properties',
         'permissions' : (CMFCorePermissions.ModifyPortalContent,),
         },
        {'id'          : 'local_roles',
         'name'        : 'Sharing',
         'action'      : 'string:${object_url}/sharing',
         'permissions' : (CMFCorePermissions.ManageProperties,),
         },
        {'id'          : 'stats',
         'name'        : 'Statistics',
         'action'      : 'string:${object_url}/stats',
         'permissions' : (CMFCorePermissions.ManageProperties,),
         },
        )

    aliases = {
        '(Default)'  : '(dynamic view)',
        'view'       : '(selected layout)',
        'index.html' : '',
        'edit'       : 'base_edit',
        'properties' : 'base_metadata',
        'sharing'    : 'folder_localrole_form',
        'stats'      : 'phc_stats',
        'gethtml'    : '',
        'mkdir'      : '',
        }



    ##############
    # the following methods are meant to be used in an enclosed object
    # that is invoking the method by aquisition.

    security.declareProtected(CMFCorePermissions.View, 'getPHCObject')
    def getPHCObject(self):
        """return the enclosing PHC object"""

        return self


    security.declareProtected(CMFCorePermissions.View, 'getPHCUrl')
    def getPHCUrl(self):
        """return the enclosing PHC object URL"""

        return self.absolute_url()


    security.declareProtected(CMFCorePermissions.View, 'getPHCPath')
    def getPHCPath(self):
        """return the enclosing PHC object path as a string"""

        return '/'.join(self.getPhysicalPath())


registerType(HelpCenter, PROJECTNAME)
