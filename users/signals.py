from django.db.models.signals import *
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import *

from django.core.mail import send_mail
from django.conf import settings
@receiver(post_save,sender=User)
def createProfile(sender,instance,created,**kwargs):

    if created:
        print("A NEW PROFILE HAS BEEN CREATED!")
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name,
        )
        send_mail(
            subject="Welcome to DevSearch",
            message="Welcome to DevSearch, we hope you enjoy your stay!",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )

@receiver(post_save,sender=Profile)
def updateUser(sender,instance,created,**kwargs):
    profile = instance
    user = profile.user
    if not created:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()

@receiver(post_delete,sender=Profile)
def deleteUser(sender,instance,**kwargs):
    print("USER HAS BEEN DELETED!")
    user = instance.user
    user.delete()