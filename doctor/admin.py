from django.contrib import admin
from .models import Doctor

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'speciality', 'gender', 'rate', 'fee_per_session')
    list_filter = ('speciality', 'gender')
    search_fields = ('name', 'speciality')
    ordering = ('name',)
