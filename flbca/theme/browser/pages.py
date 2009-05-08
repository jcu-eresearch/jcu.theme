from p4a.z2utils.patches import apply_patches
apply_patches()

from zope.component import getMultiAdapter
from Products.Collage.browser.views import BaseView
from dateable.chronos.browser.month import MonthView
from dateable.chronos.browser.base_view import DAYS, MONTHS
import datetime
import textwrap

class CollageDateableMonthPage(BaseView, MonthView):
     title = u'p4a-calendar'
     max_length = 18
     max_line_length = 10

     #Need to call the parent classes init methods as they don't
     #get done automatically in Python (at least not yet)
     def __init__(self, context=None, request=None):
         MonthView.__init__(self, context, request)
         self.weekdays = DAYS 
         self.months = MONTHS

     def calcInfo(self):
         currentDefaultDay = self.default_day
         self._default_day = datetime.date.today()
         MonthView.calcInfo(self)
         self._default_day = currentDefaultDay

     def eventTextDisplay(self, eventText):
         wrappableTitle = eventText[:self.max_length]

         wrapper = textwrap.TextWrapper(width=self.max_line_length)
         wrapper.break_on_hyphens = False
         wrappableTitle = '<br />'.join(wrapper.wrap(wrappableTitle))

         if len(eventText) > self.max_length:
             wrappableTitle += '...'
         
         return wrappableTitle

     def countMoreEvents(self, day):
        return (len(self.getOccurrencesInDay(day)) - (self.calendar_tool.displaymaxevents-1) )

