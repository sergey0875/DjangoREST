from django.db import models



class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name="название")
    description = models.TextField(null=True, blank=True, verbose_name="описание")
    preview = models.ImageField(
        upload_to="photos/",
        blank=True,
        null=True,
        verbose_name="картинка",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"


class Lesson(models.Model):
    name = models.CharField(max_length=100, verbose_name="название")
    description = models.TextField(null=True, blank=True, verbose_name="описание")
    preview = models.ImageField(
        upload_to="photos/",
        blank=True,
        null=True,
        verbose_name="картинка",
    )
    video_url = models.URLField(max_length=500, verbose_name="Ссылка на видео")
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name="Курс"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"
