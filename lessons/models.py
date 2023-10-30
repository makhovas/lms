from django.db import models

from users.models import User


# Create your models here.
class Course(models.Model):
    title = models.CharField(max_length=150, verbose_name='название курса')
    preview = models.ImageField(upload_to='lessons/', verbose_name='превью курса', null=True, blank=True)
    description = models.TextField(verbose_name='описание курса')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    title = models.CharField(max_length=150, verbose_name='название урока')
    preview = models.ImageField(upload_to='lessons/', verbose_name='превью урока', null=True, blank=True)
    link = models.URLField(verbose_name='ссылка на видео', null=True, blank=True)
    description = models.TextField(verbose_name='описание урока')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'


class LessonsQty(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, blank=True, related_name='lessonsqty')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True, related_name='lessonsqty')
    lessonsqty = models.PositiveIntegerField(verbose_name='количество уроков')

    def __str__(self):
        return f'{self.lesson if self.lesson else self.course} - {self.lessonsqty}'

    class Meta:
        verbose_name = 'количество уроков'
        verbose_name_plural = 'количество уроков'


class Payments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name='дата оплаты')
    paid_course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='оплаченный курс')
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='оплаченный урок')
    payment_amount = models.PositiveIntegerField(verbose_name='сумма оплаты')
    payment_type = models.TextField(default=True, verbose_name='способ оплаты: наличные или перевод')

    def __str__(self):
        return f'{self.paid_lesson if self.paid_lesson else self.paid_course} - {self.payment_date}'

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'
        ordering = ('-payment_date',)
