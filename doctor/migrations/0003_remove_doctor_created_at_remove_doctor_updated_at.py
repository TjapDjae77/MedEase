# Generated by Django 4.2.16 on 2024-12-17 11:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0002_rename_specialty_doctor_speciality'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctor',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='doctor',
            name='updated_at',
        ),
    ]