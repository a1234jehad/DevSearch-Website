from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from .forms import ProjectForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def projects(req):
    search_query = ''
    if req.GET.get('search_query'):
        search_query = req.GET.get('search_query')
    tags = Tag.objects.filter(name__icontains=search_query)
    projects = Project.objects.filter(
        Q(title__icontains=search_query) | 
        Q(description__icontains=search_query) |
        Q(owner__name__icontains=search_query) |
        Q(tags__in=tags)).distinct()
    

    page = req.GET.get('page', 1)
    results = 3
    paginator = Paginator(projects, results)
    projects = paginator.get_page(page)
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        projects = paginator.page(1)
    except EmptyPage:
        projects = paginator.page(paginator.num_pages)

    
    context = {'projects': projects,
                'search_query':search_query,
                'paginator':paginator}
    return render(req,'projects/projects.html',context)

def project(req,pk):
    proj = Project.objects.get(id=pk)
    context = {'projectObj' : proj}
    return render(req,'projects/single-project.html',context)

@login_required(login_url="login")
def createProject(req):
    form = ProjectForm()
    profile = req.user.profile
    if req.method == 'POST':
        form = ProjectForm(req.POST, req.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect('projects')
    context = {'form' : form}
    return render(req,"projects/project_form.html",context)


def updateProject(req,pk):
    # pk = primery key
    profile = req.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)

    if req.method == 'POST':
        form = ProjectForm(req.POST,req.FILES,instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects')
    context = {'form' : form}
    return render(req,"projects/project_form.html",context)

def deleteProject(req,pk):
    project = Project.objects.get(id=pk)
    if req.method == 'POST':
        project.delete()
        return redirect('projects')
        
    context = {'object': project}
    return render(req,'delete_template.html',context)

