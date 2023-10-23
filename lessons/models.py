from django.db import models


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
