# users/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile
from .utils import update_user_rank

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Створюємо профіль користувача після створення користувача.
    """
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Зберігаємо профіль користувача при збереженні користувача.
    """
    instance.userprofile.save()

@receiver(post_save, sender=UserProfile)
def check_rank(sender, instance, **kwargs):
    """
    Перевіряємо та оновлюємо рейтинг користувача після зміни його балів.
    """
    if kwargs.get('update_fields') and 'score' in kwargs['update_fields']:
        update_user_rank(instance)
