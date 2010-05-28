## Controller Python Script "sort_folder_contents_by_title"
##title=Sort folder contents by title
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##

from Products.CMFPlone import PloneMessageFactory as _

context.orderObjects('title')
context.plone_utils.reindexOnReorder(context)

message=_(u'Folder contents sorted by title')
context.plone_utils.addPortalMessage(message)
return state

