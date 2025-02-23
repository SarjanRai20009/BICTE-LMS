from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Student

@receiver(post_save, sender=Student)
def send_welcome_email(sender, instance, created, **kwargs):
    """
    Send a welcome email to the student when a new Student instance is created.
    """
    if created and not instance.email_sent:  # Check if it's a new student and email hasn't been sent
        # Access the raw password from the temporary attribute
        raw_password = getattr(instance, '_raw_password', None)

        if raw_password:
            subject = 'Welcome to BICTE-SMC!'
            message = f"""
            Dear {instance.st_name},

            Welcome to BICTE at Sukuna Multiple Campus! We are excited to have you as part of our BICTE-SMC family.

            Here are your registration details:
            - Name: {instance.st_name}
            - Email: {instance.st_email}
            - Roll No: {instance.st_exam_roll_no}
            - Registration No: {instance.st_reg_no}
            - Password: {raw_password}  <!-- Include the raw password here -->

            Please keep your credentials safe and log in to your account to explore more.

            Best regards,
            School Management Team
            """
            from_email = settings.DEFAULT_FROM_EMAIL  # Use the default email from settings
            recipient_list = [instance.st_email]

            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            # Mark email as sent
            instance.email_sent = True
            instance.save()  # Save the instance to update the email_sent field