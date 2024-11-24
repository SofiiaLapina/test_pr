from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render
from django.views import View
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, LeaderboardUserSerializer
from rest_framework.views import APIView
import json


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def get(self, request):
        return render(request, 'register.html')

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
            username = data.get('username')
            password = data.get('password')
        except json.JSONDecodeError:
            return Response({"detail": "Invalid input format."}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Невірні облікові дані."}, status=status.HTTP_401_UNAUTHORIZED)


class LeaderboardView(APIView):
    def get(self, request):
        # Повертаємо JSON, якщо це запит API
        if request.accepted_renderer.format == 'json':
            users = User.objects.all().order_by('-userprofile__score')[:10]
            serializer = LeaderboardUserSerializer(users, many=True)
            return Response(serializer.data)

        # Рендеримо HTML, якщо це запит через браузер
        users = User.objects.all().order_by('-userprofile__score')[:10]
        serializer = LeaderboardUserSerializer(users, many=True)
        return render(request, 'leaderboard.html', {'users': serializer.data})

class CustomLoginView(LoginView):
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        return next_url or super().get_success_url()