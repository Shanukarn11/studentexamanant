from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name='home'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('student-login/', views.student_login, name='student_login'),
    path('upload-students/', views.upload_students, name='upload_students'),
    path('view-students/', views.view_students, name='view_students'),
    path('view-baseline/', views.view_baseline, name='view_baseline'),
    path('upload-baseline/', views.upload_baseline, name='upload_baseline'),
    path('students/download/', views.download_students, name='download_students'),
]
