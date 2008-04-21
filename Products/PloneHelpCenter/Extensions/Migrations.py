try:
    from Products.contentmigration.migrator import InlineFieldActionMigrator, BaseInlineMigrator
    from Products.contentmigration.walker import CustomQueryWalker
    haveContentMigrations = True
except ImportError:
    haveContentMigrations = False
    
import types

from StringIO import StringIO
from Products.CMFCore.utils import getToolByName
from Products.Archetypes import transaction
from Products.Archetypes.BaseUnit import BaseUnit
from Products.CMFPlone.utils import safe_hasattr

from Acquisition import aq_base

def mergeKeywords(obj, value, **kwargs):
    if type(value) == type(()):
        value = list(value)
    elif type(value) == type('') or type(value) == type(u''):
        value = [value]
    
    newValue = []
    for v in value:
        if type(v) != type('') and type(v) != type(u''):
            continue
        if ',' in v:
            for i in v.split(','):
                newValue.append(i.strip())
        else:
            newValue.append(v.strip())
        
    md = getattr(aq_base(obj), '_md', None)
    if md:
        oldKeywords = md.get('subject', [])
        for kw in oldKeywords:
            if kw not in newValue:
                newValue.append(kw)

    return newValue

def v0_8_to_v0_9(self, out):
    """Migrate from 0.8 to 0.9
    """
    
    if not haveContentMigrations:
        print >> out, "WARNING: Install contentmigrations to be able to migrate from 0.8 to 0.9"
        return

    class HelpCenterMigrator(InlineFieldActionMigrator):
        src_portal_type = src_meta_type = ('HelpCenter')
        fieldActions = ({ 'fieldName' : 'versions_vocab',
                          'newFieldName' : 'versionsVocab',
                        },
                        { 'fieldName' : 'audiences_vocab',
                          'newFieldName' : 'audiencesVocab',
                        },

                        )

    class ContainerMigrator(InlineFieldActionMigrator):
        src_portal_type = src_meta_type = ('HelpCenterGlossary',
                                           'HelpCenterFAQFolder',
                                           'HelpCenterTutorialFolder',
                                           'HelpCenterReferenceManualFolder',
                                           'HelpCenterInstructionalVideoFolder',
                                           'HelpCenterLinkFolder',
                                           'HelpCenterHowToFolder',
                                           'HelpCenterErrorReferenceFolder',)
        fieldActions = ({ 'fieldName' : 'sections_vocab',
                          'newFieldName' : 'sectionsVocab',
                        },
                        )
                        
    class ItemMigrator(InlineFieldActionMigrator):
        src_portal_type = src_meta_type = ('HelpCenterDefinition', 
                                           'HelpCenterFAQ', 
                                           'HelpCenterTutorial',
                                           'HelpCenterReferenceManual',
                                           'HelpCenterInstructionalVideo',
                                           'HelpCenterLink',
                                           'HelpCenterHowTo',
                                           'HelpCenterErrorReference',)
        fieldActions = ({ 'fieldName' : 'referenced_items',
                          'newFieldName' : 'relatedItems',
                        },
                        { 'fieldName' : 'related_keywords',
                          'newFieldName' : 'subject',
                          'transform' : mergeKeywords,
                        },
                        )

    portal = getToolByName(self, 'portal_url').getPortalObject()

    # Migrate 
    walker = CustomQueryWalker(portal, HelpCenterMigrator, query = {})
    transaction.savepoint(optimistic=True)
    print >> out, "Migrating fields in help center root"
    walker.go()
    
    walker = CustomQueryWalker(portal, ContainerMigrator, query = {})
    transaction.savepoint(optimistic=True)
    print >> out, "Migrating fields in containers"
    walker.go()

    walker = CustomQueryWalker(portal, ItemMigrator, query = {})
    transaction.savepoint(optimistic=True)
    print >> out, "Migrating fields in items"
    walker.go()

    print >> out, "- You may also want to update your catalog in portal_catalog"
    print >> out, "- You may also want to update role mappings in portal_workflow"
    
def migrate(self):
    """Run migrations
    """
    out = StringIO()
    print >> out, "Starting PHC migration"
    v0_8_to_v0_9(self, out)
    print >> out, "PHC migrations finished"
    return out.getvalue()