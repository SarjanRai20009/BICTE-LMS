from rest_framework import serializers
from .models import Teacher, Semester, Course, Student, CourseNote

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'

class SemesterSerializer(serializers.ModelSerializer):
    teachers = serializers.SerializerMethodField()
    students = serializers.SerializerMethodField()
    student_count = serializers.SerializerMethodField()

    class Meta:
        model = Semester
        fields = ['id', 'se_name', 'batch', 'start_date', 'end_date', 'teachers', 'students', 'student_count']

    def get_teachers(self, obj):
        return [teacher.t_full_name for teacher in obj.get_teachers()]

    def get_students(self, obj):
        return [student.st_name for student in obj.get_students()]

    def get_student_count(self, obj):
        return obj.get_students().count()

class StudentSerializer(serializers.ModelSerializer):
    # semester = SemesterSerializer(read_only=True)
    semester_name = serializers.SerializerMethodField()
    semester_batch = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ['id', 'st_exam_roll_no', 'st_reg_no', 'st_name', 'st_contact', 'enrollment_date', 'st_email', 'st_address', 'semester_name', 'semester_batch']
        # fields = ['id', 'st_exam_roll_no', 'st_reg_no', 'st_name', 'st_contact', 'enrollment_date', 'st_email', 'st_address', 'semester', 'semester_name', 'semester_batch']

    def get_semester_name(self, obj):
        return obj.semester.get_se_name_display()

    def get_semester_batch(self, obj):
        return obj.semester.batch