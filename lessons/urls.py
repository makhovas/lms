from django.urls import path, include

from lessons.apps import LessonsConfig
from rest_framework.routers import DefaultRouter

from lessons.views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView, SubscriptionCreateAPIView, SubscriptionDestroyAPIView, PaymentsViewSet

app_name = LessonsConfig.name

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')
router.register(r'payments', PaymentsViewSet, basename='payments')

urlpatterns = [
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson-create'),
    path('lesson/', LessonListAPIView.as_view(), name='lesson-list'),
    path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson-get'),
    path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson-update'),
    path('lesson/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson-delete'),
    path('subscriptions/<int:course_id>/', SubscriptionCreateAPIView.as_view(), name='create-subscription'),
    path('subscriptions/delete/<int:course_id>/', SubscriptionDestroyAPIView.as_view(), name='delete-subscription'),
    path('users/', include('users.urls', namespace='users')),
] + router.urls
