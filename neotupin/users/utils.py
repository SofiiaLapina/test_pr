from django.core.mail import send_mail
from django.conf import settings
from .models import UserProfile


def send_rank_update_email(user, old_rank, new_rank):
    """
    Надсилає лист користувачу, якщо його рейтинг змінився.
    """
    if old_rank > new_rank:  # Якщо користувач покращив свій рейтинг
        subject = 'Вітаємо з підвищенням у рейтингу!'
        message = (
            f'Привіт, {user.username}!\n\n'
            f'Вітаємо! Ви піднялися у рейтингу. Ваше нове місце: {new_rank}.\n'
            f'Продовжуйте докладати зусиль, щоб залишатися серед лідерів!'
        )
    elif old_rank < new_rank:  # Якщо користувач втратив позицію
        subject = 'На жаль, вас обійшли у рейтингу.'
        message = (
            f'Привіт, {user.username}!\n\n'
            f'На жаль, ви втратили своє місце у рейтингу. Ваше нове місце: {new_rank}.\n'
            f'Не засмучуйтесь! Ви завжди можете повернути свої позиції.'
        )
    else:
        return  # Якщо позиція не змінилась, нічого не робимо

    # Надсилання листа
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )


def update_user_rank(user_profile, score_increment=10):
    """
    Оновлює рейтинг користувача і перевіряє, чи змінилось його місце у рейтингу.
    У разі зміни рейтингу надсилає лист з повідомленням.
    """
    # Поточне місце користувача у рейтингу
    old_rank = UserProfile.objects.filter(score__gt=user_profile.score).count() + 1

    # Оновлюємо бали користувача
    user_profile.score += score_increment
    user_profile.save(update_fields=['score'])

    # Нове місце у рейтингу після оновлення
    new_rank = UserProfile.objects.filter(score__gt=user_profile.score).count() + 1

    # Якщо місце змінилося, надсилаємо повідомлення
    if old_rank != new_rank:
        send_rank_update_email(user_profile.user, old_rank, new_rank)

