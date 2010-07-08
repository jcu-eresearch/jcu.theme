import pdb
#############################################################################
#
# Copyright (c) 2010 JCU eResearch Centre and contributors.
# All Rights Reserved.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

from Products.Five import BrowserView
from Products.CMFCore.interfaces._content import ISiteRoot
from plone.memoize.view import memoize

from jcu.theme.theming import IThemeSettingsManager

#Todo:
#* Provide global options to disable theming (or set a global theme)
#* Test it out!
class ThemeSettingsView(BrowserView):

    @property
    @memoize
    def get_theme(self):
        current_aq = self.context.aq_inner
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
                break;
            elif ISiteRoot.providedBy(current_aq):
                theme_name = theme_name or ''
                break;
            else:
                current_aq = current_aq.aq_parent

        return theme_name
