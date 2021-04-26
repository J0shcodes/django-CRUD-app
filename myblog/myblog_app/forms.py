from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import fields
from django.forms.widgets import PasswordInput

class NewUserForm(UserCreationForm):
  email = forms.EmailField(required=True)
  first_name = forms.CharField(max_length=100)
  second_name = forms.CharField(max_length=100)
  username = forms.CharField(max_length=100)
  password1 = forms.CharField(widget=PasswordInput)
  password2 = forms.CharField(widget=PasswordInput)
  
  class Meta:
    model = User
    fields = ['first_name', 'second_name', 'username', 'email', 'password1', 'password2']
    
    def save(self, commit=True):
      user = super(NewUserForm, self).save(commit=False)
      user.email = self.clean_data['email']
      if commit:
        user.save()
      return user