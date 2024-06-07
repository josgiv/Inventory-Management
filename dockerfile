# Gunakan base image Python 3.9
FROM python:3.12-slim

# Set working directory di dalam container
WORKDIR /app

# Copy seluruh konten dari direktori aplikasi Anda ke dalam working directory di container
COPY . /app

# Install dependencies yang dibutuhkan
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 ke luar container
EXPOSE 5000

# Jalankan main.py ketika container dijalankan
CMD ["python", "main.py"]

