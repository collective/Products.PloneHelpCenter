#
#  This is the Plone Help Center FAQ Folder type, with enhanced features
#  like dividing the FAQ into Sections, and Display relevant
#  versions.
#

import urllib

from zope.interface import implements

from AccessControl import ClassSecurityInfo, ModuleSecurityInfo
from zope.component import getMultiAdapter

try:
    from Products.LinguaPlone.public import *
except ImportError:
    # No multilingual support
    from Products.Archetypes.public import *

import Products.CMFCore.permissions as CMFCorePermissions
from Products.PloneHelpCenter.config import *
from schemata import HelpCenterBaseSchemaFolderish, HelpCenterContainerSchema

from Products import ATContentTypes
from PHCFolder import PHCFolder
from Products.PloneHelpCenter.interfaces import IHelpCenterFolder

FAQFolderSchema = HelpCenterBaseSchemaFolderish + Schema((
    TextField('description',
        searchable=1,
        required=1,
        accessor="Description",
        default_content_type = 'text/plain',
        allowable_content_types = ('text/plain',),
        storage=MetadataStorage(),
        widget=TextAreaWidget(
                description="Description of the FAQ Container.",
                description_msgid="phc_desc_folder",
                label_msgid="phc_label_folder",
                label="Description",
                i18n_domain = "plonehelpcenter",
                rows=6,)
        ),
    ),) + HelpCenterContainerSchema

class HelpCenterFAQFolder(PHCFolder, ATContentTypes.content.folder.ATFolder):
    """An FAQ Section can hold frequently asked questions with answers."""

    implements(IHelpCenterFolder)

    content_icon = 'faq_icon.gif'

    schema = FAQFolderSchema
    archetype_name = 'FAQ Section'
    meta_type = 'HelpCenterFAQFolder'
    global_allow = 0
    filter_content_types = 1
    allowed_content_types = ('HelpCenterFAQ', )

    security = ClassSecurityInfo()

    typeDescription= 'An FAQ Section can hold frequently asked questions with answers.'
    typeDescMsgId  = 'description_edit_faqfolder'

    # def getTOCSelectOptions(self, current=None):
    #     """
    #     Returns a sequence of dicts:
    #         title: tile of section/page, including numbering
    #         url:   URL of page
    #         current: True if current section/page
    #     This is a convenience for creating an option list.
    #     """
    # 
    #     res = []
    #     for section in getMultiAdapter((self, self.REQUEST,), name="hcf_view").getSectionsToList():
    #         res.append( 
    #             {'title':section, 
    #              'url':'%s/faqsection_view?section=%s' % (self.absolute_url(), urllib.quote(section)), 
    #              'current':False} )
    #     
    #     return res
    #     
    # def getAllPagesURL(self):
    #     return '%s?full=1' % self.absolute_url()

registerType(HelpCenterFAQFolder, PROJECTNAME)
