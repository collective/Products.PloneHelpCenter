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
from schemata import HelpCenterBaseSchemaFolderish, GenericHelpCenterItemSchema
from PHCContent import PHCContent
from Products.CMFPlone.interfaces.NonStructuralFolder import INonStructuralFolder

ErrorReferenceSchema = HelpCenterBaseSchemaFolderish + Schema((

    TextField('description',
        default='',
        searchable=1,
        required=1,
        accessor="Description",
        default_content_type = 'text/plain',
        allowable_content_types = ('text/plain',),
        storage=MetadataStorage(),
        widget = TextAreaWidget(
                  description = "Enter a brief description.",
                  description_msgid = "phc_desc_ErrorReference",
                  label = "Description",
                  label_msgid = "phc_label_ErrorReference",
                  rows = 5,
                  i18n_domain = "plonehelpcenter",
                  ),
        ),
        
    TextField('body',
        searchable=1,
        required=1,
        primary=1,
        widget=RichWidget(description_msgid='phc_desc_body_ErrorReference',
            description='Explanation of the error.',
            label_msgid='phc_label_body_ErrorReference',
            label='Body',
            i18n_domain = "plonehelpcenter",
            rows=25,
            ),

        **DEFAULT_CONTENT_TYPES
        ),
    ),) + GenericHelpCenterItemSchema

# For some reason, we need to jump through these hoops to get the fields in the
# the right order
ErrorReferenceSchema.moveField('subject', pos='bottom')
ErrorReferenceSchema.moveField('relatedItems', pos='bottom')

class HelpCenterErrorReference(PHCContent,OrderedBaseFolder):
    """An Error Reference can be used to explain a particular error which may 
    arise.
    """ 

    __implements__ = (PHCContent.__implements__,
                      OrderedBaseFolder.__implements__,
                      INonStructuralFolder)


    content_icon = 'errorref_icon.gif'

    schema = ErrorReferenceSchema
    archetype_name = 'Error Reference'
    meta_type = 'HelpCenterErrorReference'
    global_allow = 0
    filter_content_types = 1
    # allow_discussion = IS_DISCUSSABLE
    allowed_content_types = ('Image', 'File',)

    typeDescription= 'An Error Reference can be used to explain a particular error which may arise.'
    typeDescMsgId  = 'description_edit_errorreference'

    actions = PHCContent.actions + (
        {
            'id': 'attachments',
            'name': 'Attachments',
            'action': 'string:${object_url}/attachments',
            'permissions': (CMFCorePermissions.ModifyPortalContent,)
        },
    )

    # aliases = PHCContent.aliases.copy()
    # aliases.update({'(Default)'   : 'errorreference_view',
    #                 'view'        : 'errorreference_view',
    #                 'attachments' : 'phc_attachments'})

    security = ClassSecurityInfo()

registerType(HelpCenterErrorReference, PROJECTNAME)
