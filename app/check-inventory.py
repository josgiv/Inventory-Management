import os
import sqlite3

# Dapatkan path dari direktori utama
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Fungsi untuk menampilkan daftar inventaris
def show_inventory(cursor):
    cursor.execute("SELECT * FROM Daftar_Inventaris")
    inventaris = cursor.fetchall()

    print("\n=== Data Inventaris ===\n")
    if inventaris:
        print(f"{'ID':<10}{'Nama Barang':<20}{'Kategori':<20}{'Jumlah':<10}")
        print("-" * 60)
        for row in inventaris:
            print(f"{row[0]:<10}{row[1]:<20}{row[2]:<20}{row[3]:<10}")
    else:
        print("Inventaris kosong.")

# Fungsi untuk menampilkan daftar barang rusak/hilang
def show_defective(cursor):
    cursor.execute("SELECT * FROM Inventaris_Rusak")
    defective = cursor.fetchall()

    print("\n=== Data Barang Rusak/Hilang ===\n")
    if defective:
        print(f"{'ID':<10}{'Nama Barang':<20}{'Kategori':<20}{'Jumlah':<10}{'Tanggal':<15}{'Alasan':<10}")
        print("-" * 85)
        for row in defective:
            print(f"{row[0]:<10}{row[1]:<20}{row[2]:<20}{row[3]:<10}{row[4]:<15}{row[5]:<10}")
    else:
        print("Tidak ada data barang yang rusak/hilang.")

# Fungsi untuk menampilkan semua tabel
def show_all_tables():
    # Koneksi ke database SQLite
    db_path = os.path.join(project_root, 'database', 'inventaris.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Tampilkan daftar inventaris
    show_inventory(cursor)

    # Tampilkan daftar barang rusak/hilang
    show_defective(cursor)

    # Tutup koneksi database
    conn.close()

# Jalankan fungsi untuk menampilkan semua tabel
show_all_tables()
