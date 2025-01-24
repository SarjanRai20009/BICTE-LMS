from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework import generics

from rest_framework import permissions

from rest_framework.response import Response
from rest_framework import status

# Explicit import
from .serializers import Teacherserializer, SemesterSerializer

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

class TeacherList(generics.ListCreateAPIView):
    queryset = models.Teacher.objects.all()
    serializer_class = Teacherserializer
    permission_classes = [permissions.IsAuthenticated]
    
class TeacherDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Teacher.objects.all()
    serializer_class = Teacherserializer
    permission_classes = [permissions.IsAuthenticated]

class SemesterList(APIView):
    def get(self, request):
        semesters = models.Semester.objects.all()
        serializer = SemesterSerializer(semesters, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


