from django.contrib import admin
from materials.models import Course, Lesson, Subscriptions


class SubscriptionsInline(admin.TabularInline):
    model = Subscriptions
    extra = 1
    fields = ('user',)

@admin.register(Course)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id","name", "description", "preview")
    list_filter = ("name",)
    search_fields = ("name", "description",)


@admin.register(Lesson)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id","name", "description", "preview", "video_url")
    search_fields = ("name", "description",)

@admin.register(Subscriptions)
class SubscriptionsAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "course")
    list_filter = ("course", "user")
