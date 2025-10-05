from rest_framework import serializers
from .models import University, FavoriteUniversity
from django.contrib.auth.models import User

class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = ['id', 'name', 'country', 'lat', 'lng']

class FavoriteUniversitySerializer(serializers.ModelSerializer):
    university = UniversitySerializer(read_only=True)

    class Meta:
        model = FavoriteUniversity
        fields = ['id', 'user', 'university', 'added_at']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
