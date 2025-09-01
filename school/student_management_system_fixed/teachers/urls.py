
from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.teacher_dashboard, name="teacher_dashboard"),
    path("course/<int:course_id>/", views.teacher_course_detail, name="teacher_course_detail"),
    path("edit_grade/<int:student_id>/<int:course_id>/", views.edit_student_grade, name="edit_student_grade"),
]


