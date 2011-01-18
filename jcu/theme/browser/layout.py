from plone.app.layout.globals.layout import LayoutPolicy

from jcu.theme.browser.views import getThemeForContext


class JCULayoutPolicy(LayoutPolicy):
    """A view that gives access to various layout related functions.
    """

    def bodyClass(self, template, view):
        """Returns the CSS class to be used on the body tag.
        """
        return super(JCULayoutPolicy, self).bodyClass(template, view) \
                + ' %s' % getThemeForContext(self.context)

