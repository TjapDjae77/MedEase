from django.urls import path
from .views import find_doctor, appointment, schedule_view, save_schedule, connecting_view, consultation_status

urlpatterns = [
    path('find/', find_doctor, name='find_doctor'),
    path('appointment/<int:doctor_id>/', appointment, name='appointment'),
    path('schedule/<int:doctor_id>/<str:package_type>/', schedule_view, name='schedule'),
    path('save_schedule/<int:doctor_id>/<str:package_type>/', save_schedule, name='save_schedule'),
    path('<int:doctor_id>/connecting/', connecting_view, name='connecting'),
    path('<int:doctor_id>/consultation-status/', consultation_status, name='consultation_status'),
]