from django.urls import path
from .views import RegisterView, LoginView, LeaderboardView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import CustomLoginView

urlpatterns = [
    # Шляхи для реєстрації
    path('register/', RegisterView.as_view(), name='register'),

    # Шляхи для входу
    path('login/', CustomLoginView.as_view(), name='login_form'),

    # Шляхи для отримання токенів
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Шлях для відображення рейтингу
    path('leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
]
