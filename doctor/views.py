from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Q
from .models import Doctor

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
