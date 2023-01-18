from django.shortcuts import render
from .models import *
# Create your views here.
def profiles(req):
    profiles = Profile.objects.all()
    context = {'profiles': profiles}
    return render(req,'users/profiles.html',context)

def userProfile(req,pk):
    profile = Profile.objects.get(id=pk)
    context = {'profile': profile}

    return render(req,'users/user-profile.html',context)