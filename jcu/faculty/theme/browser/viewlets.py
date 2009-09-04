from zope.component import getMultiAdapter
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase, LogoViewlet, GlobalSectionsViewlet
from plone.app.layout.viewlets.common import LogoViewlet as BaseLogoViewlet

# Sample code for a basic viewlet (In order to use it, you'll have to):
# - Un-comment the following useable piece of code (viewlet python class).
# - Rename the vielwet template file ('browser/viewlet.pt') and edit the
#   following python code accordingly.
# - Edit the class and template to make them suit your needs.
# - Make sure your viewlet is correctly registered in 'browser/configure.zcml'.
# - If you need it to appear in a specific order inside its viewlet manager,
#   edit 'profiles/default/viewlets.xml' accordingly.
# - Restart Zope.
# - If you edited any file in 'profiles/default/', reinstall your package.
# - Once you're happy with your viewlet implementation, remove any related
#   (unwanted) inline documentation  ;-p

#class MyViewlet(ViewletBase):
#    render = ViewPageTemplateFile('viewlet.pt')
#
#    def update(self):
#        self.computed_value = 'any output'

class LogoViewlet(BaseLogoViewlet):
    render = ViewPageTemplateFile('logo.pt')

    def update(self):
        BaseLogoViewlet.update(self)
        portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
        portal = portal_state.portal()
	portal_id = portal.getId()

        self.home_url = portal.restrictedTraverse('base_properties').homelink

        sitelogoName = portal.restrictedTraverse('base_properties').sitelogoName
        self.sitelogo_tag = portal.restrictedTraverse(portal_id+'-'+sitelogoName).tag()

        #For the dynamic logo
        context_state = getMultiAdapter((self.context, self.request),
                                        name=u'plone_context_state')
        actions = context_state.actions()

        portal_tabs_view = getMultiAdapter((self.context, self.request),
                                           name='portal_tabs_view')
        portal_tabs = portal_tabs_view.topLevelTabs(actions=actions)
  
        selectedTabs = self.context.restrictedTraverse('selectedTabs')
        selected_tabs = selectedTabs('index_html',
                                          self.context,
                                          portal_tabs)
        self.selected_portal_tab = selected_tabs['portal']

        self.section_root_url = portal.portal_url()+'/'+self.selected_portal_tab

        self.is_not_home = ('index_html' != self.selected_portal_tab)
  
        sectionlogo_image = portal.restrictedTraverse(portal_id+'-section-'+self.selected_portal_tab+'.jpg', None)

        if sectionlogo_image:
            self.sectionlogo_tag = sectionlogo_image.tag()
        else:
            self.sectionlogo_tag = ''



