from django.urls import path
from .views import find_doctor

urlpatterns = [
    path('find/', find_doctor, name='find_doctor'),
]