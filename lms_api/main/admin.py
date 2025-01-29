from django.contrib import admin
from .models import Teacher, Semester, Course, Student, CourseNote  # Import your models

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
    list_display = ('se_name', 'batch', 'get_courses','start_date', 'end_date')
    search_fields = ('se_name', 'batch')
    list_filter = ('start_date', 'end_date')
    ordering = ('start_date',)  # Sort by start date

    def get_courses(self, obj):
        return ", ".join([course.title for course in obj.get_courses()])
    get_courses.short_description = 'Courses'

class CourseNoteInline(admin.TabularInline):
    model = CourseNote
    extra = 1  # Number of empty forms to display

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject_code', 'credits', 'semester', 'get_teacher_name')
    search_fields = ('title', 'subject_code')
    list_filter = ('semester', 'teacher')
    ordering = ('title',)  # Sort by title
    inlines = [CourseNoteInline]
    
    def get_teacher_name(self, obj):
        return obj.teacher.t_full_name if obj.teacher else 'No Teacher Assigned'
    get_teacher_name.short_description = 'Teacher'  # Column header in the admin panel


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    # list_display = ('st_name', 'st_email', 'st_contact', 'enrollment_date', 'semester')
    
    list_display = ('st_name', 'st_email', 'st_contact', 'enrollment_date', 'semester')
    search_fields = ('st_name', 'st_email')
    list_filter = ('enrollment_date', 'semester')
    ordering = ('st_name',)  # Sort by student name

@admin.register(CourseNote)
class CourseNoteAdmin(admin.ModelAdmin):
    list_display = ('course', 'get_teacher_name', 'get_course_batch', 'upload_date')
    search_fields = ('course__title', 'teacher__t_full_name')
    list_filter = ('upload_date', 'course', 'teacher')
    ordering = ('upload_date',)  # Sort by upload date


    # Custom method to display only the teacher's name
    def get_teacher_name(self, obj):
        return obj.teacher.t_full_name  # Assuming `t_full_name` stores the teacher's name
    get_teacher_name.short_description = 'Teacher'  # Column header in the admin panel
    
    def get_course_batch(self, obj):
        return obj.course.semester.batch
    get_course_batch.short_description = 'Batch'
