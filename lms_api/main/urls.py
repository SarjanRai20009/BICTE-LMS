from django.urls import path
from . import views

urlpatterns = [
    # Template views
    
    path('', views.IndexView.as_view(), name='index'),

    
    
    # Api views

    path('teacher/', views.TeacherList.as_view()),
    path('teacher/<int:pk>/', views.TeacherDetail.as_view()),
    
    path('semester/', views.SemesterList.as_view()),
    path('semester/<int:pk>/', views.SemesterDetail.as_view()),  # Add detail view
    
    path('student/', views.StudentList.as_view()),
    path('student/<int:pk>/', views.StudentDetail.as_view()),  # Add detail view
]