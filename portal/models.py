from django.db import models
from django.contrib.auth.models import User
import os
# Create your models here.
def get_upload_path(instance, filename):
	return os.path.join('files', instance.owner.username, filename)

class UploadFile(models.Model):
	#file = models.FileField(upload_to='files/%Y/%m/%d')
	file = models.FileField(upload_to=get_upload_path)

from django.utils.translation import ugettext as _
from utils import datetime_to_timestamp
from django.contrib import admin
import forms

# class Tutor(models.Model):
#     first_name = models.CharField(max_length=100, verbose_name=('First Name'))
#     last_name = models.CharField(max_length=100, verbose_name=('Last Name'))
#     email = models.EmailField(max_length=255, verbose_name=('Email'))

# class AvailabilityEvent(models.Model):
#     """
#     Calendar Events (Tutor Availability)
#     """
#     CSS_CLASS_CHOICES = (
#         ('', _('Normal')),
#         ('event-warning', _('Warning')),
#         ('event-info', _('Info')),
#         ('event-success', _('Success')),
#         ('event-inverse', _('Inverse')),
#         ('event-special', _('Special')),
#         ('event-important', _('Important')),
#     )
#     title = models.CharField(max_length=255, verbose_name=_('Title'))
#     tutor = models.CharField(max_length=50, verbose_name=('Tutor'))
#     tutor_email = models.EmailField(max_length=255, verbose_name=('Tutor Email'))
#     #student = models.CharField(max_length=50, verbose_name=('Student'))
#     #student_email = models.EmailField(max_length=255, verbose_name=('Student Email'))
#     #course = models.CharField(max_length=50, verbose_name=('Course'))
#     #url = models.URLField(verbose_name=_('URL'))
#     url = 'http://www.example.com'
#     #css_class = models.CharField(max_length=2,choices=CSS_CLASS_CHOICES,default='event-success')
#     css_class = 'event-warning'
#     start = models.DateTimeField(verbose_name=_('Start Date'))
#     end = models.DateTimeField(verbose_name=_('End Date'), blank=True)


#     @property
#     def start_timestamp(self):
#         """
#         Return end date as timestamp
#         """
#         return datetime_to_timestamp(self.start)

#     @property
#     def end_timestamp(self):
#         """
#         Return end date as timestamp
#         """
#         return datetime_to_timestamp(self.end)

#     def __unicode__(self):
#         return self.title

class CalendarEvent(models.Model):
    """
    Calendar Events (Appointment)
    """
    CSS_CLASS_CHOICES = (
        ('', _('Normal')),
        ('event-primary', _('Primary')),
        ('event-warning', _('Warning')),
        ('event-info', _('Info')),
        ('event-success', _('Success')),
        ('event-inverse', _('Inverse')),
        ('event-special', _('Special')),
        ('event-important', _('Important')),
    )
    availability = models.BooleanField(default=True)
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    tutor = models.CharField(max_length=50, verbose_name=('Tutor'))
    tutor_email = models.EmailField(max_length=255, verbose_name=('Tutor Email'))
    student = models.CharField(max_length=50, verbose_name=('Student'))
    student_email = models.EmailField(max_length=255, verbose_name=('Student Email'))
    course = models.CharField(max_length=50, verbose_name=('Course'))
    #url = models.URLField(verbose_name=_('URL'))
   # searchFlag = models.BooleanField(default=False)
    url = 'http://www.example.com'
    css_class = models.CharField(max_length=100,choices=CSS_CLASS_CHOICES,default='event-success')
    start = models.DateTimeField(verbose_name=_('Start Date'))
    end = models.DateTimeField(verbose_name=_('End Date'), blank=True)


    @property
    def start_timestamp(self):
        """
        Return end date as timestamp
        """
        return datetime_to_timestamp(self.start)

    @property
    def end_timestamp(self):
        """
        Return end date as timestamp
        """
        return datetime_to_timestamp(self.end)

    def __unicode__(self):
        return self.title

        
# This Class helps to create objects for tutor schedule
class Tutor(models.Model) :
    tutor = models.CharField(max_length=50, verbose_name=('Tutor'))
    start = models.CharField(max_length=100,verbose_name=_('Start Date'))
    end = models.CharField(max_length=100,verbose_name=_('End Date'), blank=True)

'''    
class CourseTutor(models.Model) :
    course = models.CharField(max_length=50, verbose_name=('Course'))
    tutors = models.CharField(max_length=100,verbose_name=_('Tutors'))
'''

# This Class helps to create objects to hold availability string for tutor and date combination   
class AppointmentAvailability(models.Model) :
    tutor = models.CharField(max_length=50, verbose_name=('Tutor'))
    date = models.CharField(max_length=100,verbose_name=_('Start Date'))
    slotAvail = models.CharField(max_length=1000, verbose_name=('Slots'))
   
    class Meta:
        unique_together = ["tutor", "date"]


###Admin
class CalendarEventAdmin(admin.ModelAdmin):
    list_display = ["availability", "title", "tutor", "tutor_email", "student", "student_email", "css_class", "start", "end"]
    list_filler = ["title"]

# class AvailabilityEventAdmin(admin.ModelAdmin):
#     list_display = ["title", "tutor", "tutor_email", "css_class", "start", "end"]
#     list_filler = ["title"]
    
admin.site.register(CalendarEvent,CalendarEventAdmin)
# admin.site.register(AvailabilityEvent,AvailabilityEventAdmin)