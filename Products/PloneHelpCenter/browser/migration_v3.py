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
        
        res = self.migrateNextPrev()
        res += '\n'
        res += self.migrateRefManPages()
        return res
    
    def migrateRefManPages(self):
        context = self.context
        
        catalog = getToolByName(context, 'portal_catalog')
        brains = catalog(
            portal_type=['HelpCenterReferenceManualPage',],
            path='/'.join(context.getPhysicalPath())        
        )
        
        res = ['Migrate Reference Manual Page Texts ...']
        for obj in [brain.getObject() for brain in brains]:
            body = getattr(obj, 'body', None)
            if body:
                obj.setText(body)
                delattr(obj, 'body')
                res.append(obj.id)
            
        return "\n".join(res)


    def migrateNextPrev(self):
        context = self.context

        catalog = getToolByName(context, 'portal_catalog')
        brains = catalog(
            portal_type=['HelpCenterReferenceManual','HelpCenterReferenceManualSection',],
            path='/'.join(context.getPhysicalPath())        
        )

        res = ['Turn on next/prev navigation ...']
        for obj in [brain.getObject() for brain in brains]:
            if not obj.getNextPreviousEnabled():
                obj.setNextPreviousEnabled(True)
                res.append(obj.id)
            
        return "\n".join(res)
