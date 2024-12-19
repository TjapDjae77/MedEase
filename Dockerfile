# Gunakan image Python sebagai base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Salin file requirements.txt dan install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Salin semua file proyek ke dalam container
COPY . .

# Set environment variable untuk Django
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE MedEase.settings

# Jalankan perintah untuk mengumpulkan file statis
RUN python manage.py collectstatic --noinput

# Jalankan server Django menggunakan Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "MedEase.wsgi:application"]