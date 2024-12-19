from django.db import models

class Doctor(models.Model):
    GENDER_CHOICES = [
        ('M', 'Laki-laki'),
        ('F', 'Perempuan'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="Nama Lengkap")
    speciality = models.CharField(max_length=100, verbose_name="Spesialisasi")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="Jenis Kelamin")
    rate = models.DecimalField(max_digits=3, decimal_places=1, default=5.0, verbose_name="Rating")
    fee_per_session = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Biaya per Sesi")
    description = models.TextField(null=True, blank=True, verbose_name="Deskripsi")
    profile_picture = models.ImageField(upload_to='media/doctor/', verbose_name="Foto Profil")

    class Meta:
        verbose_name = "Dokter"
        verbose_name_plural = "Dokter"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - {self.speciality}"
