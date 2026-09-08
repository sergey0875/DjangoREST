from django.template.context_processors import request
from rest_framework.response import Response

from materials.models import Subscriptions
from rest_framework import viewsets, generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from materials.paginators import CustomPagination
from materials.serializers import CourseSerializer, LessonSerializer
from materials.models import Course, Lesson
from users.permissions import IsModerator, IsOwnerOrReadOnly


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = (~IsModerator,)
        elif self.action in ['update', 'retrieve']:
            self.permission_classes = (IsModerator | IsOwnerOrReadOnly,)
        elif self.action == 'destroy':
            self.permission_classes = (~IsModerator | IsOwnerOrReadOnly,)
        return super().get_permissions()



class LessonCreateAPIview(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)




class LessonListAPIview(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = CustomPagination


    def get_queryset(self):
        """
        Если зашел модератор — отдаем все уроки.
        Если обычный пользователь — фильтруем и отдаем ТОЛЬКО его уроки.
        """
        if self.request.user.groups.filter(name='Moderator').exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)




class LessonRetrieveAPIview(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwnerOrReadOnly]
    pagination_class = CustomPagination



class LessonUpdateAPIview(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwnerOrReadOnly]


class LessonDestroyAPIview(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, ~IsModerator | IsOwnerOrReadOnly]


class SubscriptionAPIView(APIView):
      permission_classes = [IsAuthenticated]

      def post(self, request):

            """Добавление и удаление подписки"""

            user = request.user
            course_id = request.data.get('course_id')
            course_item = get_object_or_404(Course, id=course_id)
            subs_item  =  Subscriptions.objects.filter(user=user, course=course_item)

            if subs_item.exists():
                subs_item.delete()
                message = 'подписка удалена'


            else:
                Subscriptions.objects.create(user=user, course=course_item) # записываем в базу данных
                message = 'подписка добавлена'

            return Response({"message": message})



