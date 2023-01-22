from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate,logout
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import *
from django.db.models import Q

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
            return redirect('edit-account')
        else:
            messages.error(req,"Error Happend while registeration")
    context = {'page': page,
               'form': form,
    }
    return render(req,"users/login_register.html",context)


def profiles(req):
    search_query = ""
    if req.GET.get('search_query'):
        search_query = req.GET.get('search_query')
    print("search_query: ",search_query)

    skills = Skill.objects.filter(name__iexact=search_query)

    profiles = Profile.objects.filter(
        Q(name__icontains=search_query) | 
        Q(short_intro__icontains=search_query) |
        Q(skill__in=skills)).distinct()

    context = {'profiles': profiles,
                'search_query':search_query,}
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

@login_required(login_url='login')
def userAccount(req):
    profile = req.user.profile
    skills = profile.skill_set.all()
    projects = profile.project_set.all()

    context = {'profile': profile,
                'skills':skills,  
                'projects':projects,  
    }
    return render(req,'users/account.html',context)


@login_required(login_url='login')
def editAccount(req):
    profile = req.user.profile
    form = ProfileForm(instance=profile)
    context = {'form':form}
    if req.method == 'POST':
        form = ProfileForm(req.POST,req.FILES,instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')
    return render(req,"users/profile_form.html",context)


@login_required(login_url='login')
def createSkill(req):
    form = SkillForm()

    if req.method == 'POST':
        form = SkillForm(req.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = req.user.profile
            skill.save()
            return redirect('account')

    context = {'form':form}
    return render(req,"users/skill_form.html",context)


@login_required(login_url='login')
def updateSkill(req,pk):
    skill = Skill.objects.get(id=pk)
    form = SkillForm(instance=skill)

    if req.method == 'POST':
        form = SkillForm(req.POST,instance=skill)
        if form.is_valid():
            form.save()
            return redirect('account')

    context = {'form':form}
    return render(req,"users/skill_form.html",context)

@login_required(login_url='login')
def deleteSkill(req,pk):
    skill = Skill.objects.get(id=pk)
    if req.method == 'POST':
        skill.delete()
        return redirect('account')
    context = {'object':skill}
    return render(req,"delete_template.html",context)
