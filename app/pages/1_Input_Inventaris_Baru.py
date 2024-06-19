import os
import sqlite3
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Input Inventaris Baru", page_icon="📝")

# Class untuk stack inventaris
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

# Fungsi untuk menambahkan item ke dalam database dan stack inventaris
def add_inventory_item(inventory_stack, nama_barang, kategori, jumlah, gambar_bytes):
    # Koneksi ke database SQLite
    db_path = os.path.join(project_root, '..', 'database', 'inventaris.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Tanggal saat ini
    tanggal = datetime.now().strftime("%Y-%m-%d")

    # Ubah gambar menjadi nama file jika ada
    if gambar_bytes:
        nama_file_gambar = os.path.basename(gambar_bytes.name)
        gambar = gambar_bytes.read()
    else:
        nama_file_gambar = None
        gambar = None

    # Membuat item inventaris baru sebagai dictionary
    item = {
        "Nama Barang": nama_barang,
        "Kategori": kategori,
        "Jumlah": jumlah,
        "Gambar": nama_file_gambar, 
        "Tanggal": tanggal
    }

    # Tambahkan item ke stack
    inventory_stack.push(item)

    # Simpan item ke database
    cursor.execute("""
        INSERT INTO Daftar_Inventaris (tanggal, nama_barang, kategori, jumlah, gambar)
        VALUES (?, ?, ?, ?, ?)
    """, (tanggal, nama_barang, kategori, jumlah, gambar))
    conn.commit()

    # Tutup koneksi database
    conn.close()

    return item



# Fungsi utama untuk menampilkan UI dan menambahkan item inventaris
def main():
    # Judul halaman
    st.title("Input Inventaris Baru")

    # Deskripsi singkat tentang fitur di halaman ini
    st.write("Halaman ini memungkinkan Anda untuk memasukkan data inventaris baru ke dalam sistem. Anda dapat mengisi informasi tentang nama barang, kategori, jumlah, dan mengunggah gambar inventaris yang ingin Anda tambahkan. Setelah menambahkan item, Anda akan melihat detail item baru di bawah.")
    st.write("___")
    
    # Buat instance InventoryStack
    inventory_stack = InventoryStack()

    # Input form untuk menambahkan item inventaris
    nama_barang = st.text_input("Nama Barang:")
    
    # Koneksi ke database SQLite untuk mengambil opsi pilihan kategori
    db_path = os.path.join(project_root, '..', 'database', 'inventaris.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT kategori FROM Daftar_Kategori")
    kategori_options = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    kategori = st.selectbox("Kategori:", kategori_options)
    
    jumlah = st.number_input("Jumlah:", min_value=1, step=1)
    
    # Tombol untuk mengunggah gambar
    uploaded_file = st.file_uploader("Upload Gambar", type=["jpg", "jpeg", "png"])

    if st.button("Tambahkan"):
        if nama_barang and kategori and jumlah:
            # Panggil fungsi untuk menambahkan item inventaris
            new_item = add_inventory_item(inventory_stack, nama_barang, kategori, jumlah, uploaded_file)
            st.success("Item baru berhasil ditambahkan!")
            st.write("Detail item baru:")
            st.write(new_item)
        else:
            st.warning("Harap isi semua kolom!")
            
# Sidebar dengan informasi anggota Kelompok
st.sidebar.info("Daftar anggota Prodi Sains Data Semester 2")

# Daftar anggota
anggota = [
    ("Natzwa Novena Rantung", "36230026"),
    ("Vania Devina Devara", "36230027"),
    ("Zebina Jhon", "36230028"),
    ("Josia Given Santoso", "36230035"),
    ("Vinsensius Erik Kie", "36230037"),
    ("Fazrina Rahmadhani", "36230039"),
]

# Menampilkan informasi anggota di sidebar dengan bullet points
st.sidebar.markdown("### Daftar Anggota:")
for nama, nim in anggota:
    st.sidebar.markdown(f"- **{nama}** ({nim})")

if __name__ == "__main__":
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    main()
