from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from users.models import User


@shared_task
def check_last_login():
    # print(11)
    users = User.objects.all()
    for user in users:
        if user.last_login:
            if timezone.now() - user.last_login >= timedelta(days=30):
                user.is_active = False
                user.save()
