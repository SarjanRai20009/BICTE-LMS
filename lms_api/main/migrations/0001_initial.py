# Generated by Django 5.1.5 on 2025-01-23 02:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('batch', models.CharField(max_length=20)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('t_full_name', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('passwrord', models.CharField(max_length=100)),
                ('t_phone_number', models.CharField(max_length=40)),
                ('hire_date', models.DateField()),
                ('qualification', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('st_name', models.CharField(max_length=100)),
                ('contact', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('address', models.CharField(max_length=255)),
                ('enrollment_date', models.DateField()),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.semester')),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_code', models.CharField(max_length=20)),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('credits', models.IntegerField()),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.semester')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.teacher')),
            ],
        ),
    ]
