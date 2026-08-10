from unittest.mock import patch

from django.urls import path

from materials.apps import MaterialsConfig
from rest_framework.routers import DefaultRouter
from materials.views import CourseViewSet, LessonCreateAPIview, LessonListAPIview, LessonRetrieveAPIview, \
    LessonUpdateAPIview, LessonDestroyAPIview

app_name = MaterialsConfig.name


router = DefaultRouter()
router.register(r'materials', CourseViewSet, basename='materials' )


urlpatterns = [
    path('lesson/create/', LessonCreateAPIview.as_view(), name= 'lesson_create'),
    path('lesson/', LessonListAPIview.as_view(), name= 'lesson_list'),
    path('lesson/<int:pk>', LessonRetrieveAPIview.as_view(), name= 'lesson_get'),
    path('lesson/update/<int:pk>', LessonUpdateAPIview.as_view(), name= 'lesson_update'),
    path('lesson/delete/<int:pk>', LessonDestroyAPIview.as_view(), name= 'lesson_delete '),
] + router.urls
