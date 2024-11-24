# tournaments/urls.py

from django.urls import path
from .views import TournamentListView, TournamentCreateView

urlpatterns = [
    path('', TournamentListView.as_view(), name='tournament_list'),
    path('create/', TournamentCreateView.as_view(), name='tournament_create'),
]
