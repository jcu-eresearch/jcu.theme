from AccessControl import ModuleSecurityInfo

ModuleSecurityInfo('jcu.theme.Extensions.GoogleCalendar').declarePublic('createGoogleCalendarEvent')


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
