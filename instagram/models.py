from django.db import models
import datetime as dt
# cloudinary
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.db.models.fields import related
# Create your models here.


# image model
class Image(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='images')
    image = CloudinaryField('image')
    image_name = models.CharField(max_length=50)
    image_caption = models.TextField()
    image_date = models.DateTimeField(auto_now_add=True)
    profile = models.ForeignKey(User, on_delete=models.CASCADE)
    like_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)

    # get images by user
    @classmethod
    def get_images_by_user(cls, user):
        images = cls.objects.filter(user=user)
        return images

    # save image
    def save_image(self):
        self.save()

    # delete image
    def delete_image(self):
        self.delete()

    # update image caption
    def update_caption(self, new_caption):
        self.image_caption = new_caption
        self.save()

    # search images using image name
    @classmethod
    def search_by_image_name(cls, search_term):
        images = cls.objects.filter(
            image_name__icontains=search_term)
        return images

    #  get a single image using id
    @classmethod
    def get_single_image(cls, id):
        image = cls.objects.get(id=id)
        return image

    def __str__(self):
        return self.image_name


# profile model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_photo = CloudinaryField('image')
    bio = models.TextField(max_length=500, blank=True, null=True)
    contact = models.CharField(max_length=50, blank=True, null=True)

    def update(self):
        self.save()

    def save_profile(self):
        self.save()

    def delete_profile(self):
        self.delete()

    @classmethod
    def get_profile_by_user(cls, user):
        profile = cls.objects.filter(user=user)
        return profile

    def __str__(self):
        return self.user.username


# likes model
class Likes(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    # likes = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.likes


# comments model
class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    comment = models.CharField(max_length=50)
    comment_date = models.DateTimeField(auto_now_add=True)

    def save_comment(self):
        self.save()

    def __str__(self):
        return self.comment



