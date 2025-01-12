from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('accounts/register', views.register, name='register'),
    path('logout/', views.custom_logout, name='logout'),
    path('profile', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('upload/', views.photo_upload, name='photo_upload'),
    path('like/<int:photo_id>/', views.like_photo, name='like_photo'),
    path('dislike/<int:photo_id>/', views.dislike_photo, name='dislike_photo'),
    path('photo/<int:photo_id>/', views.photo_detail, name='photo_detail'),

]
