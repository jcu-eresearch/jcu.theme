from zope.component import getMultiAdapter
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
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

class WilLogoViewlet(BaseLogoViewlet):
    render = ViewPageTemplateFile('templates/logo.pt')

    def update(self):
        BaseLogoViewlet.update(self)
        portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
        portal = portal_state.portal()

        self.home_url = portal_state.navigation_root_url()

        sitelogoName = portal.restrictedTraverse('base_properties').logoName
        self.sitelogo_tag = portal.restrictedTraverse(sitelogoName).tag()

class WilFooterViewlet(ViewletBase):
    render = ViewPageTemplateFile('templates/footer.pt')

    def update(self):
        portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')

        self.navigation_root_url = portal_state.navigation_root_url()