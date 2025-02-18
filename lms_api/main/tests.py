from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from .models import Teacher, Semester, Course, Student, CourseMaterial, Assignment, Quiz, Question, QuizAttempt, UserRank
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from .models import Student, Semester

from .views import StudentCourse


# In your app's tests.py file
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Teacher, Semester, Course, Student, MaterialType, CourseMaterial, Assignment
from .serializers import *
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.permissions import AllowAny
from django.test import TestCase, RequestFactory
from datetime import date
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth import get_user_model


from django.test import TestCase
from django.contrib.auth.hashers import make_password

from .models import *
from .views import *
from .urls import *







# class StudentViewTest(TestCase):
#     def setUp(self):
#         self.client = APIClient()
        
#         self.semester = Semester.objects.create(
#             se_name="EV",
#             batch="2023",
#             start_date="2023-01-01",
#             end_date="2023-06-30",
#             is_active=True
#         )
        
#         self.student = Student.objects.create(
#             profile_picture=SimpleUploadedFile("test_image.jpg", b"file_content"),
#             st_exam_roll_no="12345678",
#             st_reg_no="0-0-000-00-0000",
#             st_name="Jane Doe",
#             st_date_of_birth="2000-01-01",
#             st_address="123 Main St",
#             st_contact="9876543210",
#             enrollment_date=2023,
#             st_email="jane.doe@example.com",
#             st_password="student123",
#             st_gender="Female",
#             st_father_name="John Doe Sr.",
#             semester=self.semester
#         )

#     def test_student_list_view(self):
#         url = reverse('api-student-list')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(len(response.data), 1)

#     def test_student_detail_view(self):
#         url = reverse('api-student-detail', args=[self.student.id])
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.data['st_name'], "Jane Doe")

#     def test_student_creation(self):
#         url = reverse('api-student-list')
#         data = {           
#             'st_exam_roll_no': "87654321",
#             'st_reg_no': "0-0-000-00-0001",
#             'st_name': "John Doe",
#             'st_date_of_birth': "2001-01-01",
#             'st_address': "456 Elm St",
#             'st_contact': "1234567890",
#             'enrollment_date': 2023,
#             'st_email': "john.doe@example.com",
#             'st_password': "student456",
#             'st_gender': "Male",
#             'st_father_name': "John Doe Sr.",
#             'semester': self.semester.id
#         }
#         response = self.client.post(url, data, format='multipart')
#         print(response.data)  # Add this line to debug
#         self.assertEqual(response.status_code, 201)
#         self.assertEqual(Student.objects.count(), 2)

# class TeacherModelTest(TestCase):
#     def setUp(self):
#         self.teacher = Teacher.objects.create(
#             t_full_name="John Doe",
#             t_email="john.doe@example.com",
#             t_password="password123",
#             t_phone_number="1234567890",
#             t_address="123 Main St",
#             hire_date="2023-01-01",
#             designation="Professor"
#         )

#     def test_teacher_creation(self):
#         self.assertEqual(self.teacher.t_full_name, "John Doe")
#         self.assertEqual(self.teacher.t_email, "john.doe@example.com")
#         self.assertTrue(self.teacher.check_password("password123"))

#     def test_teacher_str_method(self):
#         self.assertEqual(str(self.teacher), "John Doe - john.doe@example.com - 1234567890")

#     def test_teacher_password_hashing(self):
#         self.assertNotEqual(self.teacher.t_password, "password123")
#         self.assertTrue(self.teacher.check_password("password123"))

#     def test_teacher_designation(self):
#         self.assertEqual(self.teacher.get_designation(), "Professor")

# class SemesterModelTest(TestCase):
#     def setUp(self):
#         self.semester = Semester.objects.create(
#             se_name="EV",
#             batch="2023",
#             start_date="2023-01-01",
#             end_date="2023-06-30"
#         )

#     def test_semester_creation(self):
#         self.assertEqual(self.semester.se_name, "EV")
#         self.assertEqual(self.semester.batch, "2023")
#         self.assertEqual(str(self.semester), "Everest (1st sem) - Batch 2023")





# class CourseModelTest(TestCase):
#     def setUp(self):
#         self.semester = Semester.objects.create(
#             se_name="EV",
#             batch="2023",
#             start_date="2023-01-01",
#             end_date="2023-06-30"
#         )
#         self.teacher = Teacher.objects.create(
#             t_full_name="John Doe",
#             t_email="john.doe@example.com",
#             t_password="password123",
#             t_phone_number="1234567890",
#             t_address="123 Main St",
#             hire_date="2023-01-01",
#             designation="Professor"
#         )
#         self.course = Course.objects.create(
#             subject_code="CS101",
#             title="Introduction to Computer Science",
#             description="Basic concepts of computer science.",
#             credits=3,
#             semester=self.semester,
#             teacher=self.teacher
#         )

#     def test_course_creation(self):
#         self.assertEqual(self.course.title, "Introduction to Computer Science")
#         self.assertEqual(self.course.credits, 3)
#         self.assertEqual(str(self.course), "Introduction to Computer Science (CS101)")

#     def test_course_teacher_assignment(self):
#         self.assertEqual(self.course.teacher.t_full_name, "John Doe")
#         self.assertEqual(self.course.teacher.t_email, "john.doe@example.com")

# class QuizModelTest(TestCase):
#     def setUp(self):
#         self.semester = Semester.objects.create(
#             se_name="EV",
#             batch="2023",
#             start_date="2023-01-01",
#             end_date="2023-06-30"
#         )
#         self.teacher = Teacher.objects.create(
#             t_full_name="John Doe",
#             t_email="john.doe@example.com",
#             t_password="password123",
#             t_phone_number="1234567890",
#             t_address="123 Main St",
#             hire_date="2023-01-01",
#             designation="Professor"
#         )
#         self.course = Course.objects.create(
#             subject_code="CS101",
#             title="Introduction to Computer Science",
#             description="Basic concepts of computer science.",
#             credits=3,
#             semester=self.semester,
#             teacher=self.teacher
#         )
#         self.quiz = Quiz.objects.create(
#             title="Midterm Quiz",
#             description="Quiz covering the first half of the course.",
#             course=self.course,
#             teacher=self.teacher
#         )

#     def test_quiz_creation(self):
#         self.assertEqual(self.quiz.title, "Midterm Quiz")
#         self.assertEqual(self.quiz.course.title, "Introduction to Computer Science")
#         self.assertEqual(str(self.quiz), "Midterm Quiz - Introduction to Computer Science")
        
        
        
# # above testcase not ok
        
# # template testing

# class TemplateRenderingTest(TestCase):
#     def setUp(self):
#         self.client = Client()

#     def test_index_template_rendering(self):
       
#         response = self.client.get(reverse('news')) 
#         self.assertEqual(response.status_code, 200) 
#         self.assertTemplateUsed(response, 'frontends/news.html')
        
# # static file testing
# class StaticFilesTest(StaticLiveServerTestCase):
#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         cls.selenium = WebDriver()
#         cls.selenium.implicitly_wait(10)

#     @classmethod
#     def tearDownClass(cls):
#         cls.selenium.quit()
#         super().tearDownClass()
#     def test_static_files(self):
#         self.selenium.get(f"{self.live_server_url}{reverse('base')}")

      
#         logo = self.selenium.find_element(By.CSS_SELECTOR, "img[alt='Logo']")

        
#         assert "images/main_logo_light.png" in logo.get_attribute("src")


# # above testcase ok
        

# class SignInTestCase(TestCase):
    
#     def setUp(self):
#         # Create user for testing
#         self.teacher_email = "teacher@example.com"
#         self.teacher_password = "securepassword"
#         self.student_email = "student@example.com"
#         self.student_password = "studentpass"

#         self.teacher = Teacher.objects.create(
#             t_full_name="John Doe",
#             t_email=self.teacher_email,
#             t_password=make_password(self.teacher_password),
#             t_phone_number="9876543210",
#             t_address="Some Address",
#             hire_date="2020-01-01"
#         )

#         self.semester = Semester.objects.create(
#             id=1,
#             se_name="EV",
#             batch="Batch A",
#             start_date="2025-01-01",
#             end_date="2025-06-01",
#             is_active=True
#         )

#         self.student = Student.objects.create(
#             st_name="Jane Doe",
#             st_email=self.student_email,
#             st_password=make_password(self.student_password),
#             st_contact="1234567890",
#             st_address="Another Address",
#             semester=self.semester
#         )

#         self.client = Client()     
                
#     def test_teacher_signin_valid(self):
#         response = self.client.post(reverse('signin'), {
#             'username': self.teacher_email,
#             'password': self.teacher_password,
#             'remember_me': 'on',
#         })
#         print(response.content)
#         self.assertEqual(response.status_code, 200)  
        
#     def test_student_signin_valid(self):
#         response = self.client.post(reverse('signin'), {
#                 'username': self.student_email,
#                 'password': self.student_password,
#                 'remember_me': 'on',
#         })
            
#         print(response.content)
#         self.assertEqual(response.status_code, 200)
        
        
#     def test_teacher_signin_invalid_password(self):
#         response = self.client.post(reverse('signin'), {
#             'username': self.teacher_email,
#             'password': "wrongpassword",
#             'remember_me': 'on',
#         })
#         self.assertEqual(response.status_code, 200)
      
#         self.assertContains(response, 'Invalid login credentials. Please try again!')
     


# #above test ok



