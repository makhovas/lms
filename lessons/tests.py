from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Course, Lesson, Subscription

User = get_user_model()


class LessonCRUDTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@mail.ru', password='test1234', is_staff=True, is_superuser=True)
        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(
            title='Test Course',
            description='Test Course Description',
            owner=self.user
        )
        self.lesson = Lesson.objects.create(
            title='Test Lesson',
            description='Test Lesson Description',
            course=self.course
        )

    def test_create_lesson(self):
        link = reverse('lessons:lesson-create')
        data = {
            'title': 'New Lesson',
            'description': 'New Lesson Description',
            'link': 'https://www.youtube.com/testlesson',
            'course': self.course.id
        }
        response = self.client.post(link, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_lesson(self):
        link = reverse('lessons:lesson-get', args=[self.lesson.id])
        response = self.client.get(link)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_lesson(self):
        link = reverse('lessons:lesson-update', args=[self.lesson.id])
        data = {
            'title': 'Updated Lesson',
            'description': 'Updated Lesson Description',
            'link': 'https://www.youtube.com/testlesson',
            'course': self.course.id
        }
        response = self.client.put(link, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_lesson(self):
        link = reverse('lessons:lesson-delete', args=[self.lesson.id])
        response = self.client.delete(link)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class SubscriptionTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@mail.ru', password='test1234', is_staff=True, is_superuser=True)
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(
            title='Test Course',
            description='Test Course Description',
            owner=self.user
        )

    def test_subscribe_to_course(self):
        link = reverse('lessons:create-subscription', args=[self.course.id])
        response = self.client.post(link, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_unsubscribe_from_course(self):
        Subscription.objects.create(user=self.user, course=self.course)
        link = reverse('lessons:delete-subscription', args=[self.course.id])
        response = self.client.delete(link, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())
