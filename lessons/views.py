from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, status
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from lessons.models import Course, Lesson, Subscription, Payments
from lessons.paginators import LessonPaginator, CoursePaginator
from lessons.permissions import IsOwner, IsModerator
from lessons.serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer, LessonCreateSerializer, \
    PaymentsSerializer


# Create your views here.
class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = CoursePaginator

    def get_permissions(self):
        """Права доступа"""
        if self.action == 'retrieve':
            permission_classes = [IsAuthenticated, IsOwner | IsModerator | IsAdminUser]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated, IsModerator | IsAdminUser]
        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated, IsModerator | IsAdminUser]
        elif self.action == 'update':
            permission_classes = [IsAuthenticated, IsModerator | IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class PaymentsViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonCreateSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsAdminUser]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = LessonPaginator


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsModerator | IsAdminUser]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsAdminUser]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsAdminUser]


# class QuantityCreateAPIView(generics.CreateAPIView):
#     serializer_class = QuantitySerializer
#
#
# class QuantityListAPIView(generics.ListAPIView):
#     serializer_class = QuantitySerializer
#     queryset = Quantity.objects.all()
#     filter_backends = [DjangoFilterBackend, OrderingFilter]  # Бэкенд для обработки фильтра
#     filterset_fields = ('course', 'lesson')  # Набор полей для фильтрации
#     ordering_fields = ('payment_date', 'payment_type',)


# class CourseQuantityListAPIView(generics.ListAPIView):
#     queryset = Quantity.objects.filter(course__isnull=False)
#     serializer_class = CourseQuantitySerializer


class SubscriptionCreateAPIView(generics.CreateAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        course_id = kwargs.get('course_id')
        course = Course.objects.get(pk=course_id)
        if Subscription.objects.filter(user=request.user, course=course).exists():
            return Response({'detail': 'Вы уже подписаны на этот курс'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data={'user': request.user.id, 'course': course.id})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response({'detail': 'Вы успешно подписались на курс.'}, status=status.HTTP_201_CREATED)


class SubscriptionDestroyAPIView(generics.DestroyAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]
    queryset = Subscription.objects.all()

    def get_object(self):
        course_id = self.kwargs.get('course_id')
        course = Course.objects.get(pk=course_id)
        return Subscription.objects.get(user=self.request.user, course=course)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'detail': 'Вы успешно отписались от курса.'}, status=status.HTTP_200_OK)


