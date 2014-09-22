from django import forms

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    def __init__(self, *args, **kwargs): 
 		super(UserCreateForm, self).__init__(*args, **kwargs) 
 		self.fields['email'].required = True
 		self.fields['username'] = None
 		self.fields['first_name'].required = True
 		self.fields['last_name'].required = True
 		self.fields['password1'].required = True
 		self.fields['password2'].required = True
 		# remove username
 		self.fields.pop('username')
    class Meta:
        model = User
        fields = ("email","first_name", "last_name","password1", "password2")

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.username = self.cleaned_data["email"]
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user