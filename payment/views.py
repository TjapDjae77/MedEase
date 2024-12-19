from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Payment
from consultation.models import Consultation
from doctor.models import Doctor
from decimal import Decimal
import json
from datetime import datetime, time

@login_required
def payment_view(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    package_type = request.GET.get('package_type', 'regular')
    selectedDates = request.session.get('selectedDates')
    selectedTime = request.session.get('selectedTime')
    
    # Hitung biaya
    if package_type == 'regular':
        consultation_fee = doctor.fee_per_session
    elif package_type == '1day':
        consultation_fee = doctor.fee_per_session * Decimal('2') * Decimal('0.90')
    elif package_type == '3day':
        consultation_fee = doctor.fee_per_session * Decimal('6') * Decimal('0.85')
    else:  # 7day
        consultation_fee = doctor.fee_per_session * Decimal('14') * Decimal('0.75')

    admin_fee = Decimal('5000')
    total = consultation_fee + admin_fee

    context = {
        'doctor': doctor,
        'package_type': package_type,
        'selectedDates': selectedDates,
        'selectedTime': selectedTime,
        'consultation_fee': consultation_fee,
        'admin_fee': admin_fee,
        'total': total,
    }
    
    return render(request, 'payment/payment.html', context)

@login_required
def process_payment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            doctor = get_object_or_404(Doctor, id=data.get('doctor_id'))
            package_type = data.get('package_type')
            
            # Konversi string tanggal ke objek date
            consultation_date = datetime.strptime(
                data.get('consultation_date'), 
                '%Y-%m-%d'
            ).date()
            
            # Set default consultation time untuk paket berlangganan
            consultation_time = None
            if package_type in ['1day', '3day', '7day']:
                consultation_time = time(8, 0)  # Set ke 08:00
            elif data.get('consultation_time'):  # Untuk paket regular
                consultation_time = datetime.strptime(
                    data.get('consultation_time'), 
                    '%H:%M'
                ).time()

            # Hitung biaya
            if package_type == 'regular':
                consultation_fee = doctor.fee_per_session
            elif package_type == '1day':
                consultation_fee = doctor.fee_per_session * Decimal('2') * Decimal('0.90')
            elif package_type == '3day':
                consultation_fee = doctor.fee_per_session * Decimal('6') * Decimal('0.85')
            else:  # 7day
                consultation_fee = doctor.fee_per_session * Decimal('14') * Decimal('0.75')

            admin_fee = Decimal('5000')
            total = consultation_fee + admin_fee

            # Buat record Payment
            payment = Payment.objects.create(
                user=request.user,
                doctor=doctor,
                package_type=package_type,
                consultation_fee=consultation_fee,
                admin_fee=admin_fee,
                total_amount=total,
                payment_method=data.get('payment_method'),
                payment_status='paid'  # Untuk simulasi, langsung set paid
            )

            # Buat record Consultation
            consultation = Consultation.objects.create(
                user=request.user,
                doctor=doctor,
                package_type=package_type,
                consultation_date=consultation_date,
                consultation_time=consultation_time,
                status='not_started',
                payment=payment
            )

            return JsonResponse({
                'status': 'success',
                'message': 'Payment processed successfully',
                'redirect_url': '/payment/success/'
            })

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@login_required
def payment_success(request):
    return render(request, 'payment/success.html')
