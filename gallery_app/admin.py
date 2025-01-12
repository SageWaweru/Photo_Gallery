from django.contrib import admin
from . models import Subscriber, Profile, Photo, Tag


admin.site.register(Subscriber)
admin.site.register(Profile)
admin.site.register(Photo)
admin.site.register(Tag)


# Register your models here.
