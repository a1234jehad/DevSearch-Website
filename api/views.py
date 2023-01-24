from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from .serializers import ProjectSerializer
from projects.models import Project,Review
from rest_framework import status

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser

@api_view(['GET'])
def getRoutes(request):
    routes = [
        {'GET':'/api/projects/'},
        {'GET':'/api/projects/id'},
        {'POST':'/api/projects/id/vote'},
        {'POST':'/api/users/token'},
        {'POST':'/api/users/token/refresh'},

    ]

    return Response(routes)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProjects(request):
    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getProject(request, pk):
    projects = Project.objects.get(id=pk)
    serializer = ProjectSerializer(projects, many=False)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def projectVote(request, pk):
    project = Project.objects.get(id=pk)
    data = request.data
    user = request.user.profile
    review , created = project.review_set.get_or_create(
        owner=user,
        project=project,
    )
    review.value = data['value']
    review.save()
    
    print("DATA", data,    project.getVoteCount
)
    serializer = ProjectSerializer(project, many=False)
    
    return Response(serializer.data)