from django import forms
from models import UploadFile

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class AppointmentForm(forms.Form):
    content = forms.CharField(max_length=256)
    email = forms.EmailField()
    course = forms.CharField(max_length=100)
    date = forms.CharField(max_length=100)
    created_at = forms.DateTimeField()

class PostForm(forms.Form):
    content = forms.CharField(max_length=256)
	#email = forms.EmailField()
	#course = forms.CharField(max_length=100)
    created_at = forms.DateTimeField()
	# date = forms.CharField(max_length=100)
	# comment = forms.CharField(widget=forms.Textarea)

# class CalendarEventForm(CalendarEventForm):

#     class Meta:
#         model = CalendarEvent
#         fields = ("title", "tutor", "tutor_email", "student", "student_email", "course", "url", "css_class", "start", "end")

#     def save(self, commit=True):
#         event = super(CalendarEvent, self)