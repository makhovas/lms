from django.urls import path

from lessons.apps import LessonsConfig
from rest_framework.routers import DefaultRouter

from lessons.views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView, QuantityCreateAPIView, QuantityListAPIView, CourseQuantityListAPIView

app_name = LessonsConfig.name

router = DefaultRouter()
router.register(r'lessons', CourseViewSet, basename='lessons')

urlpatterns = [
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson-create'),
    path('lesson/', LessonListAPIView.as_view(), name='lesson-list'),
    path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson-get'),
    path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson-update'),
    path('lesson/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson-delete'),
    path('quantity/create/', QuantityCreateAPIView.as_view(), name='quantity-create'),
    path('quantity/', QuantityListAPIView.as_view(), name='quantity-list'),
    path('course/quantity/', CourseQuantityListAPIView.as_view(), name='course-quantity'),
] + router.urls
