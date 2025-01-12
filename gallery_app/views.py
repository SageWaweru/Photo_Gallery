from django.shortcuts import render,redirect,get_object_or_404
from django.db.models.signals import post_save
from django.dispatch import receiver
from . models import Subscriber, Profile, Tag, Photo
from . forms import RegistrationForm, ProfileForm, PhotoForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout

def home(request):
    tags = Tag.objects.all()

    selected_tag = request.GET.get('tag')
    if selected_tag:
        tag = Tag.objects.get(name=selected_tag)
        photos = Photo.objects.filter(tags=tag)
    else:
        photos = Photo.objects.all()

    return render(request, 'index.html', {'photos': photos, 'tags': tags})

def register(request):
 if request.method == 'POST':
    form = RegistrationForm(request.POST)
    if form.is_valid():
        form.save()
    return redirect('login')
 else:
    form = RegistrationForm()
 return render(request, 'registration/register.html', {'form': form})


def custom_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('logout')  
    return redirect('/') 

@login_required
def subscribe(request):
    if request.method == 'POST':
        email= request.POST['email']
        if Subscriber.objects.filter(email=email).exists():
            messages.error(request, 'You are already subscribed.')
        else:
            subscriber = Subscriber(email=email)
            subscriber.save()
            messages.success(request, 'Thank you for subscribing!')
            return redirect('subscribe')
    return render(request, 'subscribe.html')

@login_required
def profile_view(request):
    return render(request, 'profile.html', {'profile': request.user.profile})


@login_required
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'edit_profile.html', {'form': form})

@login_required
def photo_upload(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = PhotoForm()

    return render(request, 'add_photo.html', {'form': form})


def filter_photos(request):
    tags_param = request.GET.get('tags', '')  

    tag_names = tags_param.split(',')

    tags = Tag.objects.filter(name__in=tag_names)

    photos = Photo.objects.filter(tags__in=tags).distinct()

    return render(request, 'index.html', {'photos': photos})

@login_required
def like_photo(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    photo.total_likes += 1
    photo.save()
    return redirect(request.META.get('HTTP_REFERER', 'index'))

@login_required
def dislike_photo(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    photo.total_dislikes += 1
    photo.save()
    return redirect(request.META.get('HTTP_REFERER', 'index'))

def photo_detail(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    return render(request, 'photo_detail.html', {'photo': photo})
# Create your views here.
