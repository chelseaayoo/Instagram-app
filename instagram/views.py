from django.http  import HttpResponse
from django.shortcuts import render,redirect, get_object_or_404
from django.http import Http404,HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from . forms import Registration,UpdateUser,UpdateProfile,CommentsForm,postPhotoForm
from django.contrib.auth.decorators import login_required
from .models import Image,Profile,Like,Follows
from django.http import JsonResponse
from django.contrib.auth.models import User
from .email import send_welcome_email
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def welcome(request):
    return HttpResponse('Get started with Instagram')

@login_required
def index(request):
  comment_form = CommentsForm()
  post_form = postPhotoForm()
  photos = Image.display_photos()
  all_users = User.objects.all()
  
  return render (request,'index.html',{"photos":photos,"comment_form":comment_form,"post":post_form,"all_users":all_users})