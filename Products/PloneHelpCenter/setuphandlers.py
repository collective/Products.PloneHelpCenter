#!/usr/bin/env python
# encoding: utf-8
"""
setuphandlers.py

Created by Steve McMahon on 2009-04-25.
"""

from StringIO import StringIO

from Products.CMFCore.utils import getToolByName

from Products.PloneHelpCenter import config


def install(self):
    out = StringIO()

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

    turnOnVersioning(self)
    print >> out, "Turned on versioning for leaf types"

    print >> out, "Successfully installed %s" % config.PROJECTNAME

    return out.getvalue()


from Products.Archetypes.public import listTypes
from Products.Archetypes.Extensions.utils import installTypes, install_subskin
from Products.PloneHelpCenter.config import *

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


def turnOnVersioning(site):
    """ auto versioning for all leaf types """
    
    DEFAULT_POLICIES = ('at_edit_autoversion', 'version_on_revert')
    ctypes = (
        'HelpCenterHowTo',
        'HelpCenterTutorialPage',
        'HelpCenterReferenceManualPage',
        'HelpCenterFAQ',
        'HelpCenterErrorReference',
        'HelpCenterDefinition',
        )
    
    portal_repository = getToolByName(site, 'portal_repository')
    versionable_types = list(portal_repository.getVersionableContentTypes())
    for type_id in ctypes:
        if type_id not in versionable_types:
            versionable_types.append(type_id)
    portal_repository.setVersionableContentTypes(versionable_types)

    for ctype in ctypes:
        for policy_id in DEFAULT_POLICIES:
            portal_repository.addPolicyForContentType(ctype, policy_id)    


def importVarious(context):
    """
    Final plonehelpcenter import steps.
    """

    # Only run step if a flag file is present (e.g. not an extension profile)
    if context.readDataFile('plonehelpcenter-various.txt') is None:
        return

    site = context.getSite()
    print install(site)
    