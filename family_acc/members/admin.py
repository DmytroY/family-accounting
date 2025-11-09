from django.contrib import admin
from .models import Member, Profile
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


admin.site.register(Member)

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False

class CustomUserAdmin(UserAdmin):
    list_display = ("username", "first_name", "last_name", "email", "is_staff", "get_family")
    inlines = [ProfileInline]

    def get_family(self, obj):
        return obj.profile.family if hasattr(obj, 'profile') else ""
    
    get_family.short_description = "Family"

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
