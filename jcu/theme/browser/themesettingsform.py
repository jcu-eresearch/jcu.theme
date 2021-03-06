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

from z3c.form import form, field, button
from plone.app.z3cform.layout import wrap_form

from Products.CMFPlone.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from jcu.theme import _
from jcu.theme.config import MESSAGE_OKAY, MESSAGE_FAILED, MESSAGE_CANCEL, \
        MESSAGE_BALEETED
from jcu.theme.theming import IThemeSettingsManager
from jcu.theme.browser.layout import getThemeForContext


class ThemeSettingsForm(form.Form):
    fields = field.Fields(IThemeSettingsManager)
    #ignoreContext = True # don't use context to get widget data

    def __init__(self, context, request):
        super(ThemeSettingsForm, self).__init__(context, request)
        self.theme_settings_manager = IThemeSettingsManager(self.context)

    def getContent(self):
        return self.theme_settings_manager

    @button.buttonAndHandler(_(u'Apply'))
    def handleApply(self, action):
        data, errors = self.extractData()
        for field in data:
            self.theme_settings_manager.setValue(field, data[field])

        self.setStatusMessage(MESSAGE_OKAY)
        #self.setStatusMessage(MESSAGE_FAILED)

    @button.buttonAndHandler(_(u'Cancel'))
    def handleCancel(self, action):
        self.setStatusMessage(MESSAGE_CANCEL)
        self.redirectAction()

    @button.buttonAndHandler(_(u'Delete Settings'))
    def handleDelete(self, action):
        self.theme_settings_manager.delete()
        self.setStatusMessage(MESSAGE_BALEETED)
        self.redirectAction()

    def setStatusMessage(self, message):
        ptool = getToolByName(self.context, 'plone_utils')
        ptool.addPortalMessage(message)

    def redirectAction(self):
        self.request.response.redirect(self.context.absolute_url())

#ThemeSettingsFormView = wrap_form(ThemeSettingsForm)

from plone.z3cform.layout import FormWrapper


class ThemeSettingsFormView(FormWrapper):
    form = ThemeSettingsForm
    index = ViewPageTemplateFile('templates/themesettingsform.pt')

    label = _(u"Theming Options")
    description = _(u"Select the theme options you would like to \
                    use for this context.")

    @property
    def current_settings(self):
        return IThemeSettingsManager(self.context).theme_values()

    @property
    def inherited_setting(self):
        return getThemeForContext(self.context)

    @property
    def is_inherited_setting(self):
        return self.inherited_setting['theme_name'] != \
                self.current_settings.get('theme_name', '')
