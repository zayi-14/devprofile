from django.contrib import admin
from .models import Profile, Skill, Project, Message


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "email")


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "level")
    list_filter = ("category",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "role", "start_date", "end_date")
    list_filter = ("skills_used", "start_date")
    readonly_fields = ("slug",)  # hide editing
    filter_horizontal = ("skills_used",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "is_read", "created_at")
    list_filter = ("is_read",)
