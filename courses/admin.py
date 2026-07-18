from django.contrib import admin
from .models import Course, Enrollment
from .models import Rating


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "instructor", "category", "price")
    list_filter = ("category",)
    search_fields = ("title", "description", "instructor")


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "enrolled_at")
    search_fields = ("student__username", "course__title")

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("course", "user","rating","created_at" )
