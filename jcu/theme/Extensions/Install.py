from Products.CMFCore.utils import getToolByName


def install(portal):
    setup_tool = getToolByName(portal, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile('profile-jcu.theme:default')
    return "Ran all import steps."


def uninstall(portal):
    setup_tool = getToolByName(portal, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile('profile-jcu.theme:uninstall')
    return "Ran all uninstall steps."
