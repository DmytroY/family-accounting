from django.contrib import admin
from .models import Member, Profile
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class MemberAdmin(admin.ModelAdmin):
    list_display = ("firstname", "lastname", "email",)

admin.site.register(Member, MemberAdmin)

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False

class CustomUserAdmin(UserAdmin):
    inlines = [ProfileInline]

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
