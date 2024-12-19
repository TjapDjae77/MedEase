from django.db import models
from django.contrib.auth.models import User
from doctor.models import Doctor
from django.utils import timezone
from datetime import datetime, time, timedelta
import random

class Consultation(models.Model):
    STATUS_CHOICES = [
        ('not_started', 'Belum mulai'),
        ('in_progress', 'Sedang berlangsung'),
        ('completed', 'Telah berakhir'),
    ]
    
    PACKAGE_TYPES = [
        ('regular', 'Regular'),
        ('1day', '1 Day'),
        ('3day', '3 Days'),
        ('7day', '7 Days'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    package_type = models.CharField(max_length=10, choices=PACKAGE_TYPES)
    consultation_date = models.DateField()
    consultation_time = models.TimeField(null=True, blank=True)  # Opsional, untuk paket regular
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='not_started'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    payment = models.OneToOneField('payment.Payment', on_delete=models.CASCADE, null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.doctor.name} ({self.get_package_type_display()})"

    def save(self, *args, **kwargs):
        # Pastikan tanggal konsultasi menggunakan timezone yang benar
        if self.consultation_date and not timezone.is_aware(datetime.combine(self.consultation_date, time())):
            self.consultation_date = timezone.make_aware(
                datetime.combine(self.consultation_date, time())
            ).date()
        
        # Set default time untuk paket berlangganan jika belum diset
        if self.package_type in ['1day', '3day', '7day'] and not self.consultation_time:
            self.consultation_time = time(8, 0)
            
        # Set default ended_at saat pertama kali dibuat
        if not self.pk and not self.ended_at:  # Jika objek baru dan ended_at belum diset
            start_datetime = timezone.make_aware(
                datetime.combine(self.consultation_date, self.consultation_time or time(8, 0))
            )
            
            if self.package_type == 'regular':
                # Untuk regular: 30 menit setelah waktu mulai
                self.ended_at = start_datetime + timedelta(minutes=30)
            else:
                # Untuk paket: pukul 20:00 pada hari terakhir
                if self.package_type == '1day':
                    end_date = self.consultation_date
                elif self.package_type == '3day':
                    end_date = self.consultation_date + timedelta(days=2)
                else:  # 7day
                    end_date = self.consultation_date + timedelta(days=6)
                
                self.ended_at = timezone.make_aware(
                    datetime.combine(end_date, time(20, 0))
                )
        
        super().save(*args, **kwargs)

    def update_status(self):
        """Update status konsultasi berdasarkan waktu"""
        now = timezone.now()
        start_datetime = timezone.make_aware(
            datetime.combine(self.consultation_date, self.consultation_time or time(8, 0))
        )
        
        # Pastikan ended_at sudah diset
        if not self.ended_at:
            if self.package_type == 'regular':
                self.ended_at = start_datetime + timedelta(minutes=30)
            else:
                if self.package_type == '1day':
                    end_date = self.consultation_date
                elif self.package_type == '3day':
                    end_date = self.consultation_date + timedelta(days=2)
                else:  # 7day
                    end_date = self.consultation_date + timedelta(days=6)
                
                self.ended_at = timezone.make_aware(
                    datetime.combine(end_date, time(20, 0))
                )
            self.save()

        # Update status berdasarkan waktu
        if now >= self.ended_at:
            new_status = 'completed'
        elif now < start_datetime:
            new_status = 'not_started'
        else:
            new_status = 'in_progress'
            # Cek apakah perlu mengirim greeting
            if (self.status != new_status or  # Status baru berubah ke in_progress
                (new_status == 'in_progress' and not self.messages.exists())):  # Belum ada pesan sama sekali
                self.send_greeting()

        # Jika status berubah, simpan perubahan
        if self.status != new_status:
            self.status = new_status
            self.save(update_fields=['status'])

        return self.status

    def get_end_datetime(self):
        start_datetime = datetime.combine(self.consultation_date, self.consultation_time or time(8, 0))
        
        if self.package_type == 'regular':
            # Untuk regular, tambah 30 menit
            return start_datetime + timedelta(minutes=30)
        else:
            # Untuk paket, hitung berdasarkan jumlah hari
            if self.package_type == '1day':
                end_date = self.consultation_date
            elif self.package_type == '3day':
                end_date = self.consultation_date + timedelta(days=2)
            else:  # 7day
                end_date = self.consultation_date + timedelta(days=6)
            
            # Set waktu berakhir ke 20:00
            return datetime.combine(end_date, time(20, 0))

    def get_consultation_period_display(self):
        start_time = self.consultation_time or time(8, 0)
        end_datetime = self.get_end_datetime()
        
        if self.package_type == 'regular':
            return f"{start_time.strftime('%H:%M')} - {end_datetime.strftime('%H:%M')}"
        else:
            return f"{self.consultation_date.strftime('%d/%m/%Y')} {start_time.strftime('%H:%M')} - {end_datetime.strftime('%d/%m/%Y %H:%M')}"

    def get_time_until_start(self):
        now = timezone.localtime(timezone.now())
        start_datetime = timezone.make_aware(
            datetime.combine(self.consultation_date, self.consultation_time or time(8, 0)),
            timezone=timezone.get_current_timezone()
        )
        
        if now >= start_datetime:
            return None
        
        time_diff = start_datetime - now
        return time_diff

    def send_greeting(self):
        """Mengirim pesan greeting dari dokter saat konsultasi dimulai"""
        # Cek apakah sudah ada pesan dalam konsultasi ini
        if not self.messages.exists():
            greetings = [
                f"Halo, saya {self.doctor.name}. Apa yang bisa saya bantu hari ini?",
                f"Selamat datang di sesi konsultasi. Saya {self.doctor.name}, ada yang bisa saya bantu?",
                f"Halo, terima kasih sudah memilih saya sebagai dokter konsultan Anda. Apa keluhan Anda?",
            ]
            Message.objects.create(
                consultation=self,
                content=random.choice(greetings),
                is_from_doctor=True
            )

    def end_session(self):
        self.status = 'completed'
        self.ended_at = timezone.now()
        self.save()

    def is_active(self):
        """Mengecek apakah konsultasi masih aktif"""
        now = timezone.now()
        return self.status == 'in_progress' and now < self.ended_at

    def get_remaining_time(self):
        """Mendapatkan sisa waktu konsultasi"""
        if not self.is_active():
            return None
            
        now = timezone.now()
        
        # Pastikan ended_at sudah diset
        if not self.ended_at:
            start_datetime = timezone.make_aware(
                datetime.combine(self.consultation_date, self.consultation_time or time(8, 0))
            )
            
            if self.package_type == 'regular':
                self.ended_at = start_datetime + timedelta(minutes=30)
            else:
                if self.package_type == '1day':
                    end_date = self.consultation_date
                elif self.package_type == '3day':
                    end_date = self.consultation_date + timedelta(days=2)
                else:  # 7day
                    end_date = self.consultation_date + timedelta(days=6)
                
                self.ended_at = timezone.make_aware(
                    datetime.combine(end_date, time(20, 0))
                )
            self.save()
            
        remaining = self.ended_at - now
        
        if remaining.total_seconds() <= 0:
            return None
            
        hours = remaining.seconds // 3600
        minutes = (remaining.seconds % 3600) // 60
        seconds = remaining.seconds % 60
        
        if remaining.days > 0:
            return f"{remaining.days} hari {hours} jam {minutes} menit {seconds} detik"
        elif hours > 0:
            return f"{hours} jam {minutes} menit {seconds} detik"
        elif minutes > 0:
            return f"{minutes} menit {seconds} detik"
        else:
            return f"{seconds} detik"

class Message(models.Model):
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    is_from_doctor = models.BooleanField(default=False)
    is_system_message = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
