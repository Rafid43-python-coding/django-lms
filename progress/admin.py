from django.contrib import admin
from .models import StudentProgress

@admin.register(StudentProgress)
class StudentProgressAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "course",
        "completed_lessons",
        "total_lessons",
        "progress",
        "completed",
        "updated_at",
    )

    list_filter = ("completed", "course")

    search_fields = (
        "student__username",
        "course__title",
    )

    list_editable = (
        "completed_lessons",
        "total_lessons",
    )

