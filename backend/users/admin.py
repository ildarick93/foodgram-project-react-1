from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import Follow

User = get_user_model()


class CustomUserAdmin(UserAdmin):
    list_filter = (
        ('username', admin.EmptyFieldListFilter),
        ('email', admin.EmptyFieldListFilter),
    )


class FollowAdmin(admin.ModelAdmin):
    list_display = ('subscriber', 'subscribed_to')


admin.site.register(Follow)
