from StringIO import StringIO
from Products.CMFCore.utils import getToolByName

from Products.PloneHelpCenter import config

EXTENSION_PROFILE = 'profile-Products.PloneHelpCenter:default'

## how about the form controller settings?

def install(self):
    out = StringIO()

    tool=getToolByName(self, "portal_setup")

    try:
        tool.runAllImportStepsFromProfile(EXTENSION_PROFILE,
            purge_old=False)
    except AttributeError:   # before plone 3
        old_context = tool.getImportContextID()
        tool.setImportContext(EXTENSION_PROFILE)
        tool.runAllImportSteps(purge_old=False)
        tool.setImportContext(old_context)

    # Add catalog metadata columns and indexes
    catalog = getToolByName(self, 'portal_catalog')
    addCatalogIndex(self, out, catalog, 'isOutdated', 'FieldIndex')
    addCatalogMetadata(self, out, catalog, 'isOutdated')
    addCatalogIndex(self, out, catalog, 'getAudiences', 'KeywordIndex')
    addCatalogMetadata(self, out, catalog, 'getAudiences')
    addCatalogIndex(self, out, catalog, 'getSections', 'KeywordIndex')
    addCatalogMetadata(self, out, catalog, 'getSections')
    addCatalogIndex(self, out, catalog, 'getStartHere', 'FieldIndex')
    addCatalogMetadata(self, out, catalog, 'getStartHere')
    addCatalogIndex(self, out, catalog, 'getVersions', 'KeywordIndex')
    addCatalogMetadata(self, out, catalog, 'getVersions')
    print >> out, "Added PHC items to catalog indexes and metadata"

    print >> out, "Successfully installed %s" % config.PROJECTNAME

    return out.getvalue()


### leaving the old cruft in place for now
### only renaming (re)install not to confuse the quickintaller


from Products.Archetypes.public import listTypes
from Products.Archetypes.Extensions.utils import installTypes, install_subskin
from Products.PloneHelpCenter.config import *

## from Products.PloneHelpCenter.Extensions import HCWorkflow
## from Products.PloneHelpCenter.Extensions import HCFolderWorkflow
## from Products.PloneHelpCenter.Extensions import HCSubItemWorkflow


def addCatalogIndex(self, out, catalog, index, type, extra = None):
    """Add the given index name, of the given type, to the catalog."""

    if index not in catalog.indexes():
        catalog.addIndex(index, type, extra)
        print >> out, "Added index", index, "to catalog"
    else:
        print >> out, "Index", index, "already in catalog"

def addCatalogMetadata(self, out, catalog, column):
    """Add the given column to the catalog's metadata schema"""
    
    if column not in catalog.schema():
        catalog.addColumn(column)
        print >> out, "Added", column, "to catalog metadata"
    else:
        print >> out, column, "already in catalog metadata"

def removeCatalogIndex(self, out, catalog, index):
    """Delete the given index"""
    
    if index in catalog.indexes():
        catalog.delIndex(index)
        print >> out, "Removed index", index
    else:
        print >> out, "Index", index, "not in catalog"
    
def removeCatalogMetadata(self, out, catalog, column):
    """Delete the given metadata column"""
    
    if column in catalog.schema():
        catalog.delColumn(column)
        print >> out, "Removed column", column
    else:
        print >> out, "Column", column, "not in catalog"

def addToListProperty(self, out, propertySheet, property, value):
    """Add the given value to the list in the given property"""
    current = list(propertySheet.getProperty(property))
    if value not in current:
        current.append(value)
        propertySheet.manage_changeProperties(**{property : current})

    print >> out, "Added %s to %s" % (value, property)


def registerNavigationTreeSettings(self, out):
    """Make the folderish content types not appear in navigation tree.
    We don't want users to think of the HowTo as a folder, even though
    technically, it is."""

    phcTypes = ('HelpCenterHowTo','HelpCenterTutorial','HelpCenterErrorReference',
               'HelpCenterFAQ', 'HelpCenterDefinition', 'HelpCenterLink',
               'HelpCenterInstructionalVideo', 'HelpCenterReferenceManual',
               'HelpCenterTutorialPage', 'HelpCenterReferenceManualPage',
               )
    portalProperties = getToolByName(self, 'portal_properties')
    navtreeProps = getattr(portalProperties, 'navtree_properties')
    
    for t in phcTypes:
        addToListProperty(self, out, navtreeProps, 'metaTypesNotToList', t)
        addToListProperty(self, out, navtreeProps, 'parentMetaTypesNotToQuery', t)

def installPortlets(self, out):
    # prepend to the left_slots list, so it appears on top for Reviewers
    self.left_slots = [ 'here/portlet_stale_items/macros/portlet',] + list(self.left_slots)
    print >>out, "Added portlet"

def registerFormControllerActions(self, out):
    fc_tool = getToolByName(self, 'portal_form_controller')
    fc_tool.addFormAction('content_edit', 'success', 'HelpCenterHowTo', None, 'traverse_to', 'string:edit_reminder')
    fc_tool.addFormAction('content_edit', 'success', 'HelpCenterFAQ', None, 'traverse_to', 'string:edit_reminder')
    fc_tool.addFormAction('content_edit', 'success', 'HelpCenterTutorial', None, 'traverse_to', 'string:edit_reminder')
    fc_tool.addFormAction('content_edit', 'success', 'HelpCenterReferenceManual', None, 'traverse_to', 'string:edit_reminder')
    fc_tool.addFormAction('content_edit', 'success', 'HelpCenterInstructionalVideo', None, 'traverse_to', 'string:edit_reminder')
    fc_tool.addFormAction('content_edit', 'success', 'HelpCenterLink', None, 'traverse_to', 'string:edit_reminder')
    fc_tool.addFormAction('content_edit', 'success', 'HelpCenterErrorReference', None, 'traverse_to', 'string:edit_reminder')
    fc_tool.addFormAction('content_edit', 'success', 'HelpCenterDefinition', None, 'traverse_to', 'string:edit_reminder')
    print >> out, 'Set reminder to publish message hack on objects.'

def installWorkflows(self, out):
    wf_tool = getToolByName(self, 'portal_workflow')

    HCWorkflow.install()
    HCFolderWorkflow.install()
    HCSubItemWorkflow.install()

    if not 'helpcenter_workflow' in wf_tool.objectIds():
        wf_tool.manage_addWorkflow('helpcenter_workflow (Workflow for Help Center Items.)',
                                   'helpcenter_workflow')
    if not 'helpcenterfolder_workflow' in wf_tool.objectIds():
        wf_tool.manage_addWorkflow('helpcenterfolder_workflow (Workflow for Help Center Folders.)',
                                   'helpcenterfolder_workflow')
    if not 'helpcentersubitem_workflow' in wf_tool.objectIds():
        wf_tool.manage_addWorkflow('helpcentersubitem_workflow (Workflow for Help Center Sub-items.)',
                                   'helpcentersubitem_workflow')

    print >> out, 'Installed helpcenter_workflow.'
    print >> out, 'Installed helpcenterfolder_workflow.'
    print >> out, 'Installed helpcentersubitem_workflow'

    wf_tool.setChainForPortalTypes(pt_names=['HelpCenterFAQ'
                                            ,'HelpCenterHowTo'
                                            ,'HelpCenterLink'
                                            ,'HelpCenterTutorial'
                                            ,'HelpCenterReferenceManual'
                                            ,'HelpCenterInstructionalVideo'
                                            ,'HelpCenterErrorReference'
                                            ,'HelpCenterDefinition'], chain='helpcenter_workflow')
    print >> out, 'Set helpcenter_workflow as default for help center content types.'

    wf_tool.setChainForPortalTypes(pt_names=['HelpCenterFAQFolder'
                                            ,'HelpCenterHowToFolder'
                                            ,'HelpCenterLinkFolder'
                                            ,'HelpCenterTutorialFolder'
                                            ,'HelpCenterReferenceManualFolder'
                                            ,'HelpCenterInstructionalVideoFolder'
                                            ,'HelpCenterErrorReferenceFolder'
                                            ,'HelpCenterGlossary'], chain='helpcenterfolder_workflow')
    print >> out, 'Set helpcenterfolder_workflow as default for help center folder types.'

    wf_tool.setChainForPortalTypes(pt_names=['HelpCenterTutorialPage'
                                            ,'HelpCenterReferenceManualSection'
                                            ,'HelpCenterReferenceManualPage'], 
                                    chain='helpcentersubitem_workflow')
    print >> out, 'Set helpcentersubitem_workflow as default for sections and pages.'

def setupPortalFactory(self, out):
    # make new types use portal_factory
    ft = getToolByName(self, 'portal_factory')
    portal_factory_types = ft.getFactoryTypes().keys()
    for t in [
             # With this in the factory, creating the default "how to use this resource" document fails :-(
             # 'HelpCenter',
             'HelpCenterGlossary',
             'HelpCenterDefinition',
             'HelpCenterErrorReference',
             'HelpCenterErrorReferenceFolder',
             'HelpCenterFAQ',
             'HelpCenterFAQFolder',
             'HelpCenterHowTo',
             'HelpCenterHowToFolder',
             'HelpCenterInstructionalVideo',
             'HelpCenterInstructionalVideoFolder',
             'HelpCenterLink',
             'HelpCenterLinkFolder',
             'HelpCenterTutorial',
             'HelpCenterTutorialFolder',
             'HelpCenterTutorialPage',
             'HelpCenterReferenceManual',
             'HelpCenterReferenceManualFolder',
             'HelpCenterReferenceManualSection',
             'HelpCenterReferenceManualPage']:

        if t not in portal_factory_types:
            portal_factory_types.append(t)
            ft.manage_setPortalFactoryTypes(listOfTypeIds=portal_factory_types)

    print >> out, 'New types use portal_factory'

def old_install(self, reinstall=False):
    out = StringIO()

    installTypes(self, out,
                 listTypes(PROJECTNAME),
                 PROJECTNAME)

    from Products.CMFDynamicViewFTI.migrate import migrateFTIs
    migrateFTIs(self, product=PROJECTNAME)

    install_subskin(self, out, GLOBALS)

    registerNavigationTreeSettings(self, out)
    installWorkflows(self, out)
    registerFormControllerActions(self, out)
    setupPortalFactory(self, out)
    
    
    # Add catalog metadata columns and indexes
    catalog = getToolByName(self, 'portal_catalog')
    addCatalogIndex(self, out, catalog, 'isOutdated', 'FieldIndex')
    addCatalogMetadata(self, out, catalog, 'isOutdated')
    print >> out, "Added isOutdated to catalog metadata"

    # Add "stale items" portlet, so HelpCenter Managers and Reviewers can
    # review old stuff to see if it's still useful
    # installPortlets(self, out)
    # removed for now, expensive and should be a separate page or similar,
    # not a portlet. Nice and valuable functionality, though.
    
    print >> out, "Successfully installed %s." % PROJECTNAME
    return out.getvalue()

def old_uninstall(self, reinstall=False):
    out = StringIO()

    # remove the stale-items portlet from the portal root object
    #portletPath = 'here/portlet_stale_items/macros/portlet'
    #if portletPath in self.left_slots:
    #    self.left_slots = [p for p in self.left_slots if (p != portletPath)]
    #    print >> out, 'Removed stale-items portlet'

    if not reinstall:
        # Remove catalog metadata columns and indexes
        catalog = getToolByName(self, 'portal_catalog')
        removeCatalogIndex(self, out, catalog, 'isOutdated')
        removeCatalogMetadata(self, out, catalog, 'isOutdated')
        
        removeCatalogIndex(self, out, catalog, 'getAudiences')
        removeCatalogMetadata(self, out, catalog, 'getAudiences')
        
        removeCatalogIndex(self, out, catalog, 'getSections')
        removeCatalogMetadata(self, out, catalog, 'getSections')
        
        removeCatalogIndex(self, out, catalog, 'getStartHere')
        removeCatalogMetadata(self, out, catalog, 'getStartHere')
        
        removeCatalogIndex(self, out, catalog, 'isOutdated')
        removeCatalogMetadata(self, out, catalog, 'isOutdated')
        
        print >> out, "Removed PHC items from catalog indexes and metadata"


    print >> out, "Successfully uninstalled %s." % PROJECTNAME
    return out.getvalue()
