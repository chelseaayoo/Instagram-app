from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from cloudinary.models import CloudinaryField

# Create your models here.
class Image(models.Model):
  photo = CloudinaryField('image')
  photo_name = models.CharField(max_length=60)
  posted_at = models.DateTimeField(auto_now_add=True)
  photo_caption = models.TextField()
  user = models.ForeignKey(User,on_delete = models.CASCADE)

  def save_photo(self):
     self.save()

  @classmethod
  def display_photos(cls):
    photos = cls.objects.all().order_by('-posted_at')
    return photos

  @property
  def saved_comments(self):
    return self.comments.all()

  @property
  def saved_likes(self):
    return self.photolikes.count()

  @classmethod
  def search_photos(cls,search_term):
    photos = cls.objects.filter(photo_name__icontains = search_term).all()
    return photos

  def delete_post(self):
    self.delete()

  def __str__(self):
    return "%s photo" % self.photo_name

class Profile(models.Model):
  profile_photo = CloudinaryField('image')
  bio = models.TextField()
  user = models.OneToOneField(User,on_delete = models.CASCADE)


  @receiver(post_save , sender = User)
  def create_profile(instance,sender,created,**kwargs):
    if created:
      Profile.objects.create(user = instance)

  @receiver(post_save,sender = User)
  def save_profile(sender,instance,**kwargs):
    instance.profile.save()

  @property
  def saved_followers(self):
    return self.followers.count()   

  @property
  def saved_following(self):
    return self.following.count() 


  @property
  def follows(self):
    return [follow.followee for follow in self.following.all()]

  @property
  def following(self):
    return self.followers.all()



  @classmethod
  def search_profiles(cls,search_term):
    profiles = cls.objects.filter(user__username__icontains = search_term).all()
    return profiles

  def __str__(self):
    return "%s profile" % self.user