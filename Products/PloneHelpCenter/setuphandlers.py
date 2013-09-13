#!/usr/bin/env python
# encoding: utf-8
"""
setuphandlers.py

Created by Steve McMahon on 2009-04-25.
"""

from Products.CMFCore.utils import getToolByName

from Products.PloneHelpCenter import config


def install(site, logger):
    # Add catalog metadata columns and indexes
    catalog = getToolByName(site, 'portal_catalog')
    addCatalogIndex(site, logger, catalog, 'isOutdated', 'FieldIndex')
    addCatalogMetadata(site, logger, catalog, 'isOutdated')
    addCatalogIndex(site, logger, catalog, 'getAudiences', 'KeywordIndex')
    addCatalogMetadata(site, logger, catalog, 'getAudiences')
    addCatalogIndex(site, logger, catalog, 'getSections', 'KeywordIndex')
    addCatalogMetadata(site, logger, catalog, 'getSections')
    addCatalogIndex(site, logger, catalog, 'getStartHere', 'FieldIndex')
    addCatalogMetadata(site, logger, catalog, 'getStartHere')
    addCatalogIndex(site, logger, catalog, 'getVersions', 'KeywordIndex')
    addCatalogMetadata(site, logger, catalog, 'getVersions')
    logger.info("Added PHC items to catalog indexes and metadata.")

    turnOnVersioning(site)
    logger.info("Turned on versioning for leaf types.")

    logger.info("Successfully installed %s.", config.PROJECTNAME)


def addCatalogIndex(site, logger, catalog, index, type, extra=None):
    """Add the given index name, of the given type, to the catalog."""

    if index not in catalog.indexes():
        catalog.addIndex(index, type, extra)
        logger.info("Added index %s to catalog.", index)
    else:
        logger.info("Index %s already in catalog.", index)


def addCatalogMetadata(site, logger, catalog, column):
    """Add the given column to the catalog's metadata schema"""

    if column not in catalog.schema():
        catalog.addColumn(column)
        logger.info("Added %s to catalog metadata.", column)
    else:
        logger.info("%s already in catalog metadata.", column)


def removeCatalogIndex(site, logger, catalog, index):
    """Delete the given index"""

    if index in catalog.indexes():
        catalog.delIndex(index)
        logger.info("Removed index %s.", index)
    else:
        logger.info("Index %s not in catalog.", index)


def removeCatalogMetadata(site, logger, catalog, column):
    """Delete the given metadata column"""

    if column in catalog.schema():
        catalog.delColumn(column)
        logger.info("Removed column %s.", column)
    else:
        logger.info("Column %s not in catalog.", column)


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
    logger = context.getLogger('PloneHelpCenter')
    install(site, logger)
