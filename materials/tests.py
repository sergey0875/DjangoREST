from django.urls import reverse
from rest_framework import status
from  rest_framework.test import APITestCase

from materials.models import Lesson, Course
from users.models import CustomUser


class CourseTestCase(APITestCase):


    def setUp(self):

        self.user = CustomUser.objects.create(email="Mirnoy@mail.ru")
        self.course = Course.objects.create(name="курс английского", owner=self.user)
        self.lesson = Lesson.objects.create(name="урок английского",owner=self.user, course=self.course, description="быстрый урок")
        self.client.force_authenticate(user=self.user)


    def test_course(self):
        url = reverse("materials:materials-detail", args=(self.course.pk,))
        response =self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), "курс английского")



    def test_course_create(self):

        """Тестирование создания курса"""

        url = reverse("materials:materials-list")
        data = {

            "name": "Course",
            "description": "course2",
        }
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json().get("name"), "Course")


    def test_course_update(self):

        """Тестирование редоктирования курса"""

        url = reverse("materials:materials-detail", args=(self.course.pk,))

        data = {

            "name": "Venom",
            "description": "venom2",
        }
        response = self.client.patch(url, data=data)


        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("name"), "Venom")



    def test_course_delete(self):

        """Тестирование удаления курса"""

        url = reverse("materials:materials-detail", args=(self.course.pk,))

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.all().count(), 0)



    def test_lesson_create(self):

        """ тестирование создание урока"""

        data = {

            "name": "test",
            "description": "tests",
            "course": self.course.pk,
            "video_url": "http://youtube.com/"

        }

        response = self.client.post(
            "/lesson/create/",
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json().get("name"), "test")
        self.assertEqual(response.json().get("description"), "tests")
        self.assertEqual(response.json().get("video_url"), "http://youtube.com/")

        self.assertTrue(
            Lesson.objects.all().exists() # проверка записив базу данных
        )
        self.assertEqual(Lesson.objects.all().count(), 2) #Проверка количества уроков


    def test_lesson_update(self):

        """Тестирование обновления урока"""

        url = reverse("materials:lesson_update", args=(
        self.lesson.pk,))

        data = {
            "name": "обновленное название урока",
            "description": "новое описание урока",
            "course": self.course.pk,
            "video_url": "http://youtube.com/"
        }

        response = self.client.patch(url, data=data)


        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("name"), 'обновленное название урока')
        self.assertEqual(response.json().get("description"), "новое описание урока")


    def test_lesson_delete(self):
        """Тестирование удаление существующего урока"""

        url = reverse("materials:lesson_delete", args=(
        self.lesson.pk,))

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.all().count(), 0)



    def test_course_subscription_toggle(self):

        """Тестирование функционала подписки/отписки от обновлений курса"""

        url = reverse("materials:course_subscribe")
        data = {
            "course_id": self.course.pk
        }

        response = self.client.post(url, data=data)

        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_201_CREATED])

        response_data = response.json()
        self.assertEqual(response_data.get("message"), "подписка добавлена")


        response_toggle = self.client.post(url, data=data)

        self.assertEqual(response_toggle.status_code, status.HTTP_200_OK)
        response_toggle_data = response_toggle.json()
        self.assertEqual(response_toggle_data.get("message"), "подписка удалена")
