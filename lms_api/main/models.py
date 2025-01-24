from django.db import models

# Create your models here.
class Teacher(models.Model):
    # profile_picture = models.ImageField(upload_to='teacher_pics/', null=True, blank=True)  # Profile picture
   
    t_full_name = models.CharField(max_length=50)
    t_phone_number = models.CharField(max_length=40)
    t_address = models.CharField(max_length=100)
    
    t_email = models.EmailField(max_length=100, unique=True)
    t_password = models.CharField(max_length=100)
    
    hire_date = models.DateField()
    designation = models.CharField(max_length=100, default='Lecturer')

    def __str__(self):
        return f"{self.t_full_name} - {self.t_email} - {self.t_phone_number}"

    class Meta:
        verbose_name_plural = "Teachers"

class Semester(models.Model):
    EVEREST = "EV"
    ANNAPURNA = "AN"
    KANCHENJUNGA = "KA"
    MANASLU = "MA"
    LHOTSE = "LH"
    MAKALU = "MK"
    DHAULAGIRI = "DH"
    LANGTANG = "LA"
    
    SEMESTER_CHOICES = {
        EVEREST: "Everest(1st sem)",
        ANNAPURNA: "Annapurna(2nd sem)",
        KANCHENJUNGA: "Kanchenjunga(3rd sem)",
        MANASLU: "Manaslu(4th sem)",
        LHOTSE: "Lhotse(5th sem)",
        MAKALU: "Makalu(6th sem)",
        DHAULAGIRI: "Dhaulagiri(7th sem)",
        LANGTANG: "Langtang(8th sem)",
    }
    
    se_name = models.CharField(
        max_length=2,
        choices=SEMESTER_CHOICES,
        default=EVEREST,
    )
    batch = models.CharField(max_length=20)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.get_se_name_display()

    class Meta:
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
    
    # syllabus_file = models.FileField(upload_to='syllabus_files/', null=True, blank=True)  # Syllabus file

    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.title} ({self.subject_code})"

    class Meta:
        verbose_name_plural = "Courses"
    
class Student(models.Model):
    # profile_picture = models.ImageField(upload_to='student_pics/', null=True, blank=True)  # Profile picture
    st_exam_roll_no = models.CharField(max_length=8, default='00000000')  # Use CharField with fixed length and default value
    st_reg_no = models.CharField(max_length=40, default='0-0-000-00-0000')  # Provide a default value
    
    st_name = models.CharField(max_length=100)
    st_contact = models.CharField(max_length=15)
    enrollment_date = models.IntegerField()  # Store only the year
    
    st_email = models.EmailField(unique=True)
    st_address = models.CharField(max_length=255)

    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.st_name} - {self.st_email} - {self.st_contact}" 
    class Meta:
        verbose_name_plural = "Students"