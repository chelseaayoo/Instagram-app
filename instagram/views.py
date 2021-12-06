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

@login_required
def post(request):
  if request.method == 'POST':
    post_form = postPhotoForm(request.POST,request.FILES) 
    if post_form.is_valid():
      the_post = post_form.save(commit = False)
      the_post.user = request.user
      the_post.save()
      return redirect('home')

  else:
    post_form = postPhotoForm()
  return render(request,'post.html',{"post_form":post_form})

def detail(request,photo_id):
  current_user = request.user
  try:
    photo = get_object_or_404(Image, pk = photo_id)
  except ObjectDoesNotExist:
    raise Http404()
  return render(request, 'photo_details.html', {'photo':photo,'current_user':current_user})

def register(request):
  if request.method == 'POST':
    form = Registration(request.POST)
    if form.is_valid():
      form.save()
      email = form.cleaned_data['email']
      username = form.cleaned_data.get('username')

      messages.success(request,f'Account for {username} created,you can now login')
      return redirect('login')
  else:
    form = Registration()
  return render(request,'registration/registration_form.html',{"form":form})

@login_required
def profile(request):
  comment_form = CommentsForm()
  current_user = request.user
  photos = Image.objects.all().order_by('-posted_at')
  all_users = User.objects.all()
  user_photos = Image.objects.filter(user_id = current_user.id).all()
  
  return render(request,'profile/profile.html',{"photos":photos,'all_users':all_users,'comment_form':comment_form,'user_photos':user_photos,"current_user":current_user})

@login_required
def search(request):
  if 'search_user' in request.GET and request.GET["search_user"]:
    search_term = request.GET.get('search_user')
    users = Profile.search_profiles(search_term)
    photos = Image.search_photos(search_term)
    return render(request,'search.html',{"users":users,"photos":photos})
  else:
    return render(request,'search.html')

@login_required
def allcomments(request,photo_id):
  photo = Image.objects.filter(pk = photo_id).first()
  return render(request,'comments.html',{"photo":photo})