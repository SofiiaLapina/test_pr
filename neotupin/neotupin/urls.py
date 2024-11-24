#neotupin\urls.py
from django.contrib import admin
from django.urls import path, include
from .views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('api/users/', include('users.urls')),
    path('api/quizzes/', include('quizzes.urls')),
]
