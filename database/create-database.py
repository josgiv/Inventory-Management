import sqlite3
import random
from datetime import datetime, timedelta

# Fungsi untuk membuat koneksi ke database
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

# Fungsi untuk insert data ke tabel Daftar Inventaris
def insert_data_daftar_inventaris(conn, data):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Daftar_Inventaris (tanggal, nama_barang, kategori, jumlah)
            VALUES (?, ?, ?, ?)
        """, data)
        conn.commit()
    except sqlite3.Error as e:
        print(e)

# Fungsi untuk insert data ke tabel Inventaris Rusak
def insert_data_inventaris_rusak(conn, data):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Inventaris_Rusak (tanggal, nama_barang, kategori, jumlah, alasan)
            VALUES (?, ?, ?, ?, ?)
        """, data)
        conn.commit()
    except sqlite3.Error as e:
        print(e)

# Fungsi untuk generate data dummy
def generate_dummy_data():
    categories = [
        ("Kursi",),
        ("Meja",),
        ("Monitor",),
        ("ATK",),
        ("Laptop",),
        ("GPU",)
    ]
    
    dummy_data_daftar_inventaris = []
    dummy_data_inventaris_rusak = []
    
    for category in categories:
        for _ in range(20):
            # Generate nama barang secara acak berdasarkan kategori
            nama_barang = generate_random_name(category[0])
            
            # Generate jumlah acak
            jumlah = random.randint(1, 10)
            
            # Generate tanggal acak dalam rentang 1 tahun terakhir
            tanggal = generate_random_date()
            
            # Data untuk tabel Daftar Inventaris
            data_daftar = (tanggal, nama_barang, category[0], jumlah)
            dummy_data_daftar_inventaris.append(data_daftar)
            
            # Tentukan apakah inventaris rusak secara acak (10% probabilitas)
            if random.random() < 0.1:
                alasan = generate_random_alasan()
                data_rusak = (tanggal, nama_barang, category[0], jumlah, alasan)
                dummy_data_inventaris_rusak.append(data_rusak)
    
    return dummy_data_daftar_inventaris, dummy_data_inventaris_rusak

# Fungsi untuk generate nama barang secara acak berdasarkan kategori
def generate_random_name(category):
    if category == "Kursi":
        return generate_kursi_name()
    elif category == "Meja":
        return generate_meja_name()
    elif category == "Monitor":
        return generate_monitor_name()
    elif category == "ATK":
        return generate_atk_name()
    elif category == "Laptop":
        return generate_laptop_name()
    elif category == "GPU":
        return generate_gpu_name()

# Fungsi untuk generate nama kursi secara acak
def generate_kursi_name():
    types = ["Kursi Kantor", "Kursi Tamu", "Kursi Konferensi"]
    return random.choice(types)

# Fungsi untuk generate nama meja secara acak
def generate_meja_name():
    types = ["Meja Kerja", "Meja Rapat", "Meja Konferensi"]
    return random.choice(types)

# Fungsi untuk generate nama monitor secara acak
def generate_monitor_name():
    types = ["Monitor LCD", "Monitor LED", "Monitor Gaming"]
    return random.choice(types)

# Fungsi untuk generate nama ATK secara acak
def generate_atk_name():
    types = ["Pensil", "Penghapus", "Pulpen", "Spidol"]
    return random.choice(types)

# Fungsi untuk generate nama laptop secara acak
def generate_laptop_name():
    types = ["Laptop HP", "Laptop Dell", "Laptop Asus"]
    return random.choice(types)

# Fungsi untuk generate nama GPU secara acak
def generate_gpu_name():
    types = ["RTX 4090", "GTX 3080", "RX 6900 XT"]
    return random.choice(types)

# Fungsi untuk generate alasan (rusak atau hilang) secara acak
def generate_random_alasan():
    alasanes = ["rusak", "hilang"]
    return random.choice(alasanes)

# Fungsi untuk generate tanggal acak dalam rentang 1 tahun terakhir
def generate_random_date():
    start_date = datetime.now() - timedelta(days=365)
    end_date = datetime.now()
    random_date = start_date + (end_date - start_date) * random.random()
    return random_date.strftime("%Y-%m-%d")

# Fungsi utama untuk menjalankan script
def main():
    database = "database/inventaris.db"

    # Membuat koneksi ke database
    conn = create_connection(database)

    if conn is not None:
        # Generate data dummy
        dummy_data_daftar_inventaris, dummy_data_inventaris_rusak = generate_dummy_data()
        
        # Insert data ke tabel Daftar Inventaris
        for data in dummy_data_daftar_inventaris:
            insert_data_daftar_inventaris(conn, data)
        
        # Insert data ke tabel Inventaris Rusak
        for data in dummy_data_inventaris_rusak:
            insert_data_inventaris_rusak(conn, data)
        
        # Menutup koneksi ke database
        conn.close()
        print("Data dummy telah berhasil di-generate dan di-insert ke dalam database.")
    else:
        print("Koneksi ke database gagal.")

if __name__ == "__main__":
    main()
