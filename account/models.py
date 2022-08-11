from pickle import NONE
from unicodedata import name
from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name="userprofile")
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    role=models.CharField(max_length=32)

    def __str__(self):
        return self.firstname
