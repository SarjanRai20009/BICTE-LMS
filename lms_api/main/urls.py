from django.urls import path
from . import views

urlpatterns = [
    path('teacher/', views.TeacherList.as_view()),
    path('teacher/<int:pk>/', views.TeacherDetail.as_view()),
    
    path('semester/', views.SemesterList.as_view()),
    # path('semester/<int:pk>/', views.SemesterDetail.as_view()),  # Add detail view
]