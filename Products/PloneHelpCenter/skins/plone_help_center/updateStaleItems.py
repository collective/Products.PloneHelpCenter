## Script (Python) "updateStaleItems"
##title=Update stale-items portlet, then refresh
##parameters=newInterval

# Stash newInterval (as 'stale_PHC_items_interval' in a session variable,
# then reload the current page
session=context.REQUEST.SESSION
session['stale_PHC_items_interval']=newInterval

return context.REQUEST.RESPONSE.redirect(context.absolute_url())
