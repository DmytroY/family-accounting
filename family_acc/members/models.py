from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    family = models.CharField(max_length=100, blank=True, null=True)

class Member(models.Model):
    slug = models.SlugField(max_length=100, unique=True, blank=False, null=False)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    phone = models.IntegerField(null=True, blank=True)
    joined_date = models.DateField(null=True)
    email =models.EmailField(null=True, blank=True)

    def __str__(self):
        return f"{self.firstname} {self.lastname} {self.phone}"