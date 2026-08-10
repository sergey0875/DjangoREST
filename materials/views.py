from rest_framework import viewsets, generics

from materials.serializers import CourseSerializer, LessonSerializer
from materials.models import Course, Lesson




class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()




class LessonCreateAPIview(generics.CreateAPIView):
    serializer_class = LessonSerializer


class LessonListAPIview(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()



class LessonRetrieveAPIview(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()



class LessonUpdateAPIview(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonDestroyAPIview(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
