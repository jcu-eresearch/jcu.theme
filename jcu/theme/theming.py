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

from zope import interface, schema
from zope.annotation.interfaces import IAnnotations
from persistent.dict import PersistentDict

from jcu.theme.config import THEMES, THEME_ANNOTATIONS_KEY as KEY
from jcu.theme import _


class IThemeSettingsManager(interface.Interface):
    theme_name = schema.Choice(title=_(u"Theme Name"),
            description=_(u"Select the CSS class to be used in this section."),
            values=THEMES,
            default='None',
                              )

    ignore_selection = schema.Bool(title=_(u"Ignore this selection?"),
            description=_(u"Select this if you would like to purposefully \
                          ignore this theme choice here.  This context will \
                          then use a parent's theme choice."),
                                  )


class ThemeSettingsManager(object):
    interface.implements(IThemeSettingsManager)

    @property
    def theme_name(self):
        return self.getValue('theme_name')

    @property
    def ignore_selection(self):
        return self.getValue('ignore_selection')

    def __init__(self, context, form=None):
        self.context = context
        self.form = form

        self.annotations = IAnnotations(self.context)
        self.theme_annotations = self.annotations.get(KEY, None)

        if self.theme_annotations is None:
            self.annotations[KEY] = PersistentDict()
            self.theme_annotations = self.annotations[KEY]

    def getValue(self, key, default=False):
        return self.theme_annotations.get(key) or default

    def setValue(self, key, value):
        self.theme_annotations[key] = value

    def theme_values(self):
        return dict(self.theme_annotations)

    def delete(self):
        del self.annotations[KEY]
