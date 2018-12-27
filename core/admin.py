from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from core import models

admin.site.register(models.UserProfile, UserAdmin)
admin.site.register(models.UserFollowing)


class UserAdmin(UserAdmin):
    list_display = ('email', 'username', 'first_name', 'mobile_number',)
