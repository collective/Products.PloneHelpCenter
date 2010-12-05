from zope.interface import implements
from zope.component import adapts

from plone.app.layout.nextprevious.interfaces import INextPreviousProvider

from Products.PloneHelpCenter.interfaces import IHelpCenterMultiPage
from Products.ATContentTypes.browser.nextprevious import ATFolderNextPrevious

class HelpCenterFolderNextPrevious(ATFolderNextPrevious):
    """Let a HelpCenter Section act as a next/previous provider. This
    will be automatically found by the @@plone_nextprevious_view and
    viewlet. 

    This is only used within types (ReferenceManual and Tutorial) that
    provide a getTOCSelectOptions method which lists the pages in order,
    so we use that.
    """
    
    implements(INextPreviousProvider)
    adapts(IHelpCenterMultiPage)

    def getNextItem(self, obj):
        toc = list(obj.getTOCSelectOptions(current=obj))
        use_next = False
        for item in toc:
            if use_next:
                if item == toc[-1]:
                    # last item has no next one
                    return None
                else:
                    return item
            if item['current']:
                use_next = True
    
    def getPreviousItem(self, obj):
        toc = list(reversed(obj.getTOCSelectOptions(current=obj)))
        use_next = False
        for item in toc:
            if use_next:
                if item == toc[-1]:
                    # first item has no previous one
                    return None
                else:
                    return item
            if item['current']:
                use_next = True
