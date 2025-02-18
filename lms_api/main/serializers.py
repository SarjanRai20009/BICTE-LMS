# from rest_framework import serializers
# from .models import Teacher, Semester, Course, Student, MaterialType, CourseMaterial

# class TeacherSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Teacher
#         fields = '__all__'

# class SemesterSerializer(serializers.ModelSerializer):
#     teachers = serializers.SerializerMethodField()
#     students = serializers.SerializerMethodField()
#     student_count = serializers.SerializerMethodField()

#     class Meta:
#         model = Semester
#         fields = ['id', 'se_name', 'batch', 'start_date', 'end_date', 'teachers', 'students', 'student_count']

#     def get_teachers(self, obj):
#         return [teacher.t_full_name for teacher in obj.get_teachers()]

#     def get_students(self, obj):
#         return [student.st_name for student in obj.get_students()]

#     def get_student_count(self, obj):
#         return obj.get_students().count()

# class StudentSerializer(serializers.ModelSerializer):
#     semester_name = serializers.SerializerMethodField()
#     semester_batch = serializers.SerializerMethodField()

#     class Meta:
#         model = Student
#         fields = ['id', 'st_exam_roll_no', 'st_reg_no', 'st_name', 'st_contact', 'enrollment_date', 'st_email', 'st_address', 'semester_name', 'semester_batch']

#     def get_semester_name(self, obj):
#         return obj.semester.get_se_name_display()

#     def get_semester_batch(self, obj):
#         return obj.semester.batch

# class MaterialTypeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = MaterialType
#         fields = '__all__'

# class CourseMaterialSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CourseMaterial
#         fields = '__all__'


from rest_framework import serializers
from .models import *
from .models import Teacher, Semester, Course, Student, MaterialType, CourseMaterial
from django.contrib.auth.models import User



class TeacherSerializer(serializers.ModelSerializer):
    courses_taught = serializers.SerializerMethodField()  # For courses taught by the teacher
    course_count = serializers.SerializerMethodField()  # For counting how many courses the teacher teaches
    semester_details = serializers.SerializerMethodField()  # For getting the semester details for each course
    full_name_and_email = serializers.SerializerMethodField()  # A custom field combining full name and email
    
    class Meta:
        model = Teacher
        fields = ['id', 'profile_picture', 't_full_name', 't_phone_number', 't_address', 't_email', 't_password', 'hire_date', 'designation', 
                  'courses_taught', 'course_count', 'semester_details', 'full_name_and_email']

    # SerializerMethodField to get courses taught by the teacher
    def get_courses_taught(self, obj):
        courses = obj.course_set.all()  # Getting all courses associated with the teacher
        return [course.title for course in courses]  # Returning course titles as a list

    # SerializerMethodField to get the count of courses taught by the teacher
    def get_course_count(self, obj):
        return obj.course_set.count()  # Returning the count of courses

    # SerializerMethodField to return details of semesters for each course the teacher teaches
    def get_semester_details(self, obj):
        courses = obj.course_set.all()
        semester_details = []
        for course in courses:
            semester_details.append({
                "course_title": course.title,
                "semester_name": course.semester.get_se_name_display(),
                "semester_batch": course.semester.batch
            })
        return semester_details

    # Custom field that combines the full name and email into a single string
    def get_full_name_and_email(self, obj):
        return f"{obj.t_full_name} ({obj.t_email})"

    # Optional: Validation to check the phone number format
    def validate_t_phone_number(self, value):
        # Ensure the phone number follows a particular pattern
        if not value.isdigit() or len(value) < 10:
            raise serializers.ValidationError("Phone number should be numeric and at least 10 digits long.")
        return value

class SemesterSerializer(serializers.ModelSerializer):
    teachers = serializers.SerializerMethodField()
    students = serializers.SerializerMethodField()
    student_count = serializers.SerializerMethodField()

    class Meta:
        model = Semester
        fields = ['id', 'se_name', 'batch', 'start_date', 'end_date', 'is_active', 'teachers', 'students', 'student_count']

    def get_teachers(self, obj):
        return [teacher.t_full_name for teacher in obj.get_teachers()]

    def get_students(self, obj):
        return [student.st_name for student in obj.get_students()]

    def get_student_count(self, obj):
        return obj.get_students().count()

class StudentSerializer(serializers.ModelSerializer):
    semester = serializers.PrimaryKeyRelatedField(queryset=Semester.objects.all())  # This allows selecting a Semester by ID
    semester_name = serializers.SerializerMethodField()
    semester_batch = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ['id', 'profile_picture', 'st_exam_roll_no', 'st_reg_no', 'st_name', 'st_date_of_birth','st_address', 'st_contact', 'enrollment_date', 'st_email', 'st_password',  'st_gender', 'st_father_name', 'semester', 'semester_name', 'semester_batch']

    def get_semester_name(self, obj):
        return obj.semester.get_se_name_display()

    def get_semester_batch(self, obj):
        return obj.semester.batch
    
    
class CourseSerializer(serializers.ModelSerializer):
    teacher_info = serializers.SerializerMethodField()
    semester_details = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id','syllabus_file' ,'subject_code', 'title', 'description', 'credits', 'is_elective', 'semester', 'teacher', 'teacher_info', 'semester_details']

    def get_teacher_info(self, obj):
        return {
            "teacher_name": obj.teacher.t_full_name if obj.teacher else "Not Assigned",
            "teacher_email": obj.teacher.t_email if obj.teacher else "Not Assigned",
        }

    def get_semester_details(self, obj):
        return {
            "semester_name": obj.semester.get_se_name_display(),
            "semester_batch": obj.semester.batch
        }
class CourseObjectivesSerializer(serializers.ModelSerializer):    
    class Meta:
        model = CourseObjectives
        fields = ['id', 'course', 'objective']
        read_only_fields = ['created_at', 'updated_at']
class AssignmentSerializer(serializers.ModelSerializer):
    course_title = serializers.SerializerMethodField()
    teacher_info = serializers.SerializerMethodField()

    class Meta:
        model = Assignment
        fields = ['id', 'title', 'description', 'file', 'deadline', 'posted_date', 'course', 'teacher', 'course_title', 'teacher_info']

    def get_course_title(self, obj):
        return obj.course.title

    def get_teacher_info(self, obj):
        return {
            "teacher_name": obj.teacher.t_full_name,
            "teacher_email": obj.teacher.t_email,
            "designation": obj.teacher.designation,
        }

    def validate(self, data):
        if not data.get('title'):
            raise serializers.ValidationError("Title is required.")
        if not data.get('course'):
            raise serializers.ValidationError("Course is required.")
        return data
class AssignmentSubmitSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignmentSubmit
        fields = ['id', 'student', 'assignment', 'submit_date', 'assignment_file']
    def validate_assignment(self, value):
       
        if value.due_date < now():
            raise serializers.ValidationError("You cannot submit an assignment past its due date.")
        return value

    def validate(self, data):
       
        user = self.context['request'].user
        assignment = data.get('assignment')

        if AssignmentSubmit.objects.filter(student=user, assignment=assignment).exists():
            raise serializers.ValidationError("You have already submitted this assignment.")

        return data
class MaterialTypeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MaterialType
        fields = '__all__'

class CourseMaterialSerializer(serializers.ModelSerializer):
    teacher_info = serializers.SerializerMethodField()

    class Meta:
        model = CourseMaterial
        fields = '__all__'

    def get_teacher_info(self, obj):
        return {
            "name": obj.teacher.t_full_name,
            "email": obj.teacher.t_email,
            "designation": obj.teacher.designation,
        }

    def validate(self, data):
        if not data.get('title'):
            raise serializers.ValidationError("Title is required.")
        if not data.get('course'):
            raise serializers.ValidationError("Course is required.")
        return data

class ResultSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  # Display the username of the uploader
    semester = serializers.PrimaryKeyRelatedField(queryset=Semester.objects.all())  # Allow selection of semester by ID

    class Meta:
        model = Result
        fields = ['id', 'title', 'file', 'description', 'user', 'uploaded_at', 'semester']
        read_only_fields = ['uploaded_at',] 
    
class NoticeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  

    class Meta:
        model = Notice
        fields = ['id', 'title', 'description', 'link', 'notic_file', 'timestamp', 'user']
        extra_kwargs = {
            'link': {'required': False, 'allow_null': True}  # Make 'link' optional
        }
