## Script (Python) "selectRedirect"
##title=Redirector to aid noscript jump widgets
##parameters=target

# only jump within site
if target.startswith(context.portal_url()):
    context.REQUEST.RESPONSE.redirect(target)


