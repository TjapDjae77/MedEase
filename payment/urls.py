from django.urls import path
from .views import payment_view, payment_success, process_payment

urlpatterns = [
    path('payment/<int:doctor_id>/', payment_view, name='payment'),
    path('process/', process_payment, name='process_payment'),
    path('success/', payment_success, name='payment_success'),
] 