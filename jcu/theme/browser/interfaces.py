from plone.theme.interfaces import IDefaultPloneLayer
from zope.viewlet.interfaces import IViewletManager


class IThemeSpecific(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 browser layer.
       If you need to register a viewlet only for the
       "JCU Theme" theme, this interface must be its layer
       (in theme/viewlets/configure.zcml).
    """


class IPortalTop(IViewletManager):
    """Special portal top viewlet manager specifically for elements
       that need to have 100% width within Plone 4's div layout
    """
