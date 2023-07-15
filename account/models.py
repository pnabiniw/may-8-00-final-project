import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from commons.models import BaseModel

from .manager import CustomUserManager


class User(AbstractUser):
    username = models.UUIDField(default=uuid.uuid4, editable=False)
    email = models.EmailField(_("email address"), unique=True)
    account_activated = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


class UserAccountActivationKey(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=50)


class UserProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.FileField(upload_to='profile_pictures', null=True, blank=True)
    resume = models.FileField(upload_to='resumes', null=True, blank=True)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=14)
    about_me = models.TextField(max_length=1000)
