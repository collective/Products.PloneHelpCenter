# encoding: utf-8
"""
migration_v3.py

Created by Steve McMahon on 2009-01-08.
"""

# To do: set next/prev nav true in manuals, sections


from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName

class PHCv3migrate(BrowserView):
    
    def __call__(self):
        
        res = self.migrateRefManPages()
        return res
    
    def migrateRefManPages(self):
        context = self.context
        
        catalog = getToolByName(context, 'portal_catalog')
        brains = catalog(
            portal_type=['HelpCenterReferenceManualPage',],
            path='/'.join(context.getPhysicalPath())        
        )
        
        res = []
        for obj in [brain.getObject() for brain in brains]:
            body = getattr(obj, 'body', None)
            if body:
                obj.setText(body)
                delattr(obj, 'body')
                res.append(obj.id)
            
        return "\n".join(res)