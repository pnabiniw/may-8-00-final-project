from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django import forms

from account.models import UserProfile

User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["email", "password1", "password2", "first_name", "last_name"]


class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["profile_picture", "resume", "address", "phone_number", "about_me"]

    def clean_resume(self):
        resume = self.cleaned_data.get('resume')
        if resume:
            extension = resume.name.split(".")[-1]
            if extension != 'pdf':
                raise ValidationError("Resume must be a pdf file !!")
        return resume

    def clean_profile_picture(self):
        pp = self.cleaned_data.get('profile_picture')
        if pp:
            extension = pp.name.split(".")[-1]
            if extension not in ['jpg', 'png', 'jpeg', 'JPG', 'JPEG', 'svg']:
                raise ValidationError("Invalid image format for profile picture")
        return pp
