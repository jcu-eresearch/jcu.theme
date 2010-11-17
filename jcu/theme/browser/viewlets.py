from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets import common

class LogoViewlet(common.LogoViewlet):
    render = ViewPageTemplateFile('templates/logo.pt')

    def update(self):
        super(LogoViewlet,self).update()

        portal = self.portal_state.portal()
        #XXX This needs to either be rendered in the page template or something else
        self.home_url = "http://www.jcu.edu.au/"
        self.sitelogo_tag = portal.restrictedTraverse('sitelogo.png').tag()

class PathBarViewlet(common.PathBarViewlet):
    index = ViewPageTemplateFile('templates/path_bar.pt')

class SiteActionsViewlet(common.SiteActionsViewlet):
    index = ViewPageTemplateFile('templates/site_actions.pt')

