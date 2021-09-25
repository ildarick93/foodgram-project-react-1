from django.contrib import admin
from .models import Follow
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
User = get_user_model()

class CustomUserAdmin(UserAdmin):
    list_filter = (
        ('username', admin.EmptyFieldListFilter),
        ('email', admin.EmptyFieldListFilter),
    )

class FollowAdmin(admin.ModelAdmin):
    list_display = ('subscriber', 'subscribed_to')


admin.site.register(Follow, FollowAdmin)
admin.site.register(User, CustomUserAdmin)