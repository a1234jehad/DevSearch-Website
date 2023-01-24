from rest_framework import serializers
from projects.models import Project,Tag
from users.models import Profile



class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    owner = ProfileSerializer(read_only=True,many=False)
    tags = TagSerializer(read_only=True, many=True)
    class Meta:
        model = Project
        fields = '__all__'