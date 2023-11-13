import os

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from lessons.models import Subscription, Course


@shared_task
def send_email_course_updated(course_pk):
    subscribers = Subscription.objects.filter(course=course_pk)
    course = Course.objects.get(pk=course_pk)
    for subscriber in subscribers:
        send_mail(
            subject=f'Курс {course} обновлен',
            message=f'Курс {course} обновлен',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[subscriber.user.email]
        )
