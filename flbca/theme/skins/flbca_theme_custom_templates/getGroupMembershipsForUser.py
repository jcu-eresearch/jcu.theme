## Script (Python) "getGroupMembershipsForUser"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Get the current user's group memberships
##

mtool = context.portal_membership
return mtool.getMemberById(mtool.getAuthenticatedMember().getId()).getGroups()

