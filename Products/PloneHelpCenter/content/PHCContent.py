from zope.interface import implements
from AccessControl import ClassSecurityInfo

try:
    from Products.LinguaPlone.public import *
except ImportError:
    # No multilingual support
    from Products.Archetypes.public import *

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

import Products.CMFCore.permissions as CMFCorePermissions
from Products.CMFCore.utils import getToolByName

from Products.PloneHelpCenter.config import *
from Products.CMFPlone.utils import base_hasattr
from Products.PloneHelpCenter.interfaces import IHelpCenterContent

try:
    set
except NameError:
    from sets import Set as set

# Get HistoryAwareMixin on all our types:

try:
    from Products.Archetypes.HistoryAware import HistoryAwareMixin
except ImportError:
    try:
        from Products.ATContentTypes.HistoryAware import HistoryAwareMixin
    except ImportError:
        class HistoryAwareMixin:
            """Dummy class when we can't find the real McCoy"""
            
            __implements__ =()
            actions        =()


class PHCContentMixin:
    """ Provide vocabulary and default methods for HelpCenterItemSchemaNarrow """

    implements(IHelpCenterContent)

    security = ClassSecurityInfo()

    security.declareProtected(CMFCorePermissions.View, 'getVersionsVocab')
    def getVersionsVocab(self):
        """Get version vocabulary"""
        if base_hasattr(self.aq_parent, 'getVersionsVocab'):
            return self.aq_parent.getVersionsVocab()
        else:
            return ()

    security.declareProtected(CMFCorePermissions.View, 'getSectionsVocab')
    def getSectionsVocab(self):
        """Get sections vocabulary"""
        if base_hasattr(self.aq_parent, 'getSectionsVocab'):
            return self.aq_parent.getSectionsVocab()
        else:
            return ()

    security.declareProtected(CMFCorePermissions.ModifyPortalContent, 'SetSections')
    def setSections(self, values):
        """set sections"""

        # The sections field may be in use with a "topic : subtopic" pattern.
        # If so, make sure that the 'topic' is set as a separate item
        # so that we'll be able to look it up by topic as well as
        # by "topic : subtopic"

        valueSet = set(values)
        for s in values:
            pos = s.find(':')
            if pos >= 0:
                valueSet.add( s[:pos].strip() )
        self.sections = tuple(valueSet)


    security.declareProtected(CMFCorePermissions.View, 'getAudiencesVocab')
    def getAudiencesVocab(self):
        """Get audiences vocabulary"""
        if base_hasattr(self.aq_parent, 'getAudiencesVocab'):
            return self.aq_parent.getAudiencesVocab()
        else:
            return ()

    security.declareProtected(CMFCorePermissions.View, 'getSubjectVocab')
    def getSubjectVocab(self):
        """Get subject (keywords) vocabulary"""
        catalog = getToolByName(self, 'portal_catalog')
        return catalog.uniqueValuesFor('Subject')

    security.declareProtected(CMFCorePermissions.View, 'Versions')
    def Versions(self):
        """method to display the versions in a nicer way
        """
        field = self.getField('versions')
        if field:
            return ", ".join(field.get(self))
        else:
            return ''

    security.declareProtected(CMFCorePermissions.View, 'Audiences')
    def Audiences(self):
        """method to display the audiences in a nicer way
        """
        field = self.getField('audiences')
        if field:
            return ", ".join(field.get(self))
        else:
            return ''

    security.declareProtected(CMFCorePermissions.View, 'isOutdated')
    def isOutdated(self):
        """Check the current versions of the PHC root container against the
        versions of this item. If the version of this item is not in the list
        of current versions, return 1, else return 0. As a shortcircuit, if
        no "currentVersions" is defined, always return 0.
        """

        myVersions = self.getVersions()

        if not myVersions:
            return 0

        # Acquire current versions
        currentVersions = [x.decode('utf-8') for x in self.getCurrentVersions()]

        if not currentVersions:
            return 0

        for v in myVersions:
            if v in currentVersions:
                # Not outdated - we match one of the current versions
                return 0

        # Outdated - we didn't match anything
        return 1

    security.declareProtected(CMFCorePermissions.View, 'getRelatedItems') 
    def getRelatedItems(self):
        """method to fetch the referenced items in context of
           config and permissions
        """
        try:
            objs = [o for o in self.getField('relatedItems').get(self) 
                      if self.portal_membership.checkPermission('View', o)]
            return objs
        except:
            return []


def HideOwnershipFields(schema):
    """ Some PHC types should not have their own ownership metadata """
    for fname in ('creators', 'contributors', 'rights'):
        schema[fname].widget.visible = {'view':'invisible','edit':'invisible'}


def HideMetadataFields(schema):
    """ Some PHC types should have very little visible metadata """
    for field in ('creators', 'contributors', 'rights', 'location', 'subject', 'language'):
        schema[field].widget.visible = {'view':'invisible','edit':'invisible'}


class PHCContent(BrowserDefaultMixin, HistoryAwareMixin, PHCContentMixin):
    """A simple  mixin class to provide contentish functions 
       archetype with no schema defined.
    """


    security = ClassSecurityInfo()

    _at_rename_after_creation = True

    __implements__ = (HistoryAwareMixin.__implements__,)


