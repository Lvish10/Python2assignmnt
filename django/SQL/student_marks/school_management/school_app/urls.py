from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add_student/', views.add_student, name='add_student'),
    path('view_students/', views.view_students, name='view_students'),
    path('teacher_login/', views.teacher_login, name='teacher_login'),
    path('student_login/', views.student_login, name='student_login'),
    path('teacher_dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('student_dashboard/<str:student_id>/', views.student_dashboard, name='student_dashboard'),
    path('view_marks/<str:student_id>/', views.view_marks, name='view_marks'),
    path('view_attendance/<str:student_id>/', views.view_attendance, name='view_attendance'),
    path('add_marks/', views.add_marks, name='add_marks'),
    path('manage_attendance/', views.manage_attendance, name='manage_attendance'),
    path('teacher_visualizations/', views.teacher_visualizations, name='teacher_visualizations'),
    path('view_modules/<str:student_id>/', views.view_modules, name='view_modules'),
    path('view_quizzes/<str:student_id>/', views.view_quizzes, name='view_quizzes'),
    path('generate_report_card/<str:student_id>/', views.generate_report_card, name='generate_report_card'),
]