
from django.contrib import admin
from django import forms 
from .models import Teacher, Semester, Course, Student, MaterialType, CourseMaterial
from .models import Quiz, Question, QuizAttempt, UserRank

from .models import *
# Custom form for CourseMaterial to add any specific validation if needed
class CourseMaterialForm(forms.ModelForm):
    class Meta:
        model = CourseMaterial
        fields = '__all__'  

    def clean(self):
        cleaned_data = super().clean()
        # Add any custom validation logic here if needed
        return cleaned_data

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('t_full_name', 't_email', 't_phone_number', 'hire_date')
    search_fields = ('t_full_name', 't_email')
    list_filter = ('hire_date', 'designation')  # 'designation' is a valid field
    ordering = ('t_full_name',) # Sort by full name

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('se_name', 'batch', 'get_courses', 'start_date', 'end_date')
    search_fields = ('se_name', 'batch')
    list_filter = ('start_date', 'end_date')
    ordering = ('start_date',)  

    def get_courses(self, obj):
        return ", ".join([course.title for course in obj.get_courses()])
    get_courses.short_description = 'Courses'



@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject_code', 'credits', 'is_elective',  'semester', 'get_teacher_name')
    search_fields = ('title', 'subject_code')
    list_filter = ('semester', 'teacher')
    ordering = ('title',)  # Sort by title
    
    def get_teacher_name(self, obj):
        return obj.teacher.t_full_name if obj.teacher else 'No Teacher Assigned'
    get_teacher_name.short_description = 'Teacher'  # Column header in the admin panel
    
    
@admin.register(CourseObjectives)
class CourseObjectivesAdmin(admin.ModelAdmin):
    list_display = ['course', 'objective']
    list_filter = ['course']
    search_fields = ['course__title', 'objective']

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('st_name', 'st_email', 'st_contact', 'enrollment_date', 'semester', 'st_gender', 'st_father_name', 'st_date_of_birth')
    search_fields = ('st_name', 'st_email', 'st_contact')
    list_filter = ('enrollment_date', 'semester', 'st_gender')
    ordering = ('st_name',)
    # fields = ('st_exam_roll_no', 'st_reg_no', 'st_name', 'st_address', 'st_contact', 'enrollment_date', 'st_email', 'st_password', 'st_gender', 'st_father_name', 'st_date_of_birth', 'semester')

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
   
    list_display = ('title', 'author')

   
    search_fields = ('title', 'author')

    
    list_filter = ('author',)

    
    ordering = ['author', 'title']

@admin.register(MaterialType)
class MaterialTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon_class')
    search_fields = ('name',)
    ordering = ('name',) 

@admin.register(CourseMaterial)
class CourseMaterialAdmin(admin.ModelAdmin):
    form = CourseMaterialForm  # Use the custom form

    list_display = ('title', 'material_type', 'course', 'get_teacher_name', 'upload_date')
    search_fields = ('title', 'course__title', 'teacher__t_full_name')
    list_filter = ('material_type', 'course', 'teacher', 'upload_date')
    ordering = ('upload_date',)  # Sort by upload date

    def get_teacher_name(self, obj):
        return obj.teacher.t_full_name if obj.teacher else 'No Teacher Assigned'
    get_teacher_name.short_description = 'Teacher'  # Column header in the admin panel

    readonly_fields = ('upload_date', 'updated_at')  # Use readonly fields for these dates

    fieldsets = (
        (None, {
            'fields': ('title', 'material_type', 'course', 'teacher', 'description', 'file', 'external_link')
        }),
        ('Dates', {
            'fields': ('upload_date', 'updated_at'),
            'classes': ('collapse',),  # Optional: make this section collapsible
        }),
    )

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'teacher', 'deadline', 'posted_date', 'is_due')
    list_filter = ('course', 'teacher', 'deadline')
    search_fields = ('title', 'description', 'course__title', 'teacher__t_full_name')
    ordering = ('-posted_date',)
    readonly_fields = ('posted_date',)
    
@admin.register(AssignmentSubmit)
class AssignmentSubmitAdmin(admin.ModelAdmin):
    list_display = ('student', 'assignment', 'submit_date')
    search_fields = ('student__username', 'assignment__title')
    list_filter = ('submit_date',)
    
@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ['title', 'uploaded_at', 'user', 'semester']
    list_filter = ['uploaded_at', 'semester']
    search_fields = ['title', 'description']
    readonly_fields = ['uploaded_at']  

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
   
    
@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'timestamp', 'user') 
    search_fields = ('title', 'description')
    readonly_fields = ('timestamp',)

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'teacher', 'is_active', 'created_at', 'updated_at')
    search_fields = ('title', 'course__title', 'teacher__t_full_name')
    list_filter = ('is_active', 'course', 'teacher')
    ordering = ('-created_at',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'quiz', 'marks', 'correct_option')
    search_fields = ('text', 'quiz__title')
    list_filter = ('quiz',)
    ordering = ('quiz',)

@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('student', 'quiz', 'score', 'attempted_at')
    search_fields = ('student__st_name', 'quiz__title')
    list_filter = ('quiz', 'student')
    ordering = ('-attempted_at',)

@admin.register(UserRank)
class UserRankAdmin(admin.ModelAdmin):
    list_display = ('student', 'rank', 'total_score')
    search_fields = ('student__st_name',)
    ordering = ('rank',)