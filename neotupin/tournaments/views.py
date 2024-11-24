# tournaments/views.py

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Tournament
from .serializers import TournamentSerializer

class TournamentListView(generics.ListAPIView):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
    permission_classes = [IsAuthenticated]

class TournamentCreateView(generics.CreateAPIView):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
    permission_classes = [IsAuthenticated]
