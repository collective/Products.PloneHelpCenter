## Script (Python) "edit_reminder"
##title=Check edited object and print state-aware message.
##parameters=

wtool = context.portal_workflow

if wtool.getInfoFor(context, 'review_state') == 'in-progress':
    msg = 'Content+saved.%20+It+must+be+published+before+it+will+be+visible+to+others.%20+Please+submit+it+for+review+when+completed.'
else:
    msg='Your+changes+have+been+saved.'   

return context.REQUEST.RESPONSE.redirect('%s?portal_status_message=%s' % (context.absolute_url(),msg) )
