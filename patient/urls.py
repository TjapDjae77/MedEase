from django.urls import path
from .views import register_patient, login_view, profile

urlpatterns = [
    path('register/', register_patient, name='register_patient'),
    path('login/', login_view, name='login'),
    path('profile/', profile, name='profile'),
]
