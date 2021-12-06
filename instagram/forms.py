from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile,Comment,Image
from django.contrib.auth.models import User

class postPhotoForm(forms.ModelForm):
  class Meta:
    model = Image
    fields = ['photo','photo_name','photo_caption']