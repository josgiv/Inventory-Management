import os
import sqlite3
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Input Defektif", page_icon="🥡")

# Class untuk stack inventaris
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

# Fungsi untuk menambahkan barang rusak/hilang ke dalam database
def add_defective_item(id, nama_barang, jumlah, alasan):
    # Koneksi ke database SQLite
    db_path = os.path.join(project_root, 'database', 'inventaris.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Tanggal saat ini
    tanggal = datetime.now().strftime("%Y-%m-%d")

    # Ambil stok saat ini
    cursor.execute("SELECT jumlah FROM Daftar_Inventaris WHERE id = ?", (id,))
    current_stock = cursor.fetchone()[0]

    # Jika jumlah yang diminta melebihi stok saat ini, tampilkan pesan kesalahan
    if jumlah > current_stock:
        st.error("Jumlah yang diminta melebihi stok saat ini.")
        return

    # Tambahkan item ke tabel Inventaris_Rusak
    cursor.execute("""
        INSERT INTO Inventaris_Rusak (tanggal, nama_barang, jumlah, alasan)
        VALUES (?, ?, ?, ?)
    """, (tanggal, nama_barang, jumlah, alasan))

    # Update jumlah barang di Daftar_Inventaris
    cursor.execute("""
        UPDATE Daftar_Inventaris
        SET jumlah = jumlah - ?
        WHERE id = ?
    """, (jumlah, id))

    conn.commit()
    st.success("Barang berhasil ditambahkan ke daftar barang rusak/hilang.")

    # Tutup koneksi database
    conn.close()


# Fungsi utama untuk menampilkan UI dan menambahkan/barang rusak/hilang
def main():
    # Judul halaman
    st.title("Input Barang Rusak atau Hilang")

    # Gradient putih pada halaman
    st.markdown(
        """
        <style>
            body {
                background: linear-gradient(to bottom, #ffffff, #ffffff);
            }
            .btn-primary {
                background-color: #0066cc;
                color: #ffffff;
                border-radius: 5px;
                padding: 10px 20px;
                cursor: pointer;
            }
            .btn-primary:hover {
                background-color: #0052a3;
            }
            .checkbox {
                padding: 10px 0;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Buat instance InventoryStack
    inventory_stack = InventoryStack()

    # Koneksi ke database SQLite
    db_path = os.path.join(project_root, 'database', 'inventaris.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Ambil daftar inventaris dari database
    cursor.execute("SELECT id, nama_barang, jumlah FROM Daftar_Inventaris")
    items = cursor.fetchall()
    item_options = {f"ID : {item[0]} - Nama Barang : {item[1]} (Stok: {item[2]})": (item[0], item[1]) for item in items}

    # Input form untuk memilih barang
    selected_item = st.selectbox("Pilih Barang:", options=list(item_options.keys()))

    # Ambil id dan nama barang yang dipilih
    selected_id, nama_barang = item_options[selected_item]

    # Input form untuk jumlah dan alasan
    jumlah = st.number_input("Jumlah Inventaris Rusak/Hilang:", min_value=1, step=1)
    alasan = st.selectbox("Alasan:", options=["Rusak", "Hilang"])

    # Tombol untuk menambahkan barang rusak/hilang
    if st.button("Tambahkan", key="tambahkan_button"):
        if selected_id and jumlah and alasan:
            inventory_stack.push((selected_id, nama_barang, jumlah, alasan))
            add_defective_item(selected_id, nama_barang, jumlah, alasan)
        else:
            st.warning("Harap lengkapi semua kolom!")

    # Menampilkan detail barang yang ditambahkan rusak atau hilang dalam format JSON
    if st.checkbox("Tampilkan Detail Barang yang Ditambahkan", key="detail_checkbox"):
        if not inventory_stack.is_empty():
            detail_barang = inventory_stack.items[-1]
            detail_dict = {
                "ID Barang": detail_barang[0],
                "Nama Barang": detail_barang[1],
                "Jumlah": detail_barang[2],
                "Alasan": detail_barang[3]
            }
            st.json(detail_dict)
        else:
            st.info("Tidak ada barang yang ditambahkan rusak atau hilang.")

    # Tutup koneksi database
    conn.close()

if __name__ == "__main__":
    # Dapatkan path dari direktori utama
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

    # Jalankan aplikasi utama
    main()
