from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _


class UserRoles(models.TextChoices):
    MEMBER = 'member', _('member')
    MODERATOR = 'moderator', _('moderator')


# Create your models here.

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')
    city = models.CharField(max_length=50, verbose_name='город', null=True, blank=True)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    role = models.CharField(max_length=9, choices=UserRoles.choices, default=UserRoles.MEMBER)


class EmailVerification(models.Model):
    code = models.UUIDField(unique=True, verbose_name='код подтверждения')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    expiration_date = models.DateTimeField(verbose_name='срок действия кода')

    def __str__(self):
        return f'email verification for {self.user.email}'

    def send_verification(self):
        link = reverse('users:email_verification', kwargs={'email': self.user.email, 'code': self.code})
        verification_link = settings.DOMAIN_NAME + link
        subject = 'Подтверждение учетной записи'
        message = f'Для подтверждения перейдите по ссылке {verification_link}'
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.user.email],
            fail_silently=False,
        )

    def is_expired(self):
        return now() >= self.expiration_date
