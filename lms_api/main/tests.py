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
from datetime import timedelta

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
        
        
        
# # above testcase is ok
        
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


# Integrate testing

# class StudentCourseMaterialIntegrationTest(TestCase):
#     def setUp(self):
#         # Create a semester
#         self.semester = Semester.objects.create(
#             se_name="EV",
#             batch="2023",
#             start_date=date(2023, 1, 1),
#             end_date=date(2023, 6, 30),
#             is_active=True
#         )

#         # Create a teacher
#         self.teacher = Teacher.objects.create(
#             t_full_name="John Doe",
#             t_email="john.doe@example.com",
#             t_password="password123",
#             t_phone_number="1234567890",
#             t_address="123 Main St",
#             hire_date="2023-01-01",
#             designation="Professor"
#         )

#         # Create a course
#         self.course = Course.objects.create(
#             subject_code="CS101",
#             title="Introduction to Computer Science",
#             description="Basic concepts of computer science.",
#             credits=3,
#             semester=self.semester,
#             teacher=self.teacher
#         )

#         # Create students
#         self.student1 = Student.objects.create(
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

#         self.student2 = Student.objects.create(
#             st_exam_roll_no="87654321",
#             st_reg_no="0-0-000-00-0001",
#             st_name="John Doe",
#             st_date_of_birth="2000-02-01",
#             st_address="456 Main St",
#             st_contact="1234567890",
#             enrollment_date=2023,
#             st_email="john.doe@example.com",
#             st_password="student123",
#             st_gender="Male",
#             st_father_name="John Doe Jr.",
#             semester=self.semester
#         )

#         # Create a course material
#         self.course_material = CourseMaterial.objects.create(
#             title="Lecture 1 Notes",
#             description="Introduction to Programming",
#             file=SimpleUploadedFile("lecture1.pdf", b"file_content"),
#             material_type=MaterialType.objects.create(name="PDF", icon_class="bi-file-earmark-pdf"),
#             course=self.course,
#             teacher=self.teacher
#         )

#     def test_student_assigned_to_semester(self):
#         self.assertEqual(self.student1.semester, self.semester)
#         self.assertEqual(self.student2.semester, self.semester)

#     def test_course_material_association(self):
#         self.assertEqual(self.course_material.course, self.course)

#     def test_course_material_teacher_association(self):
#         self.assertEqual(self.course_material.teacher, self.teacher)
    
#     def test_multiple_students_in_same_semester(self):       
#         self.assertEqual(self.student1.semester, self.semester)
#         self.assertEqual(self.student2.semester, self.semester)

       
#         students_in_semester = Student.objects.filter(semester=self.semester)
#         self.assertEqual(students_in_semester.count(), 2)
        
        
# # above test is ok


# class TeacherCourseIntegrationTest(TestCase):
#     def setUp(self):
#         self.semester = Semester.objects.create(
#             se_name="EV",
#             batch="2023",
#             start_date=date(2023, 1, 1),
#             end_date=date(2023, 6, 30),
#             is_active=True
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
#     def test_teacher_assigned_to_course(self):
#         self.assertEqual(self.course.teacher, self.teacher)
#     def test_course_assigned_to_semester(self):
#         self.assertEqual(self.course.semester, self.semester)
        
        
# # above test ok

# class StudentAssignmentIntegrationTest(TestCase):
#     def setUp(self):
#         self.semester = Semester.objects.create(
#             se_name="EV",
#             batch="2023",
#             start_date=date(2023, 1, 1),
#             end_date=date(2023, 6, 30),
#             is_active=True
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

#         self.student = Student.objects.create(
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

#         self.assignment = Assignment.objects.create(
#             title="Assignment 1",
#             description="Complete the exercises.",
#             deadline=timezone.now() + timedelta(days=7),
#             course=self.course,
#             teacher=self.teacher
#         )

#         self.assignment_submission = AssignmentSubmit.objects.create(
#             student=self.student,
#             assignment=self.assignment,
#             assignment_file=SimpleUploadedFile("assignment1.pdf", b"file_content")
#         )

#     def test_student_submitted_assignment(self):
#         self.assertEqual(self.assignment_submission.student, self.student)
#         self.assertEqual(self.assignment_submission.assignment, self.assignment)

# #above test ok

# class CourseMaterialIntegrationTest(TestCase):
#     def setUp(self):
#         self.semester = Semester.objects.create(
#             se_name="EV",
#             batch="2023",
#             start_date=date(2023, 1, 1),
#             end_date=date(2023, 6, 30),
#             is_active=True
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

#         self.course_material = CourseMaterial.objects.create(
#             title="Lecture 1 Notes",
#             description="Introduction to Programming",
#             file=SimpleUploadedFile("lecture1.pdf", b"file_content"),
#             material_type=MaterialType.objects.create(name="PDF", icon_class="bi-file-earmark-pdf"),
#             course=self.course,
#             teacher=self.teacher
#         )

#     def test_course_material_association(self):
#         self.assertEqual(self.course_material.course, self.course)
#         self.assertEqual(self.course_material.teacher, self.teacher)

#     def test_course_material_is_accessible(self):
#         self.assertTrue(self.course_material.is_accessible())
        
        
# #above test ok

# class QuizStudentIntegrationTest(TestCase):
#     def setUp(self):
#         self.semester = Semester.objects.create(
#             se_name="EV",
#             batch="2023",
#             start_date=date(2023, 1, 1),
#             end_date=date(2023, 6, 30),
#             is_active=True
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

#         self.student = Student.objects.create(
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

#         self.quiz = Quiz.objects.create(
#             title="Quiz 1",
#             description="Test your knowledge.",
#             course=self.course,
#             teacher=self.teacher
#         )

#         self.question = Question.objects.create(
#             quiz=self.quiz,
#             text="What is 2 + 2?",
#             option1="3",
#             option2="4",
#             option3="5",
#             option4="6",
#             correct_option="2",
#             marks=1
#         )

#         self.quiz_attempt = QuizAttempt.objects.create(
#             student=self.student,
#             quiz=self.quiz,
#             score=1
#         )
#     def test_student_attempted_quiz(self):
#         self.assertEqual(self.quiz_attempt.student, self.student)
#         self.assertEqual(self.quiz_attempt.quiz, self.quiz)
#         self.assertEqual(self.quiz_attempt.score, 1)
        
# #above test ok

# class SemesterStudentIntegrationTest(TestCase):
#     def setUp(self):
#         self.semester = Semester.objects.create(
#             se_name="EV",
#             batch="2023",
#             start_date=date(2023, 1, 1),
#             end_date=date(2023, 6, 30),
#             is_active=True
#         )

#         self.student1 = Student.objects.create(
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

#         self.student2 = Student.objects.create(
#             st_exam_roll_no="87654321",
#             st_reg_no="0-0-000-00-0001",
#             st_name="John Doe",
#             st_date_of_birth="2000-02-01",
#             st_address="456 Main St",
#             st_contact="1234567890",
#             enrollment_date=2023,
#             st_email="john.doe@example.com",
#             st_password="student123",
#             st_gender="Male",
#             st_father_name="John Doe Jr.",
#             semester=self.semester
#         )

#     def test_students_assigned_to_semester(self):
#         students_in_semester = Student.objects.filter(semester=self.semester)
#         self.assertEqual(students_in_semester.count(), 2)
#         self.assertIn(self.student1, students_in_semester)
#         self.assertIn(self.student2, students_in_semester)
        
        
# #above test ok


# class LeaderboardIntegrationTest(TestCase):
#     def setUp(self):
#         # Create a semester
#         self.semester = Semester.objects.create(
#             se_name="EV",
#             batch="2023",
#             start_date=date(2023, 1, 1),
#             end_date=date(2023, 6, 30),
#             is_active=True
#         )

#         # Create a teacher
#         self.teacher = Teacher.objects.create(
#             t_full_name="John Doe",
#             t_email="john.doe@example.com",
#             t_password="password123",
#             t_phone_number="1234567890",
#             t_address="123 Main St",
#             hire_date="2023-01-01",
#             designation="Professor"
#         )

#         # Create a course
#         self.course = Course.objects.create(
#             subject_code="CS101",
#             title="Introduction to Computer Science",
#             description="Basic concepts of computer science.",
#             credits=3,
#             semester=self.semester,
#             teacher=self.teacher  # Assign the teacher to the course
#         )

#         # Create a student
#         self.student = Student.objects.create(
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

#         # Create a quiz
#         self.quiz = Quiz.objects.create(
#             title="Quiz 1",
#             description="Test your knowledge.",
#             course=self.course,
#             teacher=self.teacher  # Assign the teacher to the quiz
#         )

#         # Create a quiz attempt
#         self.quiz_attempt = QuizAttempt.objects.create(
#             student=self.student,
#             quiz=self.quiz,
#             score=10
#         )

#     def test_leaderboard_update(self):
#         # Update the leaderboard
#         update_leaderboard()

#         # Check if the leaderboard was updated correctly
#         user_rank = UserRank.objects.get(student=self.student)
#         self.assertEqual(user_rank.total_score, 10)
#         self.assertEqual(user_rank.rank, 1)
        
# #above test ok