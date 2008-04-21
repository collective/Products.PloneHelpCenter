## Script (Python) ""
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters= 
##title=

return [(v.title, k) for k, v in context.portal_workflow['helpcenter_workflow'].states.items()]

