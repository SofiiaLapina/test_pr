from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, LeaderboardView, CustomLoginView

urlpatterns = [
    # Реєстрація
    path('register/', RegisterView.as_view(), name='register'),

    # Вхід
    path('login/', CustomLoginView.as_view(), name='login_form'),

    # Вихід
    path('logout/', LogoutView.as_view(), name='logout'),

    # JWT токени
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Рейтинг
    path('leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
]
