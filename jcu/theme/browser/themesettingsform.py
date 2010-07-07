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

from z3c.form import form, field, button
from plone.app.z3cform.layout import wrap_form

from Products.CMFPlone.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from jcu.theme import _
from jcu.theme.config import MESSAGE_OKAY, MESSAGE_FAILED, MESSAGE_CANCEL, \
        MESSAGE_BALEETED
from jcu.theme.theming import IThemeSettingsManager

class ThemeSettingsForm(form.Form):
    fields = field.Fields(IThemeSettingsManager)
    #ignoreContext = True # don't use context to get widget data

    def __init__(self, context, request):
        super(ThemeSettingsForm, self).__init__(context, request)
        self.theme_settings_manager = IThemeSettingsManager(self.context)

    def getContent(self):
        return self.theme_settings_manager

#    def updateWidgets(self):
#        super(ThemeSettingsForm, self).updateWidgets()
#
#        print "Current values:"
#        for field in self.fields._data_keys.data:
#            print str(field)+' - '+str(self.theme_settings_manager.getValue(field))

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
        ptool = getToolByName(self.context,'plone_utils')
        ptool.addPortalMessage(message)

    def redirectAction(self):
        self.request.response.redirect(self.context.absolute_url())

#ThemeSettingsFormView = wrap_form(ThemeSettingsForm)

from plone.z3cform.layout import FormWrapper
class ThemeSettingsFormView(FormWrapper):
    form = ThemeSettingsForm
    index = ViewPageTemplateFile('themesettingsform.pt')

    label = _(u"Theming Options")
    description = _(u"Select the theme options you would like to use for this context.")

    @property
    def current_settings(self):
        return IThemeSettingsManager(self.context).theme_values()


#Todo:
#* Refactor this class into somewhere more sensible
#* Make the traveral work upwards to the root
#* Make the traveral pay attention to the 'ignore' option.
#* Test it out!
from Products.Five import BrowserView
from Products.CMFCore.interfaces._content import ISiteRoot
from plone.memoize.view import memoize
class ThemeSettingsView(BrowserView):

    @property
    @memoize
    def get_theme(self):
        current_aq = self.context.aq_inner
        theme_name = None

        #Loop while we don't have a theme name yet, traversing up to the
        #parents of our context
        while theme_name is None:
            theme_values = IThemeSettingsManager(current_aq).theme_values()
            if 'theme_name' in theme_values and \
               'ignore_selection' in theme_values and \
               theme_values['ignore_selection'] is False:
                theme_name = theme_values['theme_name']

            if ISiteRoot.providedBy(current_aq):
                theme_name = theme_name or ''
                break;
            else:
                current_aq = current_aq.aq_parent

        return theme_name
