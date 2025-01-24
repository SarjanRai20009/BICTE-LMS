from django.contrib import admin
from .models import Teacher, Semester, Course, Student  # Import your models

# Register your models here.
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('t_full_name', 't_email', 't_phone_number', 'hire_date')
    search_fields = ('t_full_name', 't_email')
    list_filter = ('hire_date', 'designation')
    # list_filter = ('hire_date', 'qualification')
    ordering = ('t_full_name',)  # Sort by full name

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('se_name', 'batch', 'start_date', 'end_date')
    search_fields = ('se_name', 'batch')
    list_filter = ('start_date', 'end_date')
    ordering = ('start_date',)  # Sort by start date

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject_code', 'credits', 'semester', 'teacher')
    search_fields = ('title', 'subject_code')
    list_filter = ('semester', 'teacher')
    ordering = ('title',)  # Sort by title

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('st_name', 'st_email', 'st_contact', 'enrollment_date', 'semester')
    search_fields = ('st_name', 'st_email')
    list_filter = ('enrollment_date', 'semester')
    ordering = ('st_name',)  # Sort by student name
