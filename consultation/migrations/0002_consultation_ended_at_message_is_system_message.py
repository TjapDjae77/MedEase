# Generated by Django 4.2.16 on 2024-12-18 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='consultation',
            name='ended_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='message',
            name='is_system_message',
            field=models.BooleanField(default=False),
        ),
    ]