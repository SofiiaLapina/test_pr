from rest_framework import serializers
from django.contrib.auth.models import User
from users.models import UserProfile


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Користувач із таким email вже існує.")
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Користувач із таким ім'ям вже існує.")
        if ' ' in value:
            raise serializers.ValidationError("Ім'я користувача не повинно містити пробілів.")
        if len(value) < 3:
            raise serializers.ValidationError("Ім'я користувача має містити щонайменше 3 символи.")
        if len(value) > 30:
            raise serializers.ValidationError("Ім'я користувача не може перевищувати 30 символів.")
        return value

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class BaseUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    score = serializers.IntegerField(source='userprofile.score', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', 'score']


class LeaderboardUserSerializer(serializers.ModelSerializer):
    score = serializers.IntegerField(source='userprofile.score', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'score']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']