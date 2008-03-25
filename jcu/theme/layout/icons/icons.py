from zope.interface import implements

from plone.app.layout.icons.interfaces import IContentIcon

from plone.app.layout.icons.icons import BaseIcon

class CatalogBrainContentIcon(BaseIcon):
    implements(IContentIcon)

    def __init__(self, context, request, brain):
        self.context = context
        self.request = request
        self.brain = brain

    width = 16
    height = 16

    @property
    def url(self):
        portal_url = getToolByName(self.context, 'portal_url')()
        path = self.brain.getIcon
        return "%s/%s" % (portal_url, path)

    @property
    def description(self):
        return self.brain['portal_type']

    @property
    def title(self):
        return None


