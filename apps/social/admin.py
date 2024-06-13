from django.contrib import admin
from apps.social.models import FriendRequest


# Register your models here.
@admin.register(FriendRequest)
class UserAdmin(admin.ModelAdmin):
    """
    admin interface for Request Model.
    """
    list_display = ['id', 'to_user', 'from_user']
