from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Photo, Tag

 

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email'
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Choose a username'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter password'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirm password'
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ProfileForm(forms.ModelForm):
 class Meta:
    model = Profile
    fields = [ 'profile_picture', 'bio']
    widgets = {
    'bio': forms.Textarea(attrs={
    'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm h-32 p-4'
    }),
    }

class PhotoForm(forms.ModelForm):
  tags = forms.CharField(
        required=False,
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter tags separated by commas'}),
        label='Tags (comma separated)'
    )

  class Meta:
        model = Photo
        fields = ['title', 'description','uploaded_photo', 'tags']  

  def save(self, *args, **kwargs):
        photo = super().save(commit=False)
        photo.save()

        tags_input = self.cleaned_data.get('tags')
        if tags_input:
            tag_names = [tag.strip() for tag in tags_input.split(',')]
            for name in tag_names:
                tag, created = Tag.objects.get_or_create(name=name)
                photo.tags.add(tag)

        return photo


