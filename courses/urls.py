from django.urls import path
from . import views
from .certificate import generate_certificate

urlpatterns = [
    path("", views.home, name="home"),

    path("courses/", views.course_list, name="course"),

    path(
        "course/<int:id>/",
        views.course_detail,
        name="course_detail"
    ),

    path(
        "enroll/<int:id>/",
        views.enroll_course,
        name="enroll_course"
    ),

    path(
        "my-courses/",
        views.my_courses,
        name="my_courses"
    ),

    path(
        "dashboard/",
        views.dashboard,
        name="dashboard"
    ),

    path(
        "complete/<int:id>/",
        views.complete_course,
        name="complete_course"
    ),

    path(
    "certificate/<int:enrollment_id>/",
    views.certificate,
    name="certificate"
    ),
    path("profile/", views.profile, name="profile"),
    path("rate/<int:course_id>/", views.rate_course, name="rate_course"),


    path("courses/", views.course_list, name="course_list"),


]
