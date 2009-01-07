try:
    from Products.CMFCore.permissions import AddPortalContent
    from Products.CMFCore.permissions import setDefaultRoles
except ImportError:    
    from Products.CMFCore.CMFCorePermissions import AddPortalContent
    from Products.CMFCore.CMFCorePermissions import setDefaultRoles
from Products.Archetypes.public import DisplayList

ADD_CENTER_PERMISSION = 'PloneHelpCenter: Add Plone Help Center'
ADD_CONTENT_PERMISSION = AddPortalContent
ADD_HELP_AREA_PERMISSION = 'PloneHelpCenter: Add Help Center Area'
ADD_DOCUMENTATION_PERMISSION = 'PloneHelpCenter: Add Documentation'

# Let members by default be allowed to add documentation, and managers only
# be able to add new documentation areas
setDefaultRoles(ADD_CENTER_PERMISSION, ('Manager',))
setDefaultRoles(ADD_HELP_AREA_PERMISSION, ('Manager', 'Owner',))
setDefaultRoles(ADD_DOCUMENTATION_PERMISSION, ('Manager', 'Member',))

PROJECTNAME = "PloneHelpCenter"
SKINS_DIR = 'skins'

GLOBALS = globals()

# If plone.memoize is available, the minutes to cache
# the results of expensive queries that help build
# the PHC top page.
# Set to zero for no caching.
# Note that editing the PHC object will force cache 
# invalidate.
CACHE_MINUTES = 30

DEFAULT_CONTENT_TYPES = {
    'default_output_type': 'text/html',
    'default_content_type': 'text/html',
    'allowable_content_types': ('text/plain',
                                'text/restructured',
                                'text/html',
                                'text/structured',)
    }

# A bug in CMF 2.1 prevents setting default discussion.
# If this gets fixed, we can turn this back on here
# and in the individual content types.
# IS_DISCUSSABLE = True

# The Rights DC metadata attribute (copyright) can be disabled on each content
# item, with the value for all items being set at the root HelpCenter level.
# Set GLOBAL_RIGHTS to 0 to turn this feature off.
GLOBAL_RIGHTS = 1

# here you can specify which types are allowed as references.
REFERENCEABLE_TYPES = ('HelpCenterFAQ',
    'HelpCenterDefinition',
    'HelpCenterTutorial',
    'HelpCenterErrorReference',
    'HelpCenterHowTo',
    'HelpCenterLink',
    'HelpCenterReferenceManual',
    'HelpCenterReferenceManualSection',
    'HelpCenterReferenceManualPage',
    'HelpCenterInstructionalVideo',    
    'HelpCenterKnowledgeBase',
)

IMAGE_SIZES = {
    'preview': (400, 400),
    'thumb': (128, 128),
    'tile': (64, 64),
    'icon': (32, 32),
    'listing': (16, 16),
    }

# Path to HelpCenter How-to
MANUAL_PATH        = 'doc/PHCManual.stx'
MANUAL_MIMETYPE    = 'text/structured'
MANUAL_ID          = 'use-help-center'
MANUAL_TITLE       = 'How to use this resource'
MANUAL_DESCRIPTION = 'A brief description of how you use and contribute to the Help Center.'
MANUAL_SECTION     = 'General'

# These are the types for which we'll support topic searches and views
TOPIC_VIEW_TYPES = ['HelpCenterTutorial','HelpCenterReferenceManual','HelpCenterHowTo']
