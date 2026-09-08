from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from materials.models import Course, Lesson, Subscriptions
from users.models import Payments
from materials.validators import validate_video_url


class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.URLField(validators=[validate_video_url])


    class Meta:
        model = Lesson
        fields = '__all__'





class CourseSerializer(serializers.ModelSerializer):
    world_lesson = LessonSerializer(source= 'lessons', many=True, read_only=True)
    course_count_lesson = SerializerMethodField()
    is_subscribed = SerializerMethodField()


    class Meta:
        model = Course
        fields = '__all__'

    def get_course_count_lesson(self, obj):
        return Lesson.objects.filter(course=obj).count()

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Subscriptions.objects.filter(user=request.user, course=obj).exists()
        return False


class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = '__all__'
