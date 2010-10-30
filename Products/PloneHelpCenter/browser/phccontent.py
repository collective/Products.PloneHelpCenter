""" support for HelpCenter content templates """

from Acquisition import aq_inner, aq_parent

from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName

from Products.PloneHelpCenter.interfaces import IHelpCenterNavRoot


class HelpCenterPagedView(BrowserView):
    """ support for HelpCenter paged content templates """
    
    def __init__(self, context, request):
        """ set up a few convenience object attributes """
        BrowserView.__init__(self, context, request)


    def navRootObject(self):
        """ Find the root of the page navigation """

        context = aq_inner(self.context)
        
        parent = aq_parent(context)
        while parent and not IHelpCenterNavRoot.providedBy(parent):
            parent = aq_parent(parent)
        return parent
