from plone.app.layout.globals.layout import LayoutPolicy
from Products.CMFCore.interfaces._content import ISiteRoot

from jcu.theme.theming import IThemeSettingsManager


def getThemeForContext(context):
    current_aq = context
    theme_name = None

    #Loop while we don't have a theme name yet, traversing up to the
    #parents of our context
    while theme_name is None:
        try:
            theme_values = IThemeSettingsManager(current_aq).theme_values()

            if 'theme_name' in theme_values and \
               'ignore_selection' in theme_values and \
               theme_values['ignore_selection'] is False:
                theme_name = theme_values['theme_name']
        except:
            pass

        if theme_name is not None:
            #Quick 'out' to avoid having to wake the parent object
            #or do a check on interfaces
            break
        elif ISiteRoot.providedBy(current_aq):
            theme_name = theme_name or ''
            break
        else:
            current_aq = current_aq.aq_parent

    return {'theme_name': theme_name, 'context': current_aq}

class JCULayoutPolicy(LayoutPolicy):
    """A view that gives access to various layout related functions.
    """

    def bodyClass(self, template, view):
        """Returns the CSS class to be used on the body tag.
        """
        return super(JCULayoutPolicy, self).bodyClass(template, view) \
                + ' %s' % getThemeForContext(self.context)['theme_name']


