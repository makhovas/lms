from rest_framework import serializers

from lessons.models import Course, Lesson, Quantity


class QuantitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Quantity
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    quantity = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = '__all__'

    def get_quantity(self, instance):
        if instance.quantity.all():
            return instance.quantity.all().quantity
        return 0


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(source='lesson_set', many=True)

    class Meta:
        model = Course
        fields = '__all__'


class CourseQuantitySerializer(serializers.ModelSerializer):
    quantity = CourseSerializer()

    class Meta:
        model = Quantity
        fields = ('quantity', 'course', 'lesson',)


class LessonCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'

    def create(self, validated_data):
        quantity = validated_data.pop('quantity')

        lesson_item = Lesson.objects.create(**validated_data)

        for q in quantity:
            Lesson.objects.create(**q, lesson=lesson_item)

        return lesson_item
