from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.utils.decorators import method_decorator


from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import generics
from django.views.generic import TemplateView

from django.contrib.auth.decorators import login_required, user_passes_test

from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets

from django.db.models import Q

from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy, reverse


from django.views.generic import TemplateView
from django.views import View

# Explicit import

from .serializers import *


from . import models


from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from .models import Teacher, Semester, Student, Course, MaterialType, CourseMaterial, Assignment
from .serializers import (
    TeacherSerializer, SemesterSerializer, StudentSerializer,
    CourseSerializer, MaterialTypeSerializer, CourseMaterialSerializer,
    AssignmentSerializer
)


from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Teacher, Student
import json
# Testing


# Create your views here.

# suggested code
# class TeacherList(APIView):
#     def get(self, request):
#         teachers = Teacher.objects.all()
#         teachers = models.Teacher.objects.all()
#         serializer = Teacherserializer(teachers, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

# used code of the above suggestion
# class index(APIView):
#     def get(self, request):
#         return Response("Hello World", status=status.HTTP_200_OK)





# Template-Based View
class BaseView(TemplateView):
    template_name = 'base_template/base.html'


# @login_required('/')
class MainView(TemplateView):
    template_name = 'base_template/main.html'

 
    
class NewsView(TemplateView):
    template_name = 'frontends/news.html'

@login_required(login_url='/api/login/')
def index_view(request):
    latest_notices = Notice.objects.all().order_by('-timestamp')[:5] 
    

    
    return render(request, 'frontends/index.html', {'latest_notices': latest_notices})


class SemesterCourse(TemplateView):
    template_name = 'frontends/semester_wise_course.html' 
    
class NoticeListView(TemplateView):
    template_name = 'frontends/notice_list.html'
    
    
class BaseTeacherDetails(TemplateView):
    template_name = 'teacher_template/noPK_teacher_details.html'
# admin dashboard
# @login_required(login_url='/api/login/')
# def AdminDashboard(request):
#     return render(request, 'frontends/admin-dashboard-basetemplate.html')

@login_required(login_url='/api/login/')
def AdminDashboard(request):
    # Fetch data from the database
    total_teachers = Teacher.objects.count()
    total_students = Student.objects.count()
    total_courses = Course.objects.count()
    active_semesters = Semester.objects.filter(is_active=True).count()
    
    recent_assignments = Assignment.objects.order_by('-deadline')[:5]  # Fetch recent 5 assignments
    recent_materials = CourseMaterial.objects.order_by('-upload_date')[:5]  # Fetch recent 5 materials

    # Pass the data to the template
    context = {
        'admin_name': request.user.username,  # Assuming the admin's name is the username
        'total_teachers': total_teachers,
        'total_students': total_students,
        'total_courses': total_courses,
        'active_semesters': active_semesters,
        'recent_assignments': recent_assignments,
        'recent_materials': recent_materials,
    }
    
    return render(request, 'frontends/admin-dashboard-original.html', context)
   
    
@login_required(login_url='/api/login/')
def search(request):
    query = request.GET.get('q')  # Get the search query from the URL parameter
    courses = assignments = quizzes = students = None  # Initialize variables to avoid UnboundLocalError

    if query:
        # Search across courses, assignments, quizzes, and students
        courses = Course.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
        assignments = Assignment.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
        quizzes = Quiz.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
        students = Student.objects.filter(
            Q(st_name__icontains=query) | Q(st_email__icontains=query) | Q(st_exam_roll_no__icontains=query)
        )
  
    context = {
        'query': query,
        'courses': courses,
        'assignments': assignments,
        'quizzes': quizzes,
        'students': students,
    }
    return render(request, 'frontends/search_results.html', context)


# Student view



# class StudentHomePage(TemplateView):
#     template_name = 'student_template/st_home.html'    
class StudentHomePage(LoginRequiredMixin, TemplateView):
    template_name = 'student_template/st_home.html'
    login_url = '/api/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        try:
           
            student = Student.objects.get(id=self.request.session.get('user_id'))
            context['student'] = student
        except Student.DoesNotExist:
            messages.error(self.request, 'Student not found. Please log in again.')
            return redirect('login')  
        
      
        latest_notices = Notice.objects.all().order_by('-timestamp')[:5]
        context['latest_notices'] = latest_notices

        
        context['courses'] = Course.objects.filter(semester=student.semester)
        context['assignments'] = Assignment.objects.filter(course__semester=student.semester)
        context['quizzes'] = Quiz.objects.filter(course__semester=student.semester)

        return context
    
class StudentProfile(LoginRequiredMixin,TemplateView):
    template_name = 'student_template/student_profile.html'    
    login_url = '/api/login/'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        try:
          
            student = Student.objects.get(id=self.request.session.get('user_id'))
            context['student'] = student
        except Student.DoesNotExist:
            messages.error(self.request, 'Student not found. Please log in again.')
            return redirect('login')  

        latest_notices = Notice.objects.all().order_by('-timestamp')[:5]
        context['latest_notices'] = latest_notices

       
        context['courses'] = Course.objects.filter(semester=student.semester)
        context['assignments'] = Assignment.objects.filter(course__semester=student.semester)
        context['quizzes'] = Quiz.objects.filter(course__semester=student.semester)

        return context
class StudentCourse(LoginRequiredMixin, TemplateView):
    template_name = 'student_template/st_course.html'  
    login_url = '/api/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
         
            student = Student.objects.get(id=self.request.session.get('user_id'))
            context['student'] = student
           
            context['semesters'] = Semester.objects.all()
        except Student.DoesNotExist:
            context['error'] = 'Student not found. Please log in again.'
        return context
class StudentSemesterView(LoginRequiredMixin, TemplateView):
    template_name = 'student_template/st_semester_view.html'
    login_url = '/api/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
     
        semester = get_object_or_404(Semester, id=self.kwargs['pk'])
        context['semester'] = semester
        
      
        context['courses'] = semester.course_set.all()
        context['teachers'] = Teacher.objects.filter(course__semester=semester).distinct()
        context['students'] = semester.student_set.all()
        
 
        context['materials'] = CourseMaterial.objects.filter(course__semester=semester, is_active=True)
        context['assignments'] = Assignment.objects.filter(course__semester=semester)
        

        try:
            student = Student.objects.get(id=self.request.session.get('user_id'))
            context['student'] = student
        except Student.DoesNotExist:
            context['error'] = 'Student not found. Please log in again.'
        
        return context
    
class STCourseDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'student_template/st_course_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        try:
           
            student = Student.objects.get(id=self.request.session.get('user_id'))
            context['student'] = student

          
            course_id = self.kwargs.get('course_id')
            course = get_object_or_404(Course, id=course_id)
            context['course'] = course

          
            course_objectives = CourseObjectives.objects.filter(course=course)
            context['course_objectives'] = course_objectives

            
            course_materials = CourseMaterial.objects.filter(course=course, is_active=True)
            context['course_materials'] = course_materials
            
            semester = course.semester
            context['semester'] = semester
           
            teacher = course.teacher
            context['teacher'] = teacher

            
            related_courses = Course.objects.filter(semester=course.semester).exclude(id=course.id)
            context['related_courses'] = related_courses

        except Student.DoesNotExist:
            context['error'] = 'Student not found. Please log in again.'
        except Course.DoesNotExist:
            context['error'] = 'Course not found.'
        except Exception as e:
            context['error'] = f'An error occurred: {str(e)}'

        return context
    
class StudentDashboard(TemplateView):    
    template_name = 'student_template/st_dashboard.html'  
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
           
            student = Student.objects.get(id=self.request.session.get('user_id'))
            context['student'] = student
            
            context['courses'] = Course.objects.filter(semester=student.semester)
            
        except Student.DoesNotExist:
            context['error'] = 'Student not found. Please log in again.'
        return context
class StudentDashboardAssignment(TemplateView):
    template_name = 'student_template/st_dashboard_assignment.html'  
class StudentDashboardCourse(TemplateView):
    template_name = 'student_template/st_dashboard_course.html' 
    
class StudentProfileSetting(LoginRequiredMixin, TemplateView):
    template_name = 'student_template/st_profile_setting.html'
    login_url = '/api/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
           
            student = Student.objects.get(id=self.request.session.get('user_id'))
            context['student'] = student
            
            
            context['courses'] = Course.objects.filter(semester=student.semester)
            context['assignments'] = Assignment.objects.filter(course__semester=student.semester)
            context['quizzes'] = Quiz.objects.filter(course__semester=student.semester)
           
          
        except Student.DoesNotExist:
            context['error'] = 'Student not found. Please log in again.'
        return context
    
    
class Leaderboard(LoginRequiredMixin, TemplateView):
    template_name = 'student_template/leaderboard.html'
    login_url = '/api/login/'



class UpdateStudentProfile(LoginRequiredMixin, TemplateView):
    def post(self, request, *args, **kwargs):
        try:
  
            student = Student.objects.get(id=request.session.get('user_id'))
            
      
            student.st_exam_roll_no = request.POST.get('st_exam_roll_no')
            student.st_reg_no = request.POST.get('st_reg_no')
            student.st_name = request.POST.get('st_name')
            student.st_date_of_birth = request.POST.get('st_date_of_birth')
            student.st_address = request.POST.get('st_address')
            student.st_contact = request.POST.get('st_contact')
            student.st_email = request.POST.get('st_email')
            student.st_father_name = request.POST.get('st_father_name')
            student.gender = request.POST.get('gender')
            
          
            semester_name = request.POST.get('semester')
            if semester_name:
                semester_instance = Semester.objects.get(se_name=semester_name) 
                student.semester = semester_instance  

            if 'profile_picture' in request.FILES:
                student.profile_picture = request.FILES['profile_picture']
            
            student.save()
            return JsonResponse({'status': 'success', 'message': 'Profile updated successfully!'})
        except Semester.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Invalid semester.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})


class ChangeStudentPassword(TemplateView):
    template_name = 'student_template/change_st_password.html' 
    
    
class StudentNoticeList(LoginRequiredMixin, TemplateView):
    template_name = 'student_template/student_notice_list.html'
    login_url = '/api/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

       
        try:
            student = Student.objects.get(id=self.request.session.get('user_id'))
            context['student'] = student
        except Student.DoesNotExist:
            context['student'] = None  

 
        notices = Notice.objects.all().order_by('-timestamp')

       
        notices_with_post_by = []
        for notice in notices:
            post_by = notice.user.username  
            notices_with_post_by.append({
                'notice': notice,
                'posted_by': post_by
            })

        if not notices:
            context['error'] = 'No notices found.' 

        context['notices'] = notices_with_post_by
        return context

# class TeacherDetailStudentPage(LoginRequiredMixin,TemplateView):
#     template_name = 'student_template/st_teacher_view.html'    
#     login_url = '/api/login/'
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         try:
         
#             student = Student.objects.get(id=self.request.session.get('user_id'))
#             context['student'] = student
           
       
#         except Student.DoesNotExist:
#             context['error'] = 'Student not found. Please log in again.'
#         return context

class TeacherDetailStudentPage(LoginRequiredMixin, TemplateView):
    template_name = 'student_template/st_teacher_view.html'    
    login_url = '/api/login/'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Fetch the teacher based on the pk from the URL
        teacher = get_object_or_404(Teacher, id=self.kwargs['pk'])
        context['teacher'] = teacher
        
        try:
            # Fetch the student based on the session user_id
            student = Student.objects.get(id=self.request.session.get('user_id'))
            context['student'] = student
        except Student.DoesNotExist:
            context['error'] = 'Student not found. Please log in again.'
        
        return context

    
# end student view 

# Teacher view
class TeacherHomePage(TemplateView):
    template_name = 'teacher_template/t_index.html'

   

class TeacherIndexPage(TemplateView):
    template_name = 'teacher_template/t_home.html'
    
class TeacherDashboard(TemplateView):
    template_name = 'teacher_template/t_dashboard.html'

class TeacherDashboardCourses(TemplateView):
    template_name = 'teacher_template/t_dashboard.html'
    
class TeacherDassboardAssignments(TemplateView):
    template_name = 'teacher_template/teacher_dashboard_assignments.html'
class TeacherDashpoardProfileSeting(TemplateView):
    template_name = 'teacher_template/t_profile_setting.html'

class TeacherDashboardChangePassword(TemplateView):
    template_name = 'teacher_template/change_t_password.html'


class TeacherDetails(TemplateView):
    template_name = 'teacher_template/t_details.html'
    
# class AllTeacherList(TemplateView):
#     template_name = 'teacher_template/all_teacher_list.html'
def is_superuser(user):
    return user.is_authenticated and user.is_superuser

# Class-based view for listing all teachers
class AllTeacherList(View):
    @method_decorator(login_required)
    @method_decorator(user_passes_test(is_superuser))
    def get(self, request, *args, **kwargs):
        teachers = Teacher.objects.all()
        return render(request, 'teacher_template/all_teacher_list.html', {'teachers': teachers})


#teacher view end
    
    
class CourseDetailView(TemplateView):
    template_name = 'frontends/course_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course_id = kwargs.get('course_id')
        context['course_id'] = course_id
        return context
    

    
class LatestCourseView(TemplateView):
    template_name = 'frontends/latest_course.html' 
    
class PopularCourseView(TemplateView):
    template_name = 'frontends/popular_courses.html' 





def SignIn(request):
    if request.method == 'POST':
        username = request.POST.get('username') 
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')
        
       
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            request.session['user_id'] = user.id
            request.session['user_role'] = 'user'
            return redirect('/api/home/')

       
        try:
           
            teacher = Teacher.objects.filter(t_email=username).first() or \
                      Teacher.objects.filter(t_full_name__iexact=username).first()
            
            if teacher and teacher.check_password(password):
                request.session['user_role'] = 'teacher'
                request.session['user_id'] = teacher.id
                if remember_me:
                    request.session.set_expiry(86400)  
                else:
                    request.session.set_expiry(0)
                return redirect('/api/teacher-home/')
        except Teacher.DoesNotExist:
            pass
        
       
        try:
          
            student = Student.objects.filter(st_email=username).first() or \
                      Student.objects.filter(st_name__iexact=username).first()
            
            if student and student.check_password(password):
                request.session['user_role'] = 'student'
                request.session['user_id'] = student.id
                if remember_me:
                    request.session.set_expiry(86400) 
                else:
                    request.session.set_expiry(0)
                return redirect('/api/student-home/')
        except Student.DoesNotExist:
            pass
        
      
        error_message = "Invalid login credentials. Please try again!"
        return render(request, 'auth_template/login.html', {'error_message': error_message})
    
  
    if request.user.is_authenticated:
        user_role = request.session.get('user_role')
        if user_role == 'teacher':
            return redirect('/api/teacher-home/')
        elif user_role == 'student':
            return redirect('/api/student-home/')
        elif user_role == 'user':
            return redirect('/api/home/')
    
    return render(request, 'auth_template/login.html')




class LogoutView(View):
    def get(self, request):
        """Logs out the user and redirects them to the base template."""
        logout(request)  
        return redirect('/api/')


    
    
    
    
# Generic views



class TeacherList(generics.ListCreateAPIView):
    queryset = models.Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
      
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save() 
            return Response({
                "message": "Teacher added successfully!",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TeacherDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [permissions.IsAuthenticated]
class BookListCreateAPIView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

class BookRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    permission_classes = [permissions.IsAuthenticated]
    
class SemesterList(generics.ListCreateAPIView):    
    queryset = models.Semester.objects.all()
    serializer_class = SemesterSerializer       
    permission_classes = [permissions.IsAuthenticated]
    
def create(self, request, *args, **kwargs):      
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save() 
            return Response({
                "message": "Semester added successfully!",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class SemesterDetail(generics.RetrieveUpdateDestroyAPIView):   
    queryset = models.Semester.objects.all()
    serializer_class = SemesterSerializer
    permission_classes = [permissions.IsAuthenticated]
    
def create(self, request, *args, **kwargs):      
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  
            return Response({
                "message": "Semester added successfully!",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class StudentList(generics.ListCreateAPIView):
    queryset = models.Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
      
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Student added successfully!",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class StudentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def delete(self, request, *args, **kwargs):
        """
        Override the delete method to handle deletion properly.
        After successfully deleting the student, return a success response.
        """
        student = self.get_object()
        student.delete() 
        return Response({
            "message": "Student deleted successfully!"
        }, status=status.HTTP_204_NO_CONTENT)
        
class CourseList(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]

def create(self, request, *args, **kwargs):      
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  
            return Response({
                "message": "Course added successfully!",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CourseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]

class AssignmentList(generics.ListCreateAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
def create(self, request, *args, **kwargs):      
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save() 
            return Response({
                "message": "Assignment added successfully!",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class AssignmentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
class MaterialTypeList(generics.ListCreateAPIView):
    queryset = models.MaterialType.objects.all()
    serializer_class = MaterialTypeSerializer
    permission_classes = [permissions.IsAuthenticated]
def create(self, request, *args, **kwargs):      
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Material Type added successfully!",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class MaterialTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.MaterialType.objects.all()
    serializer_class = MaterialTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

class CourseMaterialList(generics.ListCreateAPIView):
    queryset = models.CourseMaterial.objects.all()
    serializer_class = CourseMaterialSerializer
    permission_classes = [permissions.IsAuthenticated]
    
def create(self, request, *args, **kwargs):      
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Course added successfully!",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CourseMaterialDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.CourseMaterial.objects.all()
    serializer_class = CourseMaterialSerializer
    permission_classes = [permissions.IsAuthenticated]
    
class ResultList(generics.ListCreateAPIView):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)
        
        
class ResultDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    permission_classes = [permissions.IsAuthenticated]
  
        
class NoticeList(generics.ListCreateAPIView):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
       
        if self.request.user.is_superuser:
            serializer.save(user=self.request.user)
        else:
            raise permissions.PermissionDenied("Only superusers can add notices.")
class CourseObjectivesList(generics.ListCreateAPIView):
    queryset = CourseObjectives.objects.all()
    serializer_class = CourseObjectivesSerializer
    permission_classes = [permissions.IsAuthenticated]

class CourseObjectivesDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CourseObjectives.objects.all()
    serializer_class = CourseObjectivesSerializer
    permission_classes = [permissions.IsAuthenticated]

class NoticeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        if self.request.user.is_superuser:
            serializer.save()
        else:
            raise permissions.PermissionDenied("Only superusers can update notices.")

    def perform_destroy(self, instance):
        if self.request.user.is_superuser:
            instance.delete()
        else:
            raise permissions.PermissionDenied("Only superusers can delete notices.")



# for testing uncomment it


# class TeacherList(generics.ListCreateAPIView):
#     queryset = models.Teacher.objects.all()
#     serializer_class = TeacherSerializer
    
    
# class TeacherDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = models.Teacher.objects.all()
#     serializer_class = TeacherSerializer
    
    
# class SemesterList(generics.ListCreateAPIView):    
#     queryset = models.Semester.objects.all()
#     serializer_class = SemesterSerializer       

    

# class SemesterDetail(generics.RetrieveUpdateDestroyAPIView):   
#     queryset = models.Semester.objects.all()
#     serializer_class = SemesterSerializer
    
    

# class StudentList(generics.ListCreateAPIView):
#     queryset = models.Student.objects.all()
#     serializer_class = StudentSerializer
  
    
# class StudentDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = models.Student.objects.all()
#     serializer_class = StudentSerializer
   
        
# class CourseList(generics.ListCreateAPIView):
#     queryset = Course.objects.all()
#     serializer_class = CourseSerializer
 

    

# class CourseDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Course.objects.all()
#     serializer_class = CourseSerializer
   
# class AssignmentList(generics.ListCreateAPIView):
#     queryset = Assignment.objects.all()
#     serializer_class = AssignmentSerializer
    
    

# class AssignmentDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Assignment.objects.all()
#     serializer_class = AssignmentSerializer
   
    
# class MaterialTypeList(generics.ListCreateAPIView):
#     queryset = models.MaterialType.objects.all()
#     serializer_class = MaterialTypeSerializer
    
    

# class MaterialTypeDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = models.MaterialType.objects.all()
#     serializer_class = MaterialTypeSerializer
   
# class CourseMaterialList(generics.ListCreateAPIView):
#     queryset = models.CourseMaterial.objects.all()
#     serializer_class = CourseMaterialSerializer
    
    

# class CourseMaterialDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = models.CourseMaterial.objects.all()
#     serializer_class = CourseMaterialSerializer
    
    
# class ResultList(generics.ListCreateAPIView):
#     queryset = Result.objects.all()
#     serializer_class = ResultSerializer
    
    
#     def perform_create(self, serializer):
#         serializer.save(uploaded_by=self.request.user)
        
        
# class ResultDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Result.objects.all()
#     serializer_class = ResultSerializer
   
  
        
# class NoticeList(generics.ListCreateAPIView):
#     queryset = Notice.objects.all()
#     serializer_class = NoticeSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def perform_create(self, serializer):
       
#         if self.request.user.is_superuser:
#             serializer.save(user=self.request.user)
#         else:
#             raise permissions.PermissionDenied("Only superusers can add notices.")
# class CourseObjectivesList(generics.ListCreateAPIView):
#     queryset = CourseObjectives.objects.all()
#     serializer_class = CourseObjectivesSerializer
    

# class CourseObjectivesDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = CourseObjectives.objects.all()
#     serializer_class = CourseObjectivesSerializer
    
# class NoticeDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Notice.objects.all()
#     serializer_class = NoticeSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def perform_update(self, serializer):
#         if self.request.user.is_superuser:
#             serializer.save()
#         else:
#             raise permissions.PermissionDenied("Only superusers can update notices.")

#     def perform_destroy(self, instance):
#         if self.request.user.is_superuser:
#             instance.delete()
#         else:
#             raise permissions.PermissionDenied("Only superusers can delete notices.")