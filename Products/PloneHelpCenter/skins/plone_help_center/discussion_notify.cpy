## Script (Python) "notify_content_author"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##title=Notify the author of a piece of content that a comment has been added
##parameters=
from Products.PloneHelpCenter.utils import discussion_notify
discussion_notify(context)
return state
