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
from schemata import HelpCenterBaseSchemaFolderish, HelpCenterItemSchema
from PHCContent import PHCContent
from Products.CMFPlone.interfaces.NonStructuralFolder import INonStructuralFolder

from zope import event
try:
    from zope.lifecycleevent import ObjectModifiedEvent
except ImportError:
    from zope.app.event.objectevent import ObjectModifiedEvent


HowToSchema = HelpCenterBaseSchemaFolderish + Schema((
    TextField(
        'description',
        default='',
        searchable=1,
        required=1,
        accessor="Description",
        default_content_type = 'text/plain',
        allowable_content_types = ('text/plain',),
        storage=MetadataStorage(),
        widget=TextAreaWidget(
            description = 'Brief explanation of the How To.',
            description_msgid = "phc_help_detailed_howto",
            label = "Summary",
            label_msgid = "phc_label_detailed_howto",
            i18n_domain = "plonehelpcenter",
            ),
        ),

    TextField(
        'body',
        searchable=1,
        required=1,
        primary=1,
        accessor='getBody',
        widget=RichWidget(
            description_msgid='phc_desc_howto_body',
            description='The text of the Howto',
            label_msgid='phc_body',
            label='Body',
            i18n_domain = "plonehelpcenter",
            rows=25,
            ),

        **DEFAULT_CONTENT_TYPES
        ),
    ),) + HelpCenterItemSchema

# For some reason, we need to jump through these hoops to get the fields in the
# the right order
HowToSchema.moveField('subject', pos='bottom')
HowToSchema.moveField('relatedItems', pos='bottom')

MAPPING = {'text_html' : 'text/html'}

# TODO: Generalize and i18nize
def addHelpCenterHowTo(self, id, **kwargs):
    obj = HelpCenterHowTo(id)
    self._setObject(id, obj)
    obj = self._getOb(id)
    obj.initializeArchetype(**kwargs)
    event.notify(ObjectModifiedEvent(obj))
    #setattr(obj, 'body', howto_template)
    # we need to get the template from the skin, so that it's customizable
    template = getattr(self, 'HowToTemplate', None)
    if template is not None:
        setattr(obj, 'body', template(self))
    return obj.getId()

class HelpCenterHowTo(PHCContent,BaseFolder):
    """A How-to is a document describing how to address a single, common 
    use-case or issue. You may add images and files as attachments.
    """

    __implements__ = (PHCContent.__implements__,
                      BaseFolder.__implements__,
                      INonStructuralFolder)

    content_icon = 'howto_icon.gif'

    typeDescription= 'A How-to is a document describing how to address a single, common use-case or issue. You may add images and files as attachments.'
    typeDescMsgId  = 'description_edit_howto'


    schema = HowToSchema
    archetype_name = 'How-to'
    meta_type = 'HelpCenterHowTo'
    global_allow = 0
    filter_content_types = 1
    # allow_discussion = IS_DISCUSSABLE
    allowed_content_types = ('Image', 'File',)
    default_view = 'howto_view'

    # actions = PHCContent.actions + (
    #     {
    #         'id': 'attachments',
    #         'name': 'Attachments',
    #         'action': 'string:${object_url}/attachments',
    #         'permissions': (CMFCorePermissions.ModifyPortalContent,)
    #         },
    # )
    # 
    # 
    # aliases = PHCContent.aliases.copy()
    # aliases.update({'(Default)'   : 'howto_view',
    #                 'view'        : 'howto_view',
    #                 'attachments' : 'phc_attachments'})

    security = ClassSecurityInfo()

    def getText(self):
        return 'nisse'

    security.declareProtected(CMFCorePermissions.ModifyPortalContent, 'setFormat')
    def setFormat(self, value):
        value = MAPPING.get(value, value)
        BaseFolder.setFormat(self, value)

registerType(HelpCenterHowTo, PROJECTNAME)
