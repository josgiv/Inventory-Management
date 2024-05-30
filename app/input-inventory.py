import os
import sys
import sqlite3
from datetime import datetime

class InventoryStack:
    def __init__(self):
        self.stack = []

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        if not self.is_empty():
            return self.stack.pop()
        return None

    def is_empty(self):
        return len(self.stack) == 0

    def display(self):
        if self.is_empty():
            print("Inventaris kosong.")
        else:
            for item in self.stack:
                print(item)

def add_inventory_item(inventory_stack):
    print("=== Tambah Inventaris Baru ===")

    # Koneksi ke database SQLite
    db_path = os.path.join(project_root, 'database', 'inventaris.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    while True:
        nama_barang = input("Masukkan Nama Barang: ")
        kategori = input("Masukkan Kategori: ")
        jumlah = input("Masukkan Jumlah: ")
        tanggal = datetime.now().strftime("%Y-%m-%d")

        # Buat item inventaris baru sebagai dictionary
        item = {
            "Nama Barang": nama_barang,
            "Kategori": kategori,
            "Jumlah": jumlah,
            "Tanggal": tanggal
        }

        # Tambahkan item ke stack
        inventory_stack.push(item)

        # Simpan item ke database
        cursor.execute("""
            INSERT INTO Daftar_Inventaris (tanggal, nama_barang, kategori, jumlah)
            VALUES (?, ?, ?, ?)
        """, (tanggal, nama_barang, kategori, jumlah))
        conn.commit()

        # Tampilkan item yang baru ditambahkan
        print("\nItem yang baru ditambahkan:")
        print(item)

        # Tanyakan apakah ingin menambahkan item lagi atau keluar
        lanjut = input("\nApakah Anda ingin menambahkan item lain? (ya/tidak): ").strip().lower()
        if lanjut != 'ya':
            # Jika pengguna tidak ingin menambahkan item lagi, panggil fungsi main_menu
            conn.close()
            main.main_menu()
            break

# Dapatkan path dari direktori utama
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Tambahkan path ke sys.path
if project_root not in sys.path:
    sys.path.append(project_root)

# mengimpor modul main
import main

# Buat instance InventoryStack
inventory_stack = InventoryStack()

# Panggil fungsi untuk menambahkan item inventaris
add_inventory_item(inventory_stack)
