import os
import sqlite3
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Menu Cek Inventaris", page_icon="📝")

# Definisikan kelas TreeNode untuk struktur data BST
class TreeNode: 
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

# Definisikan kelas BST untuk menyimpan dan mengelola data inventaris
class BST:
    def __init__(self):
        self.root = None

    def insert(self, data):
        if not self.root:
            self.root = TreeNode(data)
        else:
            self._insert_recursive(self.root, data)

    def _insert_recursive(self, node, data):
        if data[0] < node.data[0]:
            if node.left:
                self._insert_recursive(node.left, data)
            else:
                node.left = TreeNode(data)
        else:
            if node.right:
                self._insert_recursive(node.right, data)
            else:
                node.right = TreeNode(data)

    def inorder_traversal(self, node):
        if node:
            self.inorder_traversal(node.left)
            row_data = [str(item) for item in node.data]
            st.write(" | ".join(row_data))
            self.inorder_traversal(node.right)

# Fungsi untuk menampilkan daftar inventaris dalam bentuk tabel
def show_inventory_table(cursor):
    cursor.execute("SELECT * FROM Daftar_Inventaris")
    inventaris = cursor.fetchall()

    st.write("\n### Data Inventaris\n")
    df_inventaris = pd.DataFrame(inventaris, columns=["ID", "Nama Barang", "Kategori", "Stok", "Tanggal"])
    st.write(df_inventaris.to_html(index=False, classes=["styled-table"], escape=False), unsafe_allow_html=True)

# Fungsi untuk menampilkan daftar barang rusak/hilang dalam bentuk tabel
# Fungsi untuk menampilkan daftar barang rusak/hilang dalam bentuk tabel
def show_defective_table(cursor):
    cursor.execute("SELECT * FROM Inventaris_Rusak")
    defective = cursor.fetchall()

    st.write("\n### Data Barang Rusak/Hilang\n")
    df_defective = pd.DataFrame(defective, columns=["ID", "Nama Barang", "Kategori", "Stok", "Tanggal", "Alasan"])
    
    # Hitung panjang maksimum antara tabel inventaris dan tabel barang rusak/hilang
    max_length = max(len(defective), len(defective))
    
    # Tambahkan baris kosong jika panjang tabel inventaris rusak/hilang lebih pendek
    if len(defective) < max_length:
        empty_rows = pd.DataFrame([[""] * len(df_defective.columns)] * (max_length - len(inventaris)), columns=df_defective.columns) # type: ignore
        df_defective = pd.concat([df_defective, empty_rows], ignore_index=True)
    
    st.write(df_defective.to_html(index=False, classes=["styled-table"], escape=False), unsafe_allow_html=True)


# Fungsi untuk menampilkan semua tabel
def show_all_tables():
    # Dapatkan path dari direktori saat ini
    current_dir = os.path.abspath(os.path.dirname(__file__))
    
    # Ganti ke direktori tempat file database berada
    os.chdir(current_dir)

    # Koneksi ke database SQLite
    db_path = os.path.join(current_dir, '..', '..', 'database', 'inventaris.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Tampilkan daftar inventaris
    show_inventory_table(cursor)
    st.write("\n---\n")  # Divider antar tabel

    # Tampilkan daftar barang rusak/hilang
    show_defective_table(cursor)

    # Tutup koneksi database
    conn.close()

# Main Page
def main():
    st.title("Daftar Inventaris PT Bapak Maju Terus")
    st.markdown("""
    Aplikasi ini menampilkan daftar inventaris PT Bapak Maju Terus, termasuk barang-barang yang rusak atau hilang.
    """)
    show_all_tables()

# Sidebar dengan tombol "Home" dan daftar anggota kelompok
    
st.sidebar.title("Anggota Kelompok:")
st.sidebar.write('\n')
st.sidebar.write("- Josia Given Santoso", unsafe_allow_html=True)
st.sidebar.write("- Fazrina Ramadhani", unsafe_allow_html=True)
st.sidebar.write("- Vania Devina Devara", unsafe_allow_html=True)
st.sidebar.write("- Vinsensius Erik Kie", unsafe_allow_html=True)
st.sidebar.write("- Zebina Jhon", unsafe_allow_html=True)
st.sidebar.write("- Natzwa", unsafe_allow_html=True)

# Jalankan aplikasi
if __name__ == "__main__":
    main()
