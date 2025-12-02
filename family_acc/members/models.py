from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    family = models.CharField(max_length=100, blank=True, null=True)

#automaticaly create user profile on user creation or update if username is changed
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwarg):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()


# class Member(models.Model):
#     slug = models.SlugField(max_length=100, unique=True, blank=False, null=False)
#     firstname = models.CharField(max_length=255)
#     lastname = models.CharField(max_length=255)
#     phone = models.IntegerField(null=True, blank=True)
#     joined_date = models.DateField(null=True)
#     email =models.EmailField(null=True, blank=True)

#     def __str__(self):
#         return f"{self.firstname} {self.lastname} {self.phone}"