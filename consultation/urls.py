from django.urls import path
from .views import check_consultation_status, consultation_chat, send_message, end_consultation

urlpatterns = [
    path('check-status/<int:consultation_id>/', check_consultation_status, name='check_consultation_status'),
    path('chat/<int:consultation_id>/', consultation_chat, name='consultation_chat'),
    path('send-message/<int:consultation_id>/', send_message, name='send_message'),
    path('end-session/<int:consultation_id>/', end_consultation, name='end_consultation'),
] 