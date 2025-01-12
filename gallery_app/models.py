from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    bio = models.TextField()
    profile_picture =CloudinaryField("image", null=True)
    
    def __str__(self):
            return self.user.username

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Photo(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    tags = models.ManyToManyField(Tag, related_name="photos", blank=True)
    uploaded_photo =CloudinaryField("image", null=True)
    total_likes = models.PositiveIntegerField(default=0)
    total_dislikes = models.PositiveIntegerField(default=0)    
    
    def __str__(self):
            return self.title

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

# Create your models here.
