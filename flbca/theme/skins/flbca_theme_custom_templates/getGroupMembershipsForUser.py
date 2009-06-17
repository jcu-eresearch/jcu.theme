## Script (Python) "getGroupMembershipsForUser"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Get the current user's group memberships
##

return context.portal_membership.getAuthenticatedMember().getGroups()
