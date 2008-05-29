"""
 support for the phc_attachements.pt template

 also serves as a 2.5/3.0 compatability layer 
 
"""

from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
import Acquisition



class AttachmentsView(BrowserView):
    """ support for howto attachements template """

    def __init__(self, context, request):
        """ set up a few convenience object attributes """
        
        BrowserView.__init__(self, context, request)

        self.catalog = getToolByName(self.context, 'portal_catalog')
        self.actionTool = getToolByName(self.context, 'portal_actions')
        self.portal_url = getToolByName(self.context, 'portal_url')()      
        self.context_path = '/'.join(self.context.getPhysicalPath())

    def folderButtons(self):
        """ valid folder_button actions """
        
        return [button 
                    for button in self.actionTool.listActionInfos(object=Acquisition.aq_inner(self.context))
                        if (button['category'] == 'folder_buttons') and (button['id'] != 'change_state')
                ]