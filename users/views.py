from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate,logout
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages



# Create your views here.

def loginUser(req):
    page = 'login'

    if req.user.is_authenticated:
        return redirect('profiles')
    if req.method == 'POST':
        username = req.POST['username']
        password = req.POST['password']
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(req,"USERNAME DNE")
        user = authenticate(req,username=username,password=password)
        if user is not None:
            login(req,user)
            return redirect('profiles')
        else:
            messages.error(req,"Username OR password is incorrect")
    context = {'page': page}

    return render(req,"users/login_register.html",context)

def logoutUser(req):
    logout(req)
    messages.error(req,"User logged out!")

    return redirect('login')
from .forms import CustomUserCreationForm
def registerUser(req):
    page = 'register'
    form = CustomUserCreationForm()

    if req.method == 'POST':
        form = CustomUserCreationForm(req.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(req,"User account was created!")
            login(req,user)
            return redirect('profiles')
        else:
            messages.error(req,"Error Happend while registeration")
    context = {'page': page,
               'form': form,
    }
    return render(req,"users/login_register.html",context)


def profiles(req):
    profiles = Profile.objects.all()
    context = {'profiles': profiles}
    return render(req,'users/profiles.html',context)

def userProfile(req,pk):
    profile = Profile.objects.get(id=pk)

    topSkills = profile.skill_set.exclude(description = "")
    othersSkills =profile.skill_set.filter(description = "")

    context = {'profile': profile,
                'topSkills':topSkills,
                'otherSkills':othersSkills,    
    }

    return render(req,'users/user-profile.html',context)

def userAccount(req):
    context = {}
    return render(req,'users/account.html',context)