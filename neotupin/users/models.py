from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='userprofile'
    )
    score = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} (Score: {self.score})"
