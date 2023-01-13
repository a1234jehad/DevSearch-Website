from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def projects(req):
    msg = 'Hello, you are on the projects page'
    number = 101 
    context = {'message':msg,
                'number':number}
    return render(req,'projects/projects.html',context)

def project(req,pk):
    return render(req,'projects/single-project.html')

