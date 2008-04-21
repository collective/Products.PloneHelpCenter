try:
    from Products.LinguaPlone.public import *
except ImportError:
    # No multilingual support
    from Products.Archetypes.public import *
try:
    import Products.CMFCore.permissions as CMFCorePermissions
except ImportError:
    from Products.CMFCore import CMFCorePermissions
from AccessControl import ClassSecurityInfo
from Products.PloneHelpCenter.config import *
from schemata import HelpCenterBaseSchema, GenericHelpCenterItemSchema
from PHCContent import PHCContent
from AccessControl import ClassSecurityInfo, ModuleSecurityInfo

InstructionalVideoSchema = HelpCenterBaseSchema + Schema((
    TextField(
        'description',
        default='',
        required=1,
        searchable=1,
        accessor="Description",
        default_content_type = 'text/plain',
        allowable_content_types = ('text/plain',),
        storage=MetadataStorage(),
        widget=TextAreaWidget(
                 description = "Brief explanation of the video's content.",
                 description_msgid = "phc_help_detailed_video",
                 label = "Summary",
                 label_msgid = "phc_label_detailed_video",
                 i18n_domain = "plonehelpcenter"
              ),
        ),
        
    FileField(
        'video_file',
        required=1,
        primary=1,
        widget=FileWidget(
            description="Click 'Browse' to upload a Flash .swf file.",
            description_msgid="phc_help_videofile_description",
            label="Flash File (.swf)",
            label_msgid="phc_label_videofile_description",
            i18n_domain="plonehelpcenter",
            ),
        ),

    ImageField(
        'screenshot',
        required=0,
        sizes=IMAGE_SIZES,
        widget=ImageWidget(
            label='Screenshot',
            label_msgid='phc_label_video_screenshot',
            description='Add a screenshot by clicking the \'Browse\' '
                          'button. Add a screenshot that highlights the '
                          'content of the instructional video.',
            description_msgid='phc_help_video_screenshot',
            i18n_domain='plonehelpcenter',
            ),
        ),

    StringField(
        'duration',
        required=0,
        widget=StringWidget(
            description_msgid='phc_help_video_duration',
            description='Length (in minutes) of the video.',
            label_msgid='phc_label_video_duration',
            label='Duration',
            i18n_domain='plonehelpcenter',
            ),
        ),

    IntegerField(
        'width',
        required=0,
        default='800',
        validators=('isInt',),
        widget=IntegerWidget(
            description_msgid='phc_help_video_width',
            description='Width of the video.',
            label_msgid='phc_label_video_width',
            label='Width',
            i18n_domain='plonehelpcenter',
            ),
        ),

    IntegerField(
        'height',
        required=0,
        default='600',
        validators=('isInt',),
        widget=IntegerWidget(
            description_msgid='phc_help_video_height',
            description='Height of the video.',
            label_msgid='phc_label_video_height',
            label='Height',
            i18n_domain='plonehelpcenter',
            ),
        ),
    ),

    marshall=PrimaryFieldMarshaller(),

    ) + GenericHelpCenterItemSchema

# For some reason, we need to jump through these hoops to get the fields in the
# the right order
InstructionalVideoSchema.moveField('subject', pos='bottom')
InstructionalVideoSchema.moveField('relatedItems', pos='bottom')

class HelpCenterInstructionalVideo(PHCContent,BaseContent):
    """This is an Instructional Video content type, to which you can attach 
    movies and other relevant files.
    """

    content_icon = 'movie_icon.gif'

    schema = InstructionalVideoSchema
    archetype_name = 'Video'
    meta_type = 'HelpCenterInstructionalVideo'
    global_allow = 0
    # allow_discussion = IS_DISCUSSABLE

    typeDescription= 'An Instructional Video can be used to upload Flash instructional videos.'
    typeDescMsgId  = 'description_edit_instructionalvideo'

    # aliases = PHCContent.aliases.copy()
    # aliases.update({'(Default)' : 'ivideo_view',
    #                 'view'      : 'ivideo_view'})

    security = ClassSecurityInfo()

registerType(HelpCenterInstructionalVideo, PROJECTNAME)
