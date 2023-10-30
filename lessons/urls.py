from django.urls import path

from lessons.apps import LessonsConfig
from rest_framework.routers import DefaultRouter

from lessons.views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView, LessonsQtyCreateAPIView, LessonsQtyListAPIView, \
    CourseLessonsQtyListAPIView

app_name = LessonsConfig.name

router = DefaultRouter()
router.register(r'lessons', CourseViewSet, basename='lessons')

urlpatterns = [
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson-create'),
    path('lesson/', LessonListAPIView.as_view(), name='lesson-list'),
    path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson-get'),
    path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson-update'),
    path('lesson/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson-delete'),
    path('lessonsqty/create/', LessonsQtyCreateAPIView.as_view(), name='lessonsqty-create'),
    path('lessonsqty/', LessonsQtyListAPIView.as_view(), name='lessonsqty-list'),
    path('course/lessonsqty/', CourseLessonsQtyListAPIView.as_view(), name='course-lessonsqty'),
] + router.urls
