from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User


from rest_framework.views import APIView
from rest_framework import generics
from django.views.generic import TemplateView

from rest_framework import permissions

from rest_framework.response import Response
from rest_framework import status

# Explicit import
# from .serializers import TeacherSerializer, SemesterSerializer
from .serializers import *

# from .models import Teacher
from . import models

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
class IndexView(TemplateView):
    template_name = 'base_template/base.html'

class TeacherList(generics.ListCreateAPIView):
    queryset = models.Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [permissions.IsAuthenticated]
    
class TeacherDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    

class SemesterList(generics.ListCreateAPIView):    
    queryset = models.Semester.objects.all()
    serializer_class = SemesterSerializer       

class SemesterDetail(generics.RetrieveUpdateDestroyAPIView):   
    queryset = models.Semester.objects.all()
    serializer_class = SemesterSerializer
    

class StudentList(generics.ListCreateAPIView):
    queryset = models.Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
class StudentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]