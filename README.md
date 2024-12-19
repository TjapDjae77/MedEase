# MedEase

## Filosofi Nama
Nama **MedEase** berasal dari gabungan kata "Medical" dan "Ease", yang berarti "Kemudahan Medis". Filosofi ini mencerminkan tujuan kami untuk membuat layanan kesehatan menjadi lebih mudah diakses dan digunakan oleh siapa saja. Selain itu, jika dibaca, "MedEase" terdengar seperti "Medis," menekankan fokus kami pada solusi di bidang kesehatan.

## Fitur

### Paket Konsultasi Fleksibel
- Pengguna dapat memilih paket untuk beberapa hari, memungkinkan konsultasi berkelanjutan tanpa perlu membayar per sesi.
- Fleksibilitas untuk berkonsultasi dengan dokter yang berbeda selama periode paket yang dipilih.

### Akses Online
- Menyediakan platform yang mulus bagi pengguna untuk terhubung dengan tenaga kesehatan kapan saja dan di mana saja.

### Desain Berpusat pada Pengguna
- Antarmuka yang sederhana dan intuitif untuk memastikan kemudahan navigasi dan penggunaan.
- Profil pengguna yang dipersonalisasi dengan catatan lengkap dari konsultasi dan paket yang pernah digunakan.

### Dukungan Multi-Spesialisasi
- Akses ke berbagai spesialis di berbagai bidang kesehatan.

### Keamanan dan Kerahasiaan
- Menjamin penyimpanan data pengguna yang sensitif dengan enkripsi dan standar privasi mutakhir.

## Mengapa MedEase?
MedEase bertujuan untuk menjembatani kesenjangan antara penyedia layanan kesehatan dan pasien dengan menawarkan:
- Solusi hemat biaya dengan model berbasis langganan.
- Kebebasan untuk berganti atau berkonsultasi dengan dokter yang berbeda selama periode langganan.
- Peningkatan aksesibilitas layanan kesehatan, terutama bagi individu dengan jadwal sibuk atau keterbatasan mobilitas.

## Teknologi yang Digunakan

### Frontend
- HTML, CSS, JavaScript

### Backend
- Django

### Database
- PostgreSQL

### Platform Hosting
- Backend: Railway
- Frontend: Vercel

### DevOps
- Docker (untuk backend)

## Instalasi dan Pengaturan

### Prasyarat
- Python (3.8 atau lebih tinggi)
- PostgreSQL
- Docker

### Langkah-langkah
1. Clone repositori:
   ```bash
   git clone https://github.com/yourusername/medease.git
   ```
2. Masuk ke direktori proyek:
   ```bash
   cd medease
   ```
3. Instal dependensi yang diperlukan:
   ```bash
   pip install -r requirements.txt
   ```
4. Atur database PostgreSQL dan perbarui file `settings.py` dengan kredensial database Anda.
5. Jalankan migrasi database:
   ```bash
   python manage.py migrate
   ```
6. Jalankan server pengembangan:
   ```bash
   python manage.py runserver
   ```

## Panduan Kontribusi
Kami menyambut kontribusi dari pengembang, desainer, dan profesional kesehatan. Untuk berkontribusi:
1. Fork repositori ini.
2. Buat branch fitur baru:
   ```bash
   git checkout -b nama-fitur
   ```
3. Commit perubahan Anda:
   ```bash
   git commit -m "Deskripsi perubahan Anda"
   ```
4. Push ke branch Anda:
   ```bash
   git push origin nama-fitur
   ```
5. Ajukan pull request.

## Lisensi
Proyek ini dilisensikan di bawah Lisensi MIT. Lihat file `LICENSE` untuk detailnya.

## Kontak
Untuk pertanyaan atau dukungan, silakan hubungi kami di [support@medease.com](mailto:support@medease.com).

