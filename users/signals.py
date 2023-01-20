from django.db.models.signals import *
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import *

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

@receiver(post_delete,sender=Profile)
def deleteUser(sender,instance,**kwargs):
    print("USER HAS BEEN DELETED!")
    user = instance.user
    user.delete()