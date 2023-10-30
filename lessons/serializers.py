from rest_framework import serializers

from lessons.models import Course, Lesson, LessonsQty


class LessonsQtySerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonsQty
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(source='lesson_set', many=True)

    class Meta:
        model = Course
        fields = '__all__'





class LessonCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'

    def create(self, validated_data):
        lessonsqty = validated_data.pop('lessonsqty')

        lesson_item = Lesson.objects.create(**validated_data)

        for q in lessonsqty:
            LessonsQty.objects.create(**q, lesson=lesson_item)

        return lesson_item


class CourseLessonsQtySerializer(serializers.ModelSerializer):
    course = CourseSerializer()

    class Meta:
        model = LessonsQty
        fields = ('lessonsqty', 'course', 'lesson',)


class CourseCreateSerializer(serializers.ModelSerializer):
    lessonsqty = LessonsQtySerializer(many=True)

    class Meta:
        model = Course
        fields = '__all__'

    def create(self, validated_data):
        lessonsqty = validated_data.pop('lessonsqty')

        course_item = Course.objects.create(**validated_data)

        for q in lessonsqty:
            LessonsQty.objects.create(**q, course=course_item)

        return course_item
