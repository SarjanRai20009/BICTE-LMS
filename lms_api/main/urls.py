from django.urls import path
from . import views
from .views import *
from .views import index_view
from .views import LogoutView, AdminDashboard


from rest_framework.routers import DefaultRouter




urlpatterns = [
    # Template views
    path('', views.BaseView.as_view(), name='base'),
    path('main/', views.MainView.as_view(), name='main'),
    path('news/', views.NewsView.as_view(), name='news'),
    # path('home/', views.IndexView.as_view(), name='index'),
    path('home/', views.index_view, name='index'),
    path('course-detail/<int:course_id>', views.CourseDetailView.as_view(), name='course-detail'),
    
    # admin-dashboard view
    path('admin-dashboard/', views.AdminDashboard, name='admin-dashboard'),
    
    # list pages
    path('latest-course/', views.LatestCourseView.as_view(), name='latest-course'),
    path('popular-course/', views.PopularCourseView.as_view(), name='popular-course'),
    path('all-teacher-list/', views.AllTeacherList.as_view(), name='all-teacher-list'),
    path('semester-course/<int:pk>', views.SemesterCourse.as_view(), name='semester-course'),
    
    path('notic-list/', views.NoticeListView.as_view(), name='notic-list'),
    # path('notic-list/', views.NoticeListView.as_view(), name='notic-list'),
    # login, logout
    path('login/', SignIn, name = 'signin'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    
    # search 
     path('search/', views.search, name='search'),
    
    # student template views:
    path('student-home/', views.StudentHomePage.as_view(), name='student'),
    path('student-teacher-detail/<int:pk>/', views.TeacherDetailStudentPage.as_view(), name='student-teacher-detail'),
    path('st-semester-view/<int:pk>/', views.StudentSemesterView.as_view(), name='st-semester-view'),
    path('student-notice-list/', views.StudentNoticeList.as_view(), name='student-notice-list'),
    path('student-profile/', views.StudentProfile.as_view(), name='student-profile'),
    path('student-course/', views.StudentCourse.as_view(), name='student-course'),
    path('student-dashboard/', views.StudentDashboard.as_view(), name='student-dashboard'),
    path('student-dashboard-course/', views.StudentDashboardCourse.as_view(), name='student-dashboard-course'),
    path('student-dashboard-assignment/', views.StudentDashboardAssignment.as_view(), name='student-dashboard-assignment'),
    path('student-profile-setting/', views.StudentProfileSetting.as_view(), name='student-profile-setting'),
    path('update-student-profile/', views.UpdateStudentProfile.as_view(), name='update-student-profile'),
    
    path('st-course-detail/<int:course_id>/', views.STCourseDetailView.as_view(), name='st-course-detail'),
    
    path('change-student-account-password/', views.ChangeStudentPassword.as_view(), name='change-student-account-password'),
    # Todo List
    # path("quizzes/", QuizListView.as_view(), name="quiz-list"),
    # path("quizzes/<int:quiz_id>/", QuizDetailView.as_view(), name="quiz-detail"),
    # path("quizzes/<int:quiz_id>/attempt/", QuizAttemptView.as_view(), name="quiz-attempt"),
    # path("quizzes/<int:quiz_id>/leaderboard/", LeaderboardView.as_view(), name="quiz-leaderboard"),
    path("leaderboard/", views.Leaderboard.as_view(), name = "leaderboard"),
    
    
    
    # teacher template views:
    path('teacher-home/', views.TeacherHomePage.as_view(), name='teacher-home'),
    path('teacher-dashboard/', views.TeacherDashboard.as_view(), name='teacher-dashboard'),   
    path('teacher-dashboard-courses/', views.TeacherDashboardCourses.as_view(), name='teacher-courses'),
    path('teacher-dashboard-assignments/', views.TeacherDassboardAssignments.as_view(), name='teacher-assignments'),
    path('teacher-profile-setting/', views.TeacherDashpoardProfileSeting.as_view(), name='teacher-profile-setting'),
    path('teacher-change-password/', views.TeacherDashboardChangePassword.as_view(), name='teacher-change-password'),
    path('teacher-details/<int:pk>', views.TeacherDetails.as_view(), name='teacher-details'),
    path('base-teacher-details/<int:pk>', views.BaseTeacherDetails.as_view(), name='base-teacher-details'),

    # API views with explicit names
    path('teacher/', views.TeacherList.as_view(), name='api-teacher-list'),
    path('teacher/<int:pk>/', views.TeacherDetail.as_view(), name='api-teacher-detail'),
    
    path('semester/', views.SemesterList.as_view(), name='api-semester-list'),
    path('semester/<int:pk>/', views.SemesterDetail.as_view(), name='api-semester-detail'),
    
    path('student/', views.StudentList.as_view(), name='api-student-list'),
    path('student/<int:pk>/', views.StudentDetail.as_view(), name='api-student-detail'),
    
    path('course/', views.CourseList.as_view(), name='api-course-list'),
    path('course/<int:pk>/', views.CourseDetail.as_view(), name='api-course-detail'),

    path('assignment/', views.AssignmentList.as_view(), name='api-assignment-list'),
    path('assignment/<int:pk>/', views.AssignmentDetail.as_view(), name='api-assignment-detail'),

    path('material-type/', views.MaterialTypeList.as_view(), name='api-materialtype-list'),
    path('material-type/<int:pk>/', views.MaterialTypeDetail.as_view(), name='api-materialtype-detail'),

    path('course-material/', views.CourseMaterialList.as_view(), name='api-coursematerial-list'),
    path('course-material/<int:pk>/', views.CourseMaterialDetail.as_view(), name='api-coursematerial-detail'),
    
    path('result/', views.ResultList.as_view(), name='api-result-list'),
    path('result/<int:pk>/', views.ResultDetail.as_view(), name='api-result-detail'),
    
    path('notice/', views.NoticeList.as_view(), name='api-notice-list'),
    path('notice/<int:pk>/', views.NoticeDetail.as_view(), name='api-notice-detail'),
    
    path('course-objectives/', CourseObjectivesList.as_view(), name='api-course-objectives-list'),
    path('course-objectives/<int:pk>/', CourseObjectivesDetail.as_view(), name='api-course-objectives-detail'),
    
    path('books/', views.BookListCreateAPIView.as_view(), name='api-book-list-create'),
    path('books/<int:id>/', views.BookRetrieveUpdateDestroyAPIView.as_view(), name='api-book-detail'),

]