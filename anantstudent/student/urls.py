from django.urls import path
from . import views

urlpatterns = [
    path('student-login/', views.student_login_view, name='student_login'),
    path('admin-login/', views.admin_login_view, name='admin_login'),
    path('admin/upload/', views.csv_upload_view, name='csv_upload'),
    path('admin/students/', views.student_list_view, name='student_list'),
]