from .models import Doctor
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
import random

@login_required
def find_doctor(request):
    search_query = request.GET.get('q', '')
    gender_filter = request.GET.get('gender', '')
    speciality_filters = request.GET.getlist('speciality')


    # Base queryset
    doctors = Doctor.objects.all()
    
    # Apply search filter if exists
    if search_query:
        doctors = doctors.filter(
            Q(name__icontains=search_query) |
            Q(speciality__icontains=search_query)
        )
    
    # Apply gender filter if selected
    if gender_filter in ['M', 'F']:
        doctors = doctors.filter(gender=gender_filter)

    if speciality_filters:
        doctors = doctors.filter(speciality__in=speciality_filters)
    
    specialities = Doctor.objects.values_list('speciality', flat=True).distinct().order_by('speciality')

    context = {
        'doctors': doctors,
        'search_query': search_query,
        'gender_filter': gender_filter,
        'speciality_filters': speciality_filters,
        'specialities': specialities,
    }
    return render(request, 'doctor/find_doctor.html', context)

@login_required
def appointment(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    
    # Hitung harga paket
    one_day_price = doctor.fee_per_session * Decimal('2') * Decimal('0.90')  # 10% diskon
    three_day_price = doctor.fee_per_session * Decimal('6') * Decimal('0.85')  # 15% diskon
    seven_day_price = doctor.fee_per_session * Decimal('14') * Decimal('0.75')  # 25% diskon
    
    context = {
        'doctor': doctor,
        'one_day_price': one_day_price,
        'three_day_price': three_day_price,
        'seven_day_price': seven_day_price,
    }
    return render(request, 'doctor/appointment.html', context)

@login_required
def schedule_view(request, doctor_id, package_type):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    
    # Menentukan harga berdasarkan tipe paket
    if package_type == 'regular':
        price = doctor.fee_per_session
    elif package_type == '1day':
        price = doctor.fee_per_session * Decimal('2') * Decimal('0.90')  # Misalnya 3x konsultasi per hari
    elif package_type == '3day':
        price = doctor.fee_per_session * Decimal('6') * Decimal('0.85')  # Misalnya 7x konsultasi untuk 3 hari
    elif package_type == '7day':
        price = doctor.fee_per_session * Decimal('14') * Decimal('0.75')  # Misalnya 15x konsultasi untuk 7 hari
    else:
        # Handle invalid package type
        return redirect('appointment', doctor_id=doctor_id)

    context = {
        'doctor': doctor,
        'package_type': package_type,
        'price': price,
    }
    
    return render(request, 'doctor/schedule.html', context)

@login_required
def save_schedule(request, doctor_id, package_type):
    if request.method == 'POST':
        doctor = get_object_or_404(Doctor, id=doctor_id)
        
        # Debug: print semua data POST
        print("POST data:", request.POST)
        print('Selected Date:', request.POST.get('selectedDate'))
        print('Selected Time:', request.POST.get('selectedTime'))
        
        # Simpan data ke session dengan nama field yang sesuai
        selectedDate = request.POST.get('selectedDate')
        request.session['selectedDates'] = selectedDate
        print("(save_schedule) selectedDates:", selectedDate)
        
        if package_type == 'regular':
            selectedTime = request.POST.get('selectedTime')
            request.session['selectedTime'] = selectedTime
            print("(save_schedule) selectedTime:", selectedTime)
        
        base_url = reverse('connecting', kwargs={'doctor_id': doctor_id})
        return redirect(f'{base_url}?package_type={package_type}')
    return redirect('schedule', doctor_id=doctor_id, package_type=package_type)

@login_required
def connecting_view(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    package_type = request.GET.get('package_type', 'regular')
    print(f"Doctor Name: {doctor.name}, Package Type: {package_type}")
    return render(request, 'doctor/connecting.html', {
        'doctor': doctor,
        'package_type': package_type
    })

@login_required
def consultation_status(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    package_type = request.GET.get('package_type', 'regular')
    
    # Simulasi 50-50 chance
    is_accepted = random.choice([True, False])
    
    if is_accepted:
        print(f"(ACCEPTED) Doctor Name: {doctor.name}, Package Type: {package_type}")
        return render(request, 'doctor/accepted.html', {
            'doctor': doctor,
            'package_type': package_type
        })
    else:
        return render(request, 'doctor/rejected.html', {
            'doctor': doctor,
            'package_type': package_type
        })
