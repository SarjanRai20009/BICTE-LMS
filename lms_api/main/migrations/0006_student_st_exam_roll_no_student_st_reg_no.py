# Generated by Django 5.1.5 on 2025-01-23 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_remove_teacher_qualification'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='st_exam_roll_no',
            field=models.CharField(default='00000000', max_length=8),
        ),
        migrations.AddField(
            model_name='student',
            name='st_reg_no',
            field=models.CharField(default='0-0-000-00-0000', max_length=40),
        ),
    ]
