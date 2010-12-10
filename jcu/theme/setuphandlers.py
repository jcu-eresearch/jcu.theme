from zope.app.component.hooks import getSite


def setupVarious(context):

    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.

    if context.readDataFile('jcu.theme_various.txt') is None:
        return

    # Add additional setup code here
    site = getSite()

    #Set up our reCAPTCHA keys for forms, etc
    try:
        from collective.recaptcha.settings import getRecaptchaSettings
        settings = getRecaptchaSettings()
        settings.public_key = u'6Ld5c78SAAAAAJH6NdN69ZYiXGrYcs9MLrvjY08U'
        settings.private_key = u'6Ld5c78SAAAAAGJpMrcbF_vAzeVRNWCjIWFZPZfs'
    except:
        site.plone_log('Could not configure reCAPTCHA keys.')
        pass

    #Customise the parts of the LDAP plugin our GS doesn't touch yet.
    try:
        acl_users = site.acl_users
        plugins = acl_users.plugins
        plugins.deactivatePlugin(
            plugins._getInterfaceFromName('IUserManagement'),
            'ldap-plugin',
        )
        ldap_plugin = acl_users['ldap-plugin']
        ldap_acl_users = ldap_plugin.acl_users
        ldap_acl_users.read_only = True
        ldap_acl_users._pwd_encryption = 'SSHA'
        ldap_acl_users._roles = ['Anonymous']
    except:
        site.plone_log('Could not configure LDAP plugin settings.')
        pass



