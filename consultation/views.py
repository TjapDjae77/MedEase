from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Consultation, Message
import json
import random

# Template pesan dokter
DOCTOR_RESPONSES = [
    "Baik, saya mengerti keluhan Anda. Bisa dijelaskan lebih detail?",
    "Sudah berapa lama Anda mengalami keluhan ini?",
    "Apakah ada gejala lain yang Anda rasakan?",
    "Berdasarkan keluhan Anda, sebaiknya mengurangi asupan gula dan lemak",
    "Jangan lupa untuk banyak istirahat dan minum air putih ya",
]

# Pesan pembuka dari dokter
DOCTOR_GREETING = "Selamat datang di sesi konsultasi. Apa yang bisa saya bantu hari ini?"

@login_required
def start_consultation(request, consultation_id):
    consultation = get_object_or_404(Consultation, id=consultation_id)
    
    # Buat pesan pembuka dari dokter
    Message.objects.create(
        consultation=consultation,
        content=DOCTOR_GREETING,
        is_from_doctor=True
    )
    
    return JsonResponse({'status': 'success', 'message': DOCTOR_GREETING})

@login_required
def send_message(request, consultation_id):
    try:
        if request.method == 'POST':
            consultation = get_object_or_404(Consultation, id=consultation_id)
            data = json.loads(request.body)
            content = data.get('content', '').strip()

            if not content:
                return JsonResponse({'status': 'error', 'message': 'Message cannot be empty'})

            # Simpan pesan user
            user_message = Message.objects.create(
                consultation=consultation,
                content=content,
                is_from_doctor=False
            )

            # Generate dan simpan respons dokter langsung
            doctor_responses = [
                "Baik, saya mengerti keluhan Anda.",
                "Bisa Anda jelaskan lebih detail?", 
                "Sejak kapan keluhan ini Anda rasakan?",
                "Apakah ada gejala lain yang menyertai?",
                "Sudah mencoba pengobatan apa sejauh ini?"
            ]
            
            doctor_message = Message.objects.create(
                consultation=consultation,
                content=random.choice(doctor_responses),
                is_from_doctor=True
            )

            # Pastikan response mencakup semua data yang diperlukan
            return JsonResponse({
                'status': 'success',
                'user_message': {
                    'content': user_message.content,
                    'created_at': user_message.created_at.strftime('%H:%M')
                },
                'doctor_message': {
                    'content': doctor_message.content,
                    'created_at': doctor_message.created_at.strftime('%H:%M')
                }
            })

        return JsonResponse({
            'status': 'error', 
            'message': 'Invalid request method'
        }, status=405)

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@login_required
def get_messages(request, consultation_id):
    consultation = get_object_or_404(Consultation, id=consultation_id)
    consultation.update_status()
    messages = consultation.messages.all()
    
    return JsonResponse({
        'messages': [{
            'content': msg.content,
            'created_at': msg.created_at.strftime('%H:%M'),
            'is_from_doctor': msg.is_from_doctor
        } for msg in messages],
        'consultation_status': consultation.status
    })

@login_required
def check_consultation_status(request, consultation_id):
    consultation = get_object_or_404(Consultation, id=consultation_id)
    
    # Pastikan status terupdate berdasarkan waktu saat ini
    current_status = consultation.update_status()  # Ini akan mengecek dan mengupdate status berdasarkan waktu
    
    # Cek apakah konsultasi masih aktif
    is_active = consultation.is_active()
    remaining_time = consultation.get_remaining_time() if is_active else None
    
    return JsonResponse({
        'status': 'success',
        'consultation_status': current_status,
        'is_active': is_active,
        'remaining_time': remaining_time
    })

@login_required
def consultation_chat(request, consultation_id):
    consultation = get_object_or_404(Consultation, id=consultation_id)
    
    # Update status konsultasi
    consultation.update_status()
    
    context = {
        'consultation': consultation,
        'messages': consultation.messages.all().order_by('created_at')
    }
    return render(request, 'consultation/chat.html', context)

@login_required
def end_consultation(request, consultation_id):
    if request.method == 'POST':
        consultation = get_object_or_404(Consultation, id=consultation_id)
        consultation.end_session()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=405)
