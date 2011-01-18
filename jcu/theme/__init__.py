from zope.i18nmessageid import MessageFactory
_ = MessageFactory('jcu.theme')

from AccessControl import ModuleSecurityInfo
module = ModuleSecurityInfo('jcu.theme.Extensions.GoogleCalendar') \
            .declarePublic('createGoogleCalendarEvent')


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
