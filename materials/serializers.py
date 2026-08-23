from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from materials.models import Course, Lesson
from users.models import Payments


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'



class CourseSerializer(serializers.ModelSerializer):
    world_lesson = LessonSerializer(source= 'lessons', many=True, read_only=True)
    course_count_lesson = SerializerMethodField()


    class Meta:
        model = Course
        fields = '__all__'

    def get_course_count_lesson(self, obj):
        return Lesson.objects.filter(course=obj).count()


class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = '__all__'
