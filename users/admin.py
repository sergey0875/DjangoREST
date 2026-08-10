from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class UsersAdmin(admin.ModelAdmin):
    list_display = ("id", "avatar", "number_phone","email", "city",)
    search_fields = ("number_phone", "city",)
