from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.app.layout.viewlets.browser.common import ContentActionsViewlet

class jcuContentActionsViewlet(ContentActionsViewlet):
    index = ViewPageTemplateFile('contentactions.pt')

