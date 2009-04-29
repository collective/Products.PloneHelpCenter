#!/usr/bin/env python
# encoding: utf-8
"""
upgrades.py

Created by Steve McMahon on 2009-04-17.
"""

from config import PROJECTNAME

from zope.component import getUtility
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName

from Products.Archetypes.public import process_types, listTypes

from StringIO import StringIO
from Products.contentmigration import walker
from Products.contentmigration.archetypes import InplaceATItemMigrator


# getPortal and IfInstalled stolen from Collage.
# Thanks, Giles!

def getPortal():
    return getUtility(ISiteRoot)

class NotInstalledComponent(LookupError):
    def __init__(self, cpt_name):
        self.cpt_name = cpt_name
        return

    def __str__(self):
        msg = ("Component '%s' is not installed in this site."
               " You can't run its upgrade steps."
               % self.cpt_name)
        return msg

class IfInstalled(object):
    def __init__(self, prod_name=PROJECTNAME):
        """@param prod_name: as shown in quick installer"""
        self.prod_name = prod_name

    def __call__(self, func):
        """@param func: the decorated function"""
        def wrapper(setuptool):
            qi = getPortal().portal_quickinstaller
            installed_ids = [p['id'] for p in qi.listInstalledProducts()]
            if self.prod_name not in installed_ids:
                raise NotInstalledComponent(self.prod_name)
            return func(setuptool)
        wrapper.__name__ = func.__name__
        wrapper.__dict__.update(func.__dict__)
        wrapper.__doc__ = func.__doc__
        wrapper.__module__ = func.__module__
        return wrapper
        
def migrateBodyTexts(self):

    catalog = getToolByName(self, 'portal_catalog')
    brains = catalog(
        portal_type=['HelpCenterReferenceManualPage',
                     'HelpCenterTutorialPage',
                     'HelpCenterHowTo',
                     'HelpCenterErrorReference',
                     ],
    )

    res = ['Migrate Page Texts ...']
    for obj in [brain.getObject() for brain in brains]:
        body = getattr(obj, 'body', None)
        if body:
            obj.setText(body)
            delattr(obj, 'body')
            res.append(obj.id)

    return "\n".join(res)


def migrateFAQs(self):

    catalog = getToolByName(self, 'portal_catalog')
    brains = catalog(
        portal_type=['HelpCenterFAQ',],
        path='/'.join(self.getPhysicalPath())        
    )

    res = ['Migrate FAQ Answers ...']
    for obj in [brain.getObject() for brain in brains]:
        body = getattr(obj, 'answer', None)
        if body:
            obj.setText(body)
            delattr(obj, 'answer')
            res.append(obj.id)

    return "\n".join(res)


def migrateNextPrev(self):

    catalog = getToolByName(self, 'portal_catalog')
    brains = catalog(
        portal_type=[
            'HelpCenterReferenceManual',
            'HelpCenterReferenceManualSection',
            'HelpCenterTutorial',
            ],
    )

    res = ['Turn on next/prev navigation ...']
    for obj in [brain.getObject() for brain in brains]:
        if not obj.getNextPreviousEnabled():
            obj.setNextPreviousEnabled(True)
            res.append(obj.id)

    return "\n".join(res)


def runTypesUpdate(setuptool):
    """Upgrade types from profile"""

    setuptool.runImportStepFromProfile('profile-Products.PloneHelpCenter:default', 'typeinfo',
                                       run_dependencies=True)
    setuptool.runImportStepFromProfile('profile-Products.PloneHelpCenter:default', 'workflow',
                                      run_dependencies=True)
    setuptool.runImportStepFromProfile('profile-Products.PloneHelpCenter:default', 'rolemap',
                                      run_dependencies=True)
    setuptool.runImportStepFromProfile('profile-Products.PloneHelpCenter:default', 'difftool',
                                      run_dependencies=True)


def reindexNearlyAll(portal):
    """
        We need the object_provides index to reflect
        some of our new interfaces.
    """
    
    mytypes = [ t['portal_type'] for t in listTypes(PROJECTNAME) ]
    
    catalog = getToolByName(portal, 'portal_catalog')
    for brain in catalog(portal_type=mytypes):
        brain.getObject().reindexObject('object_provides')


class RMPageMigrator(InplaceATItemMigrator):

    walkerClass = walker.CatalogWalker

    src_meta_type = 'HelpCenterReferenceManualPage'

    src_portal_type = 'HelpCenterReferenceManualPage'

    dst_meta_type = 'HelpCenterLeafPage'

    dst_portal_type = 'HelpCenterLeafPage'


class TPageMigrator(InplaceATItemMigrator):

    walkerClass = walker.CatalogWalker

    src_meta_type = 'HelpCenterTutorialPage'

    src_portal_type = 'HelpCenterTutorialPage'

    dst_meta_type = 'HelpCenterLeafPage'

    dst_portal_type = 'HelpCenterLeafPage'



@IfInstalled()        
def runTypesMigration(setuptool):
    """
        Migrate to 3+ types
    """
    
    runTypesUpdate(setuptool)
    
    portal = getPortal()
    
    # add next/previous flags to multi-page types
    print migrateNextPrev(portal)
    # move body texts
    print migrateBodyTexts(portal)
    print migrateFAQs(portal)

    # real type migration: convert manual and
    # tutorial pages to the new, generic leaf
    # content type.
    out = StringIO()
    for migrator in (RMPageMigrator, TPageMigrator):
        walker = migrator.walkerClass(portal, migrator)
        walker.go(out=out)
        print out
        print walker.getOutput()

    # object_provides catalog entries need updating
    reindexNearlyAll(setuptool)

    return
