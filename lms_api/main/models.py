from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MaxValueValidator, MinValueValidator

from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password


# Create your models here.

class Teacher(models.Model):
    # profile_picture = models.ImageField(upload_to='teacher_pics/', null=True, blank=True)  # Profile picture
   
    t_full_name = models.CharField(max_length=50)
    t_phone_number = models.CharField(max_length=40)
    t_address = models.CharField(max_length=100)
    
    t_email = models.EmailField(max_length=100, unique=True)
    t_password = models.CharField(max_length=255) 
    
    hire_date = models.DateField()
    designation = models.CharField(max_length=100, default='Lecturer')
    
    # courses = models.ManyToManyField("Course", related_name="teachers")
    
    def save(self, *args, **kwargs):
        """Hashes password only if it's a new password or changed"""
        if self.pk:  # Check if instance exists (i.e., if it's an update)
            original = Teacher.objects.get(pk=self.pk)
            if original.t_password != self.t_password:
                self.t_password = make_password(self.t_password)  # Hash the new password if it’s changed
        else:  # New user
            self.t_password = make_password(self.t_password)  # Hash the password for a new user

        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        """Checks if the entered password matches the stored hashed password"""
        return check_password(raw_password, self.t_password)

    def __str__(self):
        return f"{self.t_full_name} - {self.t_email} - {self.t_phone_number}"
    

    class Meta:
        verbose_name = "Teacher"
        verbose_name_plural = "Teachers"
    
    def get_designation(self):
        return self.designation


        
class Semester(models.Model):
    EVEREST = "EV"
    ANNAPURNA = "AN"
    KANCHENJUNGA = "KA"
    MANASLU = "MA"
    LHOTSE = "LH"
    MAKALU = "MK"
    DHAULAGIRI = "DH"
    LANGTANG = "LA"

    SEMESTER_CHOICES = [
        (EVEREST, "Everest (1st sem)"),
        (ANNAPURNA, "Annapurna (2nd sem)"),
        (KANCHENJUNGA, "Kanchenjunga (3rd sem)"),
        (MANASLU, "Manaslu (4th sem)"),
        (LHOTSE, "Lhotse (5th sem)"),
        (MAKALU, "Makalu (6th sem)"),
        (DHAULAGIRI, "Dhaulagiri (7th sem)"),
        (LANGTANG, "Langtang (8th sem)"),
    ]

    se_name = models.CharField(max_length=2, choices=SEMESTER_CHOICES, default=EVEREST)
    batch = models.CharField(max_length=20)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)  
    is_active = models.BooleanField(default=True, verbose_name="Is Active")

    def clean(self):
        
        if self.end_date and self.end_date < self.start_date:
            raise ValidationError("End date must be after start date.")

    def save(self, *args, **kwargs):
        self.clean()  
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_se_name_display()} - Batch {self.batch}"

    class Meta:
        verbose_name = "Semester"
        verbose_name_plural = "Semesters"

    def get_courses(self):
        return self.course_set.all()

    def get_teachers(self):
        return Teacher.objects.filter(course__semester=self).distinct()

    def get_students(self):
        return self.student_set.all()


class Course(models.Model):    
    subject_code = models.CharField(max_length=20)
    title = models.CharField(max_length=50)
    description = models.TextField()
    credits = models.IntegerField()
    
    is_elective = models.BooleanField(default=False, blank=True, null=True)

    # syllabus_file = models.FileField(upload_to='syllabus_files/', null=True, blank=True)  # Syllabus file

    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"{self.title} ({self.subject_code})"

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"
        
    def get_course_teacher(self):
        return self.teacher.t_full_name if self.teacher else "Not Assigned"
    
class Student(models.Model):
    # profile_picture = models.ImageField(upload_to='student_pics/', null=True, blank=True)  # Profile picture
    st_exam_roll_no = models.CharField(max_length=8, default='00000000')  # Use CharField with fixed length and default value
    st_reg_no = models.CharField(max_length=40, default='0-0-000-00-0000')  # Provide a default value
    
    st_name = models.CharField(max_length=100)
    st_date_of_birth = models.DateField(null=True, blank=True)
    st_address = models.CharField(max_length=255)
    st_contact = models.CharField(max_length=15)
    enrollment_date = models.IntegerField()  
    
    st_email = models.EmailField(unique=True)
    st_password = models.CharField(max_length=128, default='studentSMC1')  # Add default password
    
    st_gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], null=True, blank=True)
    st_father_name = models.CharField(max_length=100, null=True, blank=True)
    
    
       

    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)   
    
    
    
    def save(self, *args, **kwargs):
        """Hashes password only if it's a new password or changed"""
        if self.pk:  # Check if instance exists (i.e., if it's an update)
            original = Student.objects.get(pk=self.pk)
            if original.st_password != self.st_password:
                self.st_password = make_password(self.st_password)  # Hash the new password if it's changed
        else:  # New user
            self.st_password = make_password(self.st_password)  # Hash the password for a new user

        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        """Checks if the entered password matches the stored hashed password"""
        return check_password(raw_password, self.st_password)
    
    def __str__(self):
        return f"{self.st_name} - {self.st_email} - {self.st_contact}" 
    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"
        
    def get_student_info(self):
        return f"Roll No: {self.st_exam_roll_no}, Reg No: {self.st_reg_no}, Semester: {self.semester.se_name}"

        


class MaterialType(models.Model):
    MATERIAL_CHOICES = [
        ('BOOK', 'Book', 'bi-book'), 
        ('DOCX', 'Docx', 'bi-file-earmark-text'),
        ('VIDEO', 'Video', 'bi-camera-video'),  
        ('AUDIO', 'Audio', 'bi-music-note'),  
        ('PDF', 'PDF', 'bi-file-earmark-pdf'),  
        ('SLIDES', 'Slides', 'bi-file-earmark-slides'),  
        ('QUIZ', 'Quiz', 'bi-question-circle'),  
        ('ASSIGNMENT', 'Assignment', 'bi-pencil-square'),  
        ('IMAGE', 'Image', 'bi-file-image'),  
        ('LINK', 'Link', 'bi-link'),  
        ('PPTX', 'PPTX', 'bi-file-earmark-powerpoint'),  
        ('PPT', 'PPT', 'bi-file-earmark-ppt'),  
        ('XLS', 'XLS', 'bi-file-earmark-excel'), 
        ('XLSX', 'XLSX', 'bi-file-earmark-excel'),  
        ('ZIP', 'ZIP', 'bi-file-earmark-zip'),  
    ]

    name = models.CharField(max_length=20, choices=[(item[0], item[1]) for item in MATERIAL_CHOICES], default='PDF', verbose_name="Material Type")
    icon_class = models.CharField(max_length=50, choices=[(item[0], item[2]) for item in MATERIAL_CHOICES], default='bi-file-earmark-pdf', verbose_name="Icon Class")

    def __str__(self):
        return self.get_name_display()

    class Meta:
        verbose_name = "Material Type"
        verbose_name_plural = "Material Types"
        
        
class CourseMaterial(models.Model):
    title = models.CharField(max_length=255, verbose_name="Material Title")
    file = models.FileField(upload_to="course_materials/", blank=True, null=True, verbose_name="Material File")
    external_link = models.URLField(blank=True, null=True, verbose_name="External Link")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    upload_date = models.DateField(auto_now_add=True, verbose_name="Upload Date")
    updated_at = models.DateField(auto_now=True, verbose_name="Last Updated")
    
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    
    material_type = models.ForeignKey(MaterialType, on_delete=models.CASCADE, related_name="materials", verbose_name="Material Type")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="materials", verbose_name="Course")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="materials", verbose_name="Teacher")

    def __str__(self):
         return f"{self.title} ({self.material_type.name}) - {self.course.title}"
    class Meta:
        verbose_name = "Course Material"
        verbose_name_plural = "Course Materials"
        
    
    def is_accessible(self):
        """Check if the material is active and the associated course is in an active semester."""
        return self.is_active and self.course.semester.is_active

    def get_material_info(self):
        """Return a summary of the material."""
        return {
            "title": self.title,
            "type": self.material_type.name,
            "course": self.course.title,
            "upload_date": self.upload_date,
            "is_active": self.is_active,
        }

    def get_related_materials(self):
        """Retrieve other materials associated with the same course."""
        return self.course.materials.exclude(id=self.id)  # Exclude the current material

    def get_upload_age(self):
        """Calculate how long ago the material was uploaded."""
        age = timezone.now().date() - self.upload_date
        return age.days  # Return the age in days

    def get_teacher_info(self):
        """Retrieve information about the teacher associated with the material."""
        return {
            "name": self.teacher.t_full_name,
            "email": self.teacher.t_email,
            "designation": self.teacher.designation,
        }
class Assignment(models.Model):
    title = models.CharField(max_length=255, verbose_name="Assignment Title")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    
    file = models.FileField(upload_to="assignments/", blank=True, null=True, verbose_name="Assignment File")
    
    deadline = models.DateTimeField(verbose_name="Submission Deadline")
    posted_date = models.DateTimeField(auto_now_add=True, verbose_name="Posted Date")
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="assignments", verbose_name="Course")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="assignments", verbose_name="Teacher")

    def __str__(self):
        return f"{self.title} - {self.course.title} (Deadline: {self.deadline.strftime('%Y-%m-%d %H:%M')})"

    def is_due(self):
        """Check if the assignment is overdue."""
        return timezone.now() > self.deadline

    class Meta:
        verbose_name = "Assignment"
        verbose_name_plural = "Assignments"
        ordering = ["-posted_date"]  