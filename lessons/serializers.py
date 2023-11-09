from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from lessons.models import Course, Lesson, Subscription, Payments
from lessons.services import get_session_by_stripe_id
from lessons.validators import LinkValidator


# class QuantitySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Quantity
#         fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'

    # def get_quantity(self, instance):
    #     if instance.quantity.all():
    #         return instance.quantity.all().quantity
    #     return 0


class CourseSerializer(serializers.ModelSerializer):
    # lessons = LessonSerializer(source='lesson_set', many=True)
    lessons_count = SerializerMethodField()
    is_subscribed = SerializerMethodField()

    def get_lessons_count(self, course):
        return course.lesson_set.count()

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return Subscription.objects.filter(user=user, course=obj).exists()

    class Meta:
        model = Course
        fields = '__all__'


# class CourseQuantitySerializer(serializers.ModelSerializer):
#     quantity = CourseSerializer()
#
#     class Meta:
#         model = Quantity
#         fields = ('quantity', 'course', 'lesson',)


class LessonCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [
            LinkValidator(field='link')
        ]

    # def validate(self, attrs):
    #     #validate_link(attrs)
    #     return attrs

    # def create(self, validated_data):
    #     quantity = validated_data.pop('quantity')
    #
    #     lesson_item = Lesson.objects.create(**validated_data)
    #
    #     for q in quantity:
    #         Lesson.objects.create(**q, lesson=lesson_item)
    #
    #     return lesson_item


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'


class PaymentsSerializer(serializers.ModelSerializer):
    url = SerializerMethodField(read_only=True)

    class Meta:
        model = Payments
        fields = '__all__'

    def get_url(self, obj):
        session = get_session_by_stripe_id(obj.session)
        return session.url
