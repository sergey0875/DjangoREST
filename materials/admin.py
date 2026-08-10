from django.contrib import admin
from materials.models import Course, Lesson



@admin.register(Course)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id","name", "description", "preview")
    list_filter = ("name",)
    search_fields = ("name", "description",)


@admin.register(Lesson)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id","name", "description", "preview", "video_url")
    search_fields = ("name", "description",)
