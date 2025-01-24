from rest_framework import serializers
from . import models

class Teacherserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Teacher
        fields = '__all__' 
class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Semester
        fields = ['se_name', 'batch', 'start_date', 'end_date']