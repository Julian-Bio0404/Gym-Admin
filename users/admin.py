"""User models admin."""

# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Models
from users.models import User, Profile, Membership


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """User model admin."""

    list_display = (
        'email', 'username', 
        'first_name', 'last_name',
        'type_identification', 'identification_number',
        'rol', 'is_verified'
    )

    list_filter = (
        'rol', 'created', 'modified'
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Profile model admin."""

    list_display = (
        'user', 'is_active', 'age',
        'weight', 'height'
    )

    search_fields = (
        'user__username', 'user__email', 
        'user__first_name', 'user__last_name'
    )

    list_filter = ('is_active', 'age')


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    """Membership model admin."""

    list_display = (
        'user', 'available_days', 
        'category'
    )
