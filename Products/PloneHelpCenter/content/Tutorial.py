try:
    from Products.LinguaPlone.public import *
except ImportError:
    # No multilingual support
    from Products.Archetypes.public import *
from Products.PloneHelpCenter.config import *
try:
    import Products.CMFCore.permissions as CMFCorePermissions
except ImportError:
    from Products.CMFCore import CMFCorePermissions
from schemata import HelpCenterBaseSchema, HelpCenterItemSchema
from PHCContent import PHCContent
from AccessControl import ClassSecurityInfo

TutorialSchema = HelpCenterBaseSchema + Schema((
    TextField(
        'description',
        default='',
        searchable=1,
        required=1,
        primary=1,
        accessor="Description",
        default_content_type = 'text/plain',
        allowable_content_types = ('text/plain',),
        storage=MetadataStorage(),
        widget=TextAreaWidget(
                 description = 'A summary of the tutorial--aims and scope. Will be displayed on every page of the tutorial.',
                 description_msgid = "phc_help_tutorial_summary",
                 label = "Tutorial Description",
                 label_msgid = "phc_label_tutorial_description",
                 rows = 5,
                 i18n_domain = "plonehelpcenter",
                )
        ),
    ),)  + HelpCenterItemSchema

# For some reason, we need to jump through these hoops to get the fields in the
# the right order
TutorialSchema.moveField('subject', pos='bottom')
TutorialSchema.moveField('relatedItems', pos='bottom')

class HelpCenterTutorial(PHCContent,OrderedBaseFolder):
    """A tutorial containing TutorialPages, Files and Images."""

    __implements__ = (PHCContent.__implements__,
                      OrderedBaseFolder.__implements__,)

    schema = TutorialSchema
    archetype_name = 'Tutorial'
    meta_type = portal_type = 'HelpCenterTutorial'
    content_icon = 'tutorial_icon.gif'

    global_allow = 0
    filter_content_types = 1
    allowed_content_types = ('HelpCenterTutorialPage', 'Image', 'File')
    # allow_discussion = IS_DISCUSSABLE

    typeDescription= 'A Tutorial can contain Tutorial Pages, Images and Files. Index order is decided by the folder order, use the normal up/down arrow in the folder content view to rearrange content.'
    typeDescMsgId  = 'description_edit_tutorial'

    security = ClassSecurityInfo()

    security.declareProtected(CMFCorePermissions.View, 'getTutorialDescription')
    def getTutorialDescription(self):
        """ Returns the description of the Tutorial--convenience method for TutorialPage """
        return self.Description()

    security.declareProtected(CMFCorePermissions.View, 'getPages')
    def getPages(self, states=[]):
        """Get items"""
        criteria = contentFilter = {'portal_type' : 'HelpCenterTutorialPage'}
        if states:
            criteria['review_state'] = states
        return self.getFolderContents(contentFilter = criteria)

    security.declareProtected(CMFCorePermissions.View, 'getPagePosition')
    def getPagePosition(self, obj, states=[]):
        """Get position in folder of the current context"""
        pages = self.getPages()
        for i in range(len(pages)):
            if pages[i].getId == obj.getId():
                return i
        return None

registerType(HelpCenterTutorial, PROJECTNAME)

