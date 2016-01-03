from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Problem, Tag, News, Submission


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class ProblemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Problem
        fields = ('url', 'id', 'problemName', 'problemStatement', 'level')