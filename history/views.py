from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from payment.models import Payment
from consultation.models import Consultation

@login_required
def history_view(request):
    # Ambil semua payment dan consultation untuk user yang login
    payments = Payment.objects.filter(user=request.user).order_by('-created_at')
    consultations = Consultation.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'payments': payments,
        'consultations': consultations
    }
    return render(request, 'history/history.html', context)
