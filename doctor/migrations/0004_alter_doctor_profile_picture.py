# Generated by Django 4.2.16 on 2024-12-17 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0003_remove_doctor_created_at_remove_doctor_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='profile_picture',
            field=models.ImageField(upload_to='media/doctors/', verbose_name='Foto Profil'),
        ),
    ]
