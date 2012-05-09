from zope.i18nmessageid import MessageFactory
_ = MessageFactory('jcu.theme')

from AccessControl import ModuleSecurityInfo
module = ModuleSecurityInfo('jcu.theme.Extensions.GoogleCalendar') \
            .declarePublic('createGoogleCalendarEvent')

#XXX Monkey patch until CAS4PAS is fixed
import Products.CAS4PAS.CASAuthHelper
from zLOG import DEBUG
Products.CAS4PAS.CASAuthHelper.ERROR = DEBUG

def initialize(context):
    """Initializer called when used as a Zope 2 product."""
