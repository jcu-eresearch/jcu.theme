from zope.app.component.hooks import getSite
from Products.CMFCore.utils import getToolByName

PROFILE_ID = 'profile-jcu.theme:default'

def setupVarious(context):
    """
    Set up various aspects of Plone that we can't set up using
    GenericSetup profiles (yet).  These aspects should be removed
        whenever possible and replaced with a GS import profile.
    """

    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.

    if context.readDataFile('jcu.theme_various.txt') is None:
        return

    # Add additional setup code here
    site = getSite()

    #Set up the new Plone 4 MailHost for queuing
    try:
        site.MailHost.manage_makeChanges(
            title='Mail server settings for outgoing mail',
            smtp_host='hostrelay.jcu.edu.au',
            smtp_port='25',
            smtp_queue=True,
            smtp_queue_directory='/tmp/mailhost'
        )
        site.plone_log('MailHost configured for queuing.')
    except:
        site.plone_log('Could not reconfigure MailHost for queuing.')

    #Set up our reCAPTCHA keys for forms, etc
    try:
        from collective.recaptcha.settings import getRecaptchaSettings
        settings = getRecaptchaSettings()
        settings.public_key = u'6Ld5c78SAAAAAJH6NdN69ZYiXGrYcs9MLrvjY08U'
        settings.private_key = u'6Ld5c78SAAAAAGJpMrcbF_vAzeVRNWCjIWFZPZfs'
        site.plone_log('reCAPTCHA keys configured.')
    except:
        site.plone_log('Could not configure reCAPTCHA keys.')

    #Customise the parts of the LDAP plugin our GS doesn't touch yet.
    try:
        acl_users = site.acl_users
        plugins = acl_users.plugins
        deactivation = ['ICredentialsResetPlugin',
                        'IGroupManagement',
                        'IUserAdderPlugin',
                        'IUserManagement',
                       ]
        for interface in deactivation:
            try:
                plugins.deactivatePlugin(
                    plugins._getInterfaceFromName(interface),
                    'ldap-plugin',
                )
            except:
                #Changes since plone.app.ldap 1.2.4 mean this is going to
                #fail.  Not a bad thing though to check!
                site.plone_log("JCU LDAP: Couldn't deactivate %s interface" \
                               % interface)
        ldap_plugin = acl_users['ldap-plugin']
        ldap_acl_users = ldap_plugin.acl_users
        ldap_acl_users.read_only = True
        ldap_acl_users._pwd_encryption = 'SSHA'
        ldap_acl_users._roles = ['Anonymous']
        site.plone_log('LDAP plugin settings configured.')
    except:
        site.plone_log('Could not configure LDAP plugin settings.')
        raise

    #We can import plone.app.caching profiles (we have already via
    #metadata.xml) but we need to manually turn it on.
    try:
        from zope.component import getUtility
        from plone.registry.interfaces import IRegistry
        from plone.caching.interfaces import ICacheSettings
        from plone.app.caching.interfaces import IPloneCacheSettings
        from plone.cachepurging.interfaces import ICachePurgingSettings

        registry = getUtility(IRegistry)
        settings = registry.forInterface(ICacheSettings)
        settings.enabled = True
        ploneSettings = registry.forInterface(IPloneCacheSettings)
        ploneSettings.enableCompression = False
        purgingSettings = registry.forInterface(ICachePurgingSettings)
        purgingSettings.enabled = False

        site.plone_log('plone.app.caching settings configured.  Caching and \
                       compression are now active.')
    except:
        site.plone_log('Could not configure plone.app.caching settings.')


def run_import_step(context, step, logger=None):
    """Re-import some specified import step for Generic Setup.
    """
    setup = getToolByName(context, 'portal_setup')
    setup.runImportStepFromProfile(PROFILE_ID, step)
    return

def upgrade_actions(context, logger=None):
    run_import_step(context, 'actions')

def upgrade_mailhost(context, logger=None):
    run_import_step(context, 'mailhost')
