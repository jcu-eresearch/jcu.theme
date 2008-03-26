from Products.CMFCore.utils import getToolByName
from plone.app.layout.icons.icons import CatalogBrainContentIcon as BaseCatalogBrainContentIcon
from plone.app.layout.icons.icons import DefaultContentIcon as BaseDefaultContentIcon
from plone.app.layout.icons.icons import FTIContentIcon as BaseFTIContentIcon
from plone.app.layout.icons.icons import CMFContentIcon as BaseCMFContentIcon
from plone.app.layout.icons.icons import PloneSiteContentIcon as BasePloneSiteContentIcon


class CatalogBrainContentIcon(BaseCatalogBrainContentIcon):

    @property
    def url(self):
        portal_url = getToolByName(self.context, 'portal_url')()
        path = self.brain.getIcon
	return None
        return "%s/%s" % (portal_url, path)


class CMFContentIcon(BaseCMFContentIcon):

    @property
    def url(self):
        portal_url = getToolByName(self.context, 'portal_url')()
        path = self.obj.getIcon(1)
        return "%s/%s" % (portal_url, path)


class FTIContentIcon(BaseFTIContentIcon):

    @property
    def url(self):
        portal_url = getToolByName(self.context, 'portal_url')()
        path = self.obj.getIcon()
        return "%s/%s" % (portal_url, path)


class PloneSiteContentIcon(BasePloneSiteContentIcon):

    @property
    def url(self):
        portal_url = getToolByName(self.context, 'portal_url')()
        return "%s/site_icon.gif" % portal_url


class DefaultContentIcon(BaseDefaultContentIcon):

    @property
    def url(self):
        portal_url = getToolByName(self.context, 'portal_url')()
        if self.obj is None:
            return None
        return "%s/error_icon.gif" % portal_url

