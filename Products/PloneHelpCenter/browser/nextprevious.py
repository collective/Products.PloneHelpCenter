from zope.interface import implements
from zope.component import adapts

from plone.app.layout.nextprevious.interfaces import INextPreviousProvider

from plone.memoize.instance import memoize

from Acquisition import aq_parent, aq_inner

from Products.CMFCore.utils import getToolByName

from Products.PloneHelpCenter.interfaces import IHelpCenterMultiPage, \
    IHelpCenterNavRoot
from Products.ATContentTypes.browser.nextprevious import ATFolderNextPrevious

class HelpCenterFolderNextPrevious(ATFolderNextPrevious):
    """Let a HelpCenter Section act as a next/previous provider. This
    will be automatically found by the @@plone_nextprevious_view and
    viewlet. 

    Work recursively, so the next item of the last page of a given
    section will be the next section, and the previous item of the
    first page will be the previous section.
    """
    
    implements(INextPreviousProvider)
    adapts(IHelpCenterMultiPage)

    def getNextItem(self, obj):
        next = super(HelpCenterFolderNextPrevious, self).getNextItem(obj)

        if next is None and not IHelpCenterNavRoot.providedBy(self.context):
            # no next item in this section and we're not at a root element
            parent = aq_parent(aq_inner(self.context))
            return INextPreviousProvider(parent).getNextItem(self.context)
        else: # normal behaviour
            return next
        
    def getPreviousItem(self, obj):
        previous = super(HelpCenterFolderNextPrevious, self).getPreviousItem(obj)
        if previous is not None: 
            return previous
        else: # no previous item in this folder
            parent = aq_parent(aq_inner(self.context))
            return INextPreviousProvider(parent).getPreviousItem(self.context)


    def buildNextPreviousQuery(self, position, range, sort_order = None):
        sort_on                  = 'getObjPositionInParent'

        query                    = {}
        query['sort_on']         = sort_on
        query['sort_limit']      = 1
        query['path']            = dict(query = '/'.join(self.context.getPhysicalPath()),
                                        depth = 1)

        # Query the position using a range
        if position == 0:
            query[sort_on]       = 0
        else:
            query[sort_on]       = dict(query = position, range = range)

        # Filters on content
        query['is_default_page'] = False
        # note we've deleted here the ATCT original:
        # query['is_folderish'] = False

        # Should I sort in any special way ?
        if sort_order:
            query['sort_order']  = sort_order

        return query
