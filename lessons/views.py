from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter

from lessons.models import Course, Lesson, LessonsQty
from lessons.serializers import CourseSerializer, LessonSerializer, LessonsQtySerializer, CourseLessonsQtySerializer


# Create your views here.
class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()


class LessonsQtyCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonsQtySerializer


class LessonsQtyListAPIView(generics.ListAPIView):
    serializer_class = LessonsQtySerializer
    queryset = LessonsQty.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]  # Бэкенд для обработки фильтра
    filterset_fields = ('course', 'lesson')  # Набор полей для фильтрации
    ordering_fields = ('payment_date', 'payment_type',)


class CourseLessonsQtyListAPIView(generics.ListAPIView):
    queryset = LessonsQty.objects.filter(course__isnull=False)
    serializer_class = CourseLessonsQtySerializer
