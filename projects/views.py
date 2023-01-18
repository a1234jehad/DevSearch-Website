from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Project
from .forms import ProjectForm

# Create your views here.
def projects(req):
    projects = Project.objects.all()
    print(projects)
    context = {'projects': projects}
    return render(req,'projects/projects.html',context)

def project(req,pk):
    proj = Project.objects.get(id=pk)
    context = {'projectObj' : proj}
    return render(req,'projects/single-project.html',context)

def createProject(req):
    form = ProjectForm()

    if req.method == 'POST':
        form = ProjectForm(req.POST, req.FILES)
        if form.is_valid():
            form.save()
            return redirect('projects')
    context = {'form' : form}
    return render(req,"projects/project_form.html",context)


def updateProject(req,pk):
    # pk = primery key
    project = Project.objects.get(id=pk)
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
        
    context = {'obj': project}
    return render(req,'projects/deleted_obj.html',context)