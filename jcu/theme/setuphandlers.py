from zope.app.component.hooks import getSite
from Products.CMFCore.utils import getToolByName

PROFILE_ID = 'profile-jcu.theme:default'

def setupVarious(context, site=None):
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
    site = site or getSite()

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

    #Customise the parts of the LDAP plugin our GS doesn't touch yet.
    try:
        acl_users = site.acl_users
        plugins = acl_users.plugins
        deactivation = ['IAuthenticationPlugin',
                        'ICredentialsResetPlugin',
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

def switch_to_cas(context):
    pass

def run_import_step(context, step, logger=None):
    """Re-import some specified import step for Generic Setup.
    """
    setup = getToolByName(context, 'portal_setup')
    return setup.runImportStepFromProfile(PROFILE_ID, step)

#Define all our upgrade functions in a simple, DRY fashion.
_upgrade_functions = [
    ('actions', 'actions'),
    ('mailhost', 'mailhost'),
    ('registry', 'plone.app.registry')
]

_function_template = """
def upgrade_%s(context, logger=None, return_values=False):
    result = run_import_step(context, '%s')
    if return_values: return result
"""

for spec in _upgrade_functions:
    exec _function_template % spec

