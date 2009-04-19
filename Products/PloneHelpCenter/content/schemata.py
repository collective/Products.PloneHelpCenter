try:
    from Products.LinguaPlone.public import *
except ImportError:
    # No multilingual support
    from Products.Archetypes.public import *
try:
    import Products.CMFCore.permissions as CMFCorePermissions
except ImportError:
    from Products.CMFCore import CMFCorePermissions
from Products.Archetypes.Marshall import PrimaryFieldMarshaller
from Products.PloneHelpCenter.config import *

from Products import ATContentTypes as atct

try:
    from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
    PHCReferenceWidget = ReferenceBrowserWidget
except ImportError:
    PHCReferenceWidget = ReferenceWidget

try:
    from Products.AddRemoveWidget import AddRemoveWidget
    PHCKeywordWidget = AddRemoveWidget
except ImportError:
    PHCKeywordWidget = KeywordWidget


###########################################
# Common components to Help Types schemas #
###########################################

HelpCenterItemSchema = Schema((

    LinesField(
        'versions',
        languageIndependent=1,
        index='KeywordIndex',
        vocabulary='getVersionsVocab',
        condition='object/getVersionsVocab',
        multiValued=1,
        required=0,
        widget=MultiSelectionWidget(
                label_msgid='phc_label_versions',
                label= "Versions",
                condition='object/getVersionsVocab',
                description='Versions of product that apply to this item ' \
                            '(leave blank if not version-specific).',
                description_msgid = "phc_versions",
                i18n_domain = "plonehelpcenter"
                ),
        ),
    
    LinesField(
        'sections',
        multiValued=1,
        required=0,
        vocabulary='getSectionsVocab',
        condition='object/getSectionsVocab',
        index='KeywordIndex:schema',
        widget=MultiSelectionWidget(
                label='Sections',
                condition='object/getSectionsVocab',
                description='Section(s) that this item should appear in.',
                description_msgid = "phc_sections",
                label_msgid = "phc_label_sections",
                i18n_domain = "plonehelpcenter",
                ),
        ),
    
    LinesField(
        'audiences',
        multiValued=1,
        required=0,
        vocabulary='getAudiencesVocab',
        condition="object/getAudiencesVocab",
        index='KeywordIndex:schema',
        widget=MultiSelectionWidget(
                label='Audiences',
                description='Audience(s) this item is targetted at.',
                description_msgid = "phc_audiences",
                condition="object/getAudiencesVocab",
                label_msgid = "phc_label_audiences",
                i18n_domain = "plonehelpcenter",
                ),
        ),
    
    LinesField(
        'contributors',
        accessor="Contributors",
        languageIndependent=1,
        widget=LinesWidget(
                label='Contributors',
                label_msgid="label_contributors",
                description="Enter additional names (no need to include the current owner) for those who have contributed to this entry, one per line.",
                description_msgid="help_contributors",
                i18n_domain="plone",
                ),
        ),
    
    LinesField(
        'subject',
        accessor='Subject',
        searchable=1,
        vocabulary='getSubjectVocab',
        enforceVocabulary=0,
        isMetadata=1,
        widget=PHCKeywordWidget(
                label='Related keywords',
                label_msgid = "phc_label_related",
                i18n_domain="plonehelpcenter",
        ),
    ),

    BooleanField(
        'startHere',
        index='FieldIndex:schema',
        permission = CMFCorePermissions.ReviewPortalContent,
        widget=BooleanWidget(
                label='Start Here',
                description="Marks this as a good starting point for its section. Only key documents should have this property.",
                description_msgid = "phc_starthere",
                label_msgid = "phc_label_starthere",
                i18n_domain="plonehelpcenter"
        ),
    ),
    
    ReferenceField(
        'relatedItems',
        relationship='PloneHelpCenter',
        allowed_types=REFERENCEABLE_TYPES,
        required = 0,
        multiValued=1,
        languageIndependent=1,
        widget=PHCReferenceWidget (
                label="Referenced Items",
                description="Set one or more references to HelpCenter items.",
                description_msgid = "phc_reference",
                label_msgid = "phc_label_reference",
                i18n_domain="plonehelpcenter"
                ),
    ),
    
))

# a version that doesn't duplicate any
# extensibleMetadata fields.
HelpCenterItemSchemaNarrow = Schema((
    LinesField(
        'versions',
        languageIndependent=1,
        index='KeywordIndex',
        vocabulary='getVersionsVocab',
        condition='object/getVersionsVocab',
        multiValued=1,
        required=0,
        widget=MultiSelectionWidget(
                label_msgid='phc_label_versions',
                label= "Versions",
                condition='object/getVersionsVocab',
                description='Versions of product that apply to this item ' \
                            '(leave blank if not version-specific).',
                description_msgid = "phc_versions",
                i18n_domain = "plonehelpcenter"
                ),
        ),
    
    LinesField(
        'sections',
        multiValued=1,
        required=0,
        vocabulary='getSectionsVocab',
        condition='object/getSectionsVocab',
        index='KeywordIndex:schema',
        widget=MultiSelectionWidget(
                label='Sections',
                condition='object/getSectionsVocab',
                description='Section(s) that this item should appear in.',
                description_msgid = "phc_sections",
                label_msgid = "phc_label_sections",
                i18n_domain = "plonehelpcenter",
                ),
        ),
    
    LinesField(
        'audiences',
        multiValued=1,
        required=0,
        vocabulary='getAudiencesVocab',
        condition="object/getAudiencesVocab",
        index='KeywordIndex',
        widget=MultiSelectionWidget(
                label='Audiences',
                description='Audience(s) this item is targetted at.',
                description_msgid = "phc_audiences",
                condition="object/getAudiencesVocab",
                label_msgid = "phc_label_audiences",
                i18n_domain = "plonehelpcenter",
                ),
        ),
    
    BooleanField(
        'startHere',
        index='FieldIndex',
        permission = CMFCorePermissions.ReviewPortalContent,
        widget=BooleanWidget(
                label='Start Here',
                description="Marks this as a good starting point for its section. Only key documents should have this property.",
                description_msgid = "phc_starthere",
                label_msgid = "phc_label_starthere",
                i18n_domain="plonehelpcenter"
        ),
    ),
    
))

GenericHelpCenterItemSchema = HelpCenterItemSchema.copy()
del GenericHelpCenterItemSchema['audiences']

# what sections should there be? (for enclosing folders, not indiv items!)
HelpCenterContainerSchema = Schema((

    LinesField(
        'sectionsVocab',
        accessor='getSectionsVocab',
        edit_accessor='getRawSectionsVocab',
        mutator='setSectionsVocab',
        widget=LinesWidget(
                   label="Sections",
                   description="One section on each line. Used for grouping items. If you leave this blank, the help center's sections will be used. If both are blank, sections will not be used.",
                   description_msgid = "phc_sections_vocab",
                   label_msgid = "phc_label_sections-vocab",
                   i18n_domain="plonehelpcenter",
                   rows=6,
                   )
        ),
    ))

# non folderish Help Center Base schemata
HelpCenterBaseSchema = BaseSchema.copy()

# folderish Help Center Base schemata
HelpCenterBaseSchemaFolderish = atct.content.folder.ATFolderSchema.copy()


# Remove "contributors" from metadata, so that we can add it later
if GLOBAL_RIGHTS:
    del HelpCenterBaseSchema['contributors']
    del HelpCenterBaseSchema['rights']
