from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MaxValueValidator, MinValueValidator

from django.db.models import Sum

from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ValidationError


# Create your models here.

class Teacher(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    profile_picture = models.ImageField(upload_to='teacher_pics/', null=True, blank=True, default='images/default_profile_image.jpg')    
    t_full_name = models.CharField(max_length=50)
    designation = models.CharField(max_length=100, default='Teacher Assistant')
    
    t_email = models.EmailField(max_length=100, unique=True)
    t_password = models.CharField(max_length=255) 
    
    t_phone_number = models.CharField(max_length=40)
    t_address = models.CharField(max_length=100)
    
    
    hire_date = models.DateField()
    
    gender = models.CharField(max_length=10,choices=GENDER_CHOICES, verbose_name="Gender",
        default='male')
    
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
    syllabus_file = models.FileField(upload_to='syllabus_files/', null=True, blank=True) 
    subject_code = models.CharField(max_length=20)
    title = models.CharField(max_length=50)
    description = models.TextField()
    credits = models.IntegerField()
    
    is_elective = models.BooleanField(default=False, blank=True, null=True)


    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"{self.title} ({self.subject_code})"

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"
        
    def get_course_teacher(self):
        return self.teacher.t_full_name if self.teacher else "Not Assigned"
    
class Book(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False)
    author = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"

class CourseObjectives(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='objectives', verbose_name="Course")
    objective = models.CharField(max_length=255)
   

    def __str__(self):
        return f"Objective for {self.course.title}"

    class Meta:
        verbose_name = "Course Objective"
        verbose_name_plural = "Course Objectives"
        
class Student(models.Model):    
    profile_picture = models.ImageField(upload_to='student_pics/', null=True, blank=True , default='no_image2.jpg') 
    
    st_exam_roll_no = models.CharField(max_length=8, default='00000000') 
    st_reg_no = models.CharField(max_length=40, default='0-0-000-00-0000')  
    
    st_name = models.CharField(max_length=100)
    st_date_of_birth = models.DateField(null=True, blank=True)
    st_address = models.CharField(max_length=255)
    st_contact = models.CharField(max_length=15)
    enrollment_date = models.IntegerField(null=True, blank=True)  
    
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
                self.st_password = make_password(self.st_password) 
        else:  # New user
            self.st_password = make_password(self.st_password) 

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
        
class AssignmentSubmit(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    submit_date = models.DateTimeField(auto_now_add=True)
    assignment_file = models.FileField(upload_to="assignments/")

    def __str__(self):
        return f"{self.student.username} - {self.assignment.title}"
    class Meta:
        verbose_name = "Assignment Submission"
        verbose_name_plural = "Assignment Submissions"

        
        
class Result(models.Model):
    title = models.CharField(max_length=255, verbose_name="Result Title")
    file = models.FileField(upload_to="results/", verbose_name="Result File")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Uploaded At")
    
    user = models.ForeignKey(User, on_delete=models.CASCADE,  blank=True, null=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name="results", verbose_name="Semester")

    def __str__(self):
        return f"{self.title} (Semester: {self.semester.se_name})"
    
    def save(self, *args, **kwargs):
        """Override save method to ensure result is accessible to all students in the semester."""
        super().save(*args, **kwargs)  # Save the result first

       
        students_in_semester = Student.objects.filter(semester=self.semester)

      
        for student in students_in_semester:
            self.notify_student(student)

    def notify_student(self, student):
        """Notify a student about the new result."""
      
        print(f"Notifying student {student.st_name} about the new result: {self.title}")

    class Meta:
        verbose_name = "Result"
        verbose_name_plural = "Results"
        
        
        
class Notice(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    link = models.URLField(blank=True, null=True) 
    notic_file = models.FileField(upload_to="notices/", blank=True, null=True, verbose_name="Notice File")
    timestamp = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Associate notice with a user

    def __str__(self):
        return self.title

class Quiz(models.Model):
    title = models.CharField(max_length=255, verbose_name="Quiz Title")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")
    is_active = models.BooleanField(default=True, verbose_name="Is Active")

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="quizzes", verbose_name="Course")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="quizzes", verbose_name="Teacher")
    def __str__(self):
        return f"{self.title} - {self.course.title}"

    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quizzes"
        
class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions", verbose_name="Quiz")
    text = models.TextField(verbose_name="Question Text")
    option1 = models.CharField(max_length=255, verbose_name="Option 1")
    option2 = models.CharField(max_length=255, verbose_name="Option 2")
    option3 = models.CharField(max_length=255, verbose_name="Option 3", blank=True, null=True)
    option4 = models.CharField(max_length=255, verbose_name="Option 4", blank=True, null=True)
    correct_option = models.CharField(
        max_length=10,
        choices=[("1", "Option 1"), ("2", "Option 2"), ("3", "Option 3"), ("4", "Option 4")],
        verbose_name="Correct Option"
    )
    marks = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(10)], verbose_name="Marks")

    def __str__(self):
        return f"{self.text} (Quiz: {self.quiz.title})"

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"


class QuizAttempt(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="quiz_attempts", verbose_name="Student")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="attempts", verbose_name="Quiz")
    
    score = models.PositiveIntegerField(default=0, verbose_name="Score")
    attempted_at = models.DateTimeField(auto_now_add=True, verbose_name="Attempted At")

    def __str__(self):
        return f"{self.student.st_name} - {self.quiz.title} (Score: {self.score})"

    class Meta:
        verbose_name = "Quiz Attempt"
        verbose_name_plural = "Quiz Attempts"
class UserRank(models.Model):
    student = models.OneToOneField('Student', on_delete=models.CASCADE, related_name="rank")
    rank = models.IntegerField(null=True, blank=True)
    total_score = models.IntegerField(default=0)

    def __str__(self):
        return f"Rank {self.rank}: {self.student.st_name} (Total Score: {self.total_score})"

    @receiver(post_save, sender= QuizAttempt)  # Use the correct model name
    def update_user_rank(sender, instance, **kwargs):
        update_leaderboard()


def update_leaderboard():
    user_scores = (
        QuizAttempt.objects.values('student')
        .annotate(total_score=Sum('score'))
        .order_by('-total_score',)
    )

    rank = 1
    for entry in user_scores:
        student_id = entry['student']
        total_score = entry['total_score']
        
        # Update or create a UserRank entry
        user_rank, created = UserRank.objects.update_or_create(
            student_id=student_id,
            defaults={'total_score': total_score, 'rank': rank}
        )
        rank += 1
class Notification(models.Model):
    title = models.CharField(max_length=255, verbose_name="Notification Title")
    content = models.TextField(verbose_name="Notification Content")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_notifications", verbose_name="Created By")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    is_active = models.BooleanField(default=True, verbose_name="Is Active")

    def __str__(self):
        return f"{self.title} by {self.created_by.username}"

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = ["-created_at"]
class News(models.Model):
    title = models.CharField(max_length=255, verbose_name="News Title")
    content = models.TextField(verbose_name="News Content")
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posted_news", verbose_name="Posted By")
    posted_at = models.DateTimeField(auto_now_add=True, verbose_name="Posted At")
    is_active = models.BooleanField(default=True, verbose_name="Is Active")

    def __str__(self):
        return f"{self.title} by {self.posted_by.username}"

    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"
        ordering = ["-posted_at"]

class MessageGroup(models.Model):
    name = models.CharField(max_length=100, verbose_name="Group Name")
    teacher_creator = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="created_groups", null=True, blank=True)
    student_creator = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="created_groups", null=True, blank=True)
    students = models.ManyToManyField(Student, related_name="message_groups", blank=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name="message_groups", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    def __str__(self):
        return f"{self.name} (Semester: {self.semester.se_name if self.semester else 'No Semester'})"

    class Meta:
        verbose_name = "Message Group"
        verbose_name_plural = "Message Groups"
class Message(models.Model):
    # Allow sender to be either a Teacher or a Student
    teacher_sender = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="sent_messages", null=True, blank=True)
    student_sender = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="sent_messages", null=True, blank=True)
    
    # Receiver can be a Student, Teacher, or Group
    student_receiver = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="received_messages", null=True, blank=True)
    teacher_receiver = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="received_messages", null=True, blank=True)
    group = models.ForeignKey('MessageGroup', on_delete=models.CASCADE, related_name="group_messages", null=True, blank=True)
    
    content = models.TextField(verbose_name="Message Content")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Timestamp")
    is_read = models.BooleanField(default=False, verbose_name="Is Read")

    def __str__(self):
        if self.group:
            return f"Group Message in {self.group.name} by {self.get_sender_name()}"
        return f"Message from {self.get_sender_name()} to {self.get_receiver_name()}"

    def get_sender_name(self):
        """Returns the name of the sender, whether it's a teacher or a student."""
        if self.teacher_sender:
            return self.teacher_sender.t_full_name
        elif self.student_sender:
            return self.student_sender.st_name
        return "Anonymous"

    def get_receiver_name(self):
        """Returns the name of the receiver, whether it's a student, teacher, or group."""
        if self.student_receiver:
            return self.student_receiver.st_name
        elif self.teacher_receiver:
            return self.teacher_receiver.t_full_name
        elif self.group:
            return f"Group: {self.group.name}"
        return "Unknown"

    def save(self, *args, **kwargs):
        """Override save method to handle group messaging."""
        if self.group:  # If the message is sent to a group
            group_members = self.group.students.all()  # Retrieve all group members
            for member in group_members:
                # Create a new message for each group member
                Message.objects.create(
                    student_sender=self.student_sender,
                    teacher_sender=self.teacher_sender,
                    student_receiver=member,  # Set the receiver to the group member
                    content=self.content,
                    is_read=False,
                )
            # Do not save the original group message (it's redundant)
            return
        super().save(*args, **kwargs)  # Save individual messages

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        ordering = ["-timestamp"]
