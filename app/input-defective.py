from datetime import datetime
import os
import sqlite3

class InventoryItem:
    def __init__(self, id, jumlah, kategori, tanggal):
        self.id = id
        self.jumlah = jumlah
        self.kategori = kategori
        self.tanggal = tanggal

class InventoryStack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        else:
            return None

    def is_empty(self):
        return len(self.items) == 0

    def clear(self):
        self.items = []

def main():
    # Koneksi ke database SQLite
    db_path = os.path.join(project_root, 'database', 'inventaris.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    inventory_stack = InventoryStack()

    while True:
        print("\nMenu Barang Rusak/Hilang:")
        print("1. Input Barang Rusak/Hilang")
        print("2. Tampilkan Barang Rusak/Hilang")
        print("3. Hapus Barang Rusak/Hilang")
        print("4. Keluar")

        choice = input("Masukkan pilihan Anda: ")

        if choice == "1":
            # Ambil daftar inventaris dari database
            cursor.execute("SELECT id, nama_barang FROM Daftar_Inventaris")
            items = cursor.fetchall()
            
            if items:
                print("\nDaftar Inventaris:")
                for item in items:
                    print(f"ID: {item[0]}, Nama Barang: {item[1]}")
                
                id = input("Silahkan pilih ID barang anda: ")
                jumlah = int(input("Masukkan Jumlah Inventaris Rusak/Hilang: "))
                alasan = input("Masukkan Alasan (Hilang/Rusak): ").strip().capitalize()
                
                # Validasi alasan
                if alasan not in ["Hilang", "Rusak"]:
                    print("Alasan tidak valid. Silakan masukkan 'Hilang' atau 'Rusak'.")
                    continue

                # Ambil detail item dari database
                cursor.execute("SELECT nama_barang, kategori, jumlah FROM Daftar_Inventaris WHERE id = ?", (id,))
                item = cursor.fetchone()

                if item:
                    nama_barang, kategori, jumlah_sekarang = item
                    tanggal = datetime.now().strftime("%Y-%m-%d")
                    
                    if jumlah > jumlah_sekarang:
                        print("Jumlah barang rusak/hilang melebihi jumlah stok.")
                        continue
                    
                    # Update stok di tabel Daftar_Inventaris
                    jumlah_baru = jumlah_sekarang - jumlah
                    cursor.execute("""
                        UPDATE Daftar_Inventaris
                        SET jumlah = ?
                        WHERE id = ?
                    """, (jumlah_baru, id))
                    
                    # Tambahkan item ke tabel Inventaris_Rusak
                    cursor.execute("""
                        INSERT INTO Inventaris_Rusak (tanggal, nama_barang, kategori, jumlah, alasan)
                        VALUES (?, ?, ?, ?, ?)
                    """, (tanggal, nama_barang, kategori, jumlah, alasan))
                    
                    conn.commit()
                    print("Barang berhasil ditambahkan ke daftar barang rusak/hilang.")
                else:
                    print("ID barang tidak ditemukan.")
            else:
                print("Tidak ada data inventaris yang tersedia.")

        elif choice == "2":
            print("Daftar Barang Rusak/Hilang:")
            cursor.execute("SELECT * FROM Inventaris_Rusak")
            items = cursor.fetchall()
            if items:
                print(f"{'ID':<10}{'Tanggal':<15}{'Nama Barang':<20}{'Kategori':<20}{'Jumlah':<10}{'Alasan':<10}")
                print("-" * 75)
                for item in items:
                    print(f"{item[0]:<10}{item[1]:<15}{item[2]:<20}{item[3]:<20}{item[4]:<10}{item[5]:<10}")
            else:
                print("Daftar barang rusak/hilang kosong.")

        elif choice == "3":
            cursor.execute("DELETE FROM Inventaris_Rusak")
            conn.commit()
            print("Semua barang rusak/hilang berhasil dihapus.")

        elif choice == "4":
            print("Terima kasih!")
            conn.close()
            os.system("python ../main.py")
            break

        else:
            print("Pilihan tidak valid. Silakan masukkan pilihan yang benar.")

if __name__ == "__main__":
    # Dapatkan path dari direktori utama
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    main()
