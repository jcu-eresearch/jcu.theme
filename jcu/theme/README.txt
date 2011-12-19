Introduction
============

Some helpers:

    >>> portal = layer['portal']

First, we must perform some setup. We use the testbrowser that is shipped
with Five, as this provides proper Zope 2 integration. Most of the
documentation, though, is in the underlying zope.testbrower package.

    >>> from plone.testing.z2 import Browser
    >>> browser = Browser(layer['app'])
    >>> browser.handleErrors = False
    >>> portal_url = portal.absolute_url()
    >>> login_url = portal_url + '/login_form'

The following is useful when writing and debugging testbrowser tests. It lets
us see all error messages in the error_log.

    >>> portal.error_log._ignored_exceptions = ()

With that in place, we can go to the portal front page and log in. We will
do this using the default user from PloneTestCase:

    >>> from plone.app.testing.interfaces import SITE_OWNER_NAME, SITE_OWNER_PASSWORD

    >>> browser.open(login_url)

We have the login portlet, so let's use that.

    >>> browser.getControl(name='__ac_name').value = SITE_OWNER_NAME
    >>> browser.getControl(name='__ac_password').value = SITE_OWNER_PASSWORD
    >>> browser.getControl(name='submit').click()

Here, we set the value of the fields on the login form and then simulate a
submit click.

We then test that we are still on the portal front page:

    >>> browser.url == login_url
    True

And we ensure that we get the friendly logged-in message:

    >>> "You are now logged in" in browser.contents
    True

Jump over to the homepage.

    >>> browser.open(portal_url)

Theme tests
===========

Let's define some helpers first.

    >>> def tagContents(tag, haystack):
    ...     return haystack.partition('<%s' % tag)[2].partition('>')[0].strip()

Our product should be installed, so check that we can see various elements
of our theme.

Resources
---------

Check to see if our browser resources are present.

    >>> 'portal_css/JCU%20Theme' \
    ... in browser.contents
    True
    >>> 'portal_javascripts/JCU%20Theme' in browser.contents
    True

Action Items
------------

Check for custom portal action links; visible only when logged on.

    >>> browser.getLink('Get Support')
    <Link text='Get Support' url='http://eresearch.jcu.edu.au/support'>
    >>> browser.getLink('About Me')
    <Link text='About Me' url='http://nohost/plone/author/...

Viewlets
--------

Check the presence of our viewlets.  We customise the logo to have 2 images.

    >>> browser.getLink(id='global-logo')
    <Link text='[IMG]' url='http://www.jcu.edu.au/'>
    >>> browser.getLink(id='portal-logo')
    <Link text='...[IMG]...' url='http://nohost/plone'>

We customise the site actions to be a second menu.

    >>> 'portal-siteactions-wrapper' in browser.contents
    True
    >>> '<dl class="actionMenu deactivated" id="portal-siteactions">' in browser.contents
    True
    >>> '<ul id="portal-siteactions">' not in browser.contents
    True
    
Check for the footer and colophon.

    >>> 'James Cook University. All rights reserved' in browser.contents
    True
    >>> 'Designed and developed by JCU eResearch Centre' in browser.contents
    True
    >>> browser.contents.find('portal-footer-wrapper') > 0
    True

Check our ordering for the viewlets

    >>> browser.contents.find('portal-siteactions-wrapper') > \
    ... browser.contents.find('portal-personaltools-wrapper')
    True

Custom Theming
--------------

    >>> from jcu.theme import config
    >>> from jcu.theme.theming import IThemeSettingsManager

We shouldn't have any themes set at present on the home page.
 
    >>> browser.url == portal_url
    True
    >>> any([a in browser.contents for a in config.THEMES])
    False

But we should have a Theme tab available.
    
    >>> theme_tab = browser.getLink('Theme')
    >>> theme_tab
    <Link text='Theme' url='.../@@edit_theming_settings'> 

Click it.

    >>> theme_tab.click()

Theming page
~~~~~~~~~~~~

We should now be looking at the theming for the home page (which is a default
view).

    >>> 'Theming Options' in browser.contents
    True
    >>> 'Theme Name' in browser.contents
    True
    >>> 'Ignore this selection?' in browser.contents
    True
    >>> browser.getControl('Apply')
    <SubmitControl name='form.buttons.apply' type='submit'>
    >>> browser.getControl('Cancel')
    <SubmitControl name='form.buttons.cancel' type='submit'>
    >>> browser.getControl('Delete Settings')
    <SubmitControl name='form.buttons.44656c6574652053657474696e6773' type='submit'>

This isn't the actual container, so check we're reporting this.

    >>> adjusting_msg = 'adjusting the theming for a default view'
    >>> adjusting_msg in browser.contents
    True
    >>> go_here_link = browser.getLink('go here')
    >>> go_here_link
    <Link text='go here' url='http://nohost/plone/@@edit_theming_settings'>

Let's go set the theme options at the site root.

    >>> go_here_link.click()

We shouldn't get that message we had before and should now be at the root.

    >>> adjusting_msg not in browser.contents
    True
    >>> browser.url == 'http://nohost/plone/@@edit_theming_settings'
    True

Setting the theme
~~~~~~~~~~~~~~~~~
    
Set the theme to be blue.

    >>> list_control = browser.getControl(name='form.widgets.theme_name:list')
    >>> list_control
    <ListControl name='form.widgets.theme_name:list' type='select'>

    >>> theme_setting = ['jcu-blue']
    >>> list_control.value = theme_setting
    >>> list_control.value == theme_setting
    True
 
    >>> browser.getControl('Apply').click()

Clicking the apply button has now modified our body CSS class, and our
settings page should display our settings.

    >>> config.MESSAGE_OKAY in browser.contents
    True
    >>> print tagContents('body', browser.contents)
    class="template-edit_theming_settings ...jcu-blue"...

Just for good measure, we'll confirm this programmatically too.

    >>> settings = IThemeSettingsManager(portal)
    >>> print settings.theme_name
    jcu-blue
    >>> print settings.ignore_selection
    False


Changing a theme setting
~~~~~~~~~~~~~~~~~~~~~~~~

Our drop-down menu should be set to our setting by default.

    >>> list_control = browser.getControl(name='form.widgets.theme_name:list')
    >>> list_control.value == theme_setting
    True

We can change our setting too.

    >>> theme_setting = ['jcu-red']
    >>> list_control.value = theme_setting
    >>> list_control.value == theme_setting
    True
 
    >>> browser.getControl('Apply').click()
    >>> print tagContents('body', browser.contents)
    class="...jcu-red"...
    >>> print settings.theme_name
    jcu-red

Inheritance and overrides
~~~~~~~~~~~~~~~~~~~~~~~~~

By default, all contexts beneath our setting get the same theme.  We can,
however, override this whenever we'd like.  Let's have a look at our Users
area, where we should have our current theme applied already.

    >>> browser.getLink('Users').click()
    >>> print tagContents('body', browser.contents)
    class="...jcu-red"...

And we can override our settings on another context.  Let's try changing
the theme for our Users area.
  
    >>> browser.getLink('Theme').click()
    >>> list_control = browser.getControl(name='form.widgets.theme_name:list')

We shouldn't have any value set yet, because we're inheriting.

    >>> list_control.value
    ['None']
    >>> '<span>jcu-red</span>, inherited from:' in browser.contents
    True

Change the theme and have a look at the difference in body class.

    >>> theme_setting = ['jcu-green']
    >>> list_control.value = theme_setting
    >>> list_control.value == theme_setting
    True
 
    >>> browser.getControl('Apply').click()
    >>> print tagContents('body', browser.contents)
    class="template-edit_theming_settings ...jcu-green"...

    >>> "Effective inherited setting" not in browser.contents
    True

    >>> local_settings = IThemeSettingsManager(portal.Members)
    >>> print local_settings.theme_name
    jcu-green

And we should also check the portal root as well to make sure our application
function worked correctly.

    >>> settings.theme_name != local_settings.theme_name
    True
    >>> print settings.theme_name
    jcu-red

Finishing up
~~~~~~~~~~~~

Test logout and check theming whilst logged out.

    >>> browser.getLink('Log out').click()
    >>> 'You are now logged out' in browser.contents
    True

    >>> browser.open(portal_url)
    >>> print tagContents('body', browser.contents)
    class="...jcu-red"...
 
    >>> browser.getLink('Users').click()
    >>> print tagContents('body', browser.contents)
    class="...jcu-green"...
   
Logged out aspects
------------------

Check a couple of final aspects that should be visible if you're logged
out (or not visible, as the case may be).

    >>> 'Get Support' not in browser.contents
    True

    >>> browser.getLink('Log in')
    <Link text='Log in' url='http://nohost/plone/...'>

