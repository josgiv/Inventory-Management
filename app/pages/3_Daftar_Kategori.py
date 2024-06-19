import streamlit as st
import sqlite3
import os
import pandas as pd

# Definisikan class Stack
class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return None

    def is_empty(self):
        return len(self.items) == 0

    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        return None

# Mendeklarasikan jalur basis data secara relatif dari lokasi skrip
db_path_kategori = os.path.join(os.path.dirname(__file__), '..', '..', 'database', 'inventaris.db')

# Inisialisasi session state untuk menyimpan daftar kategori sebagai stack
if 'categories' not in st.session_state:
    st.session_state['categories'] = Stack()

# Fungsi untuk memeriksa keberadaan tabel
def table_exists():
    try:
        conn = sqlite3.connect(db_path_kategori)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Daftar_Kategori';")
        exists = cursor.fetchone() is not None
        conn.close()
        return exists
    except sqlite3.Error as e:
        st.error(f"Error checking table: {e}")
        return False

# Fungsi untuk menambahkan kategori baru ke database
def add_category_to_db(category):
    try:
        conn = sqlite3.connect(db_path_kategori)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Daftar_Kategori (kategori) VALUES (?)", (category,))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False
    except sqlite3.Error as e:
        st.error(f"Database error: {e}")
        return False

# Fungsi untuk menghapus kategori berdasarkan ID
def delete_category_by_id(category_id):
    try:
        conn = sqlite3.connect(db_path_kategori)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Daftar_Kategori WHERE id=?", (category_id,))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        st.error(f"Error deleting category: {e}")
        return False

# Fungsi untuk menambahkan kategori baru
def add_category():
    new_category = st.text_input("Masukkan Kategori Baru", key='new_category')
    if st.button("Tambah Kategori"):
        if new_category:
            if table_exists():
                if add_category_to_db(new_category):
                    st.session_state['categories'].push(new_category)
                    st.success(f'Kategori "{new_category}" berhasil ditambahkan!')
                else:
                    st.warning(f'Kategori "{new_category}" sudah ada di database.')
            else:
                st.error("Tabel 'Daftar_Kategori' tidak ditemukan dalam database.")
        else:
            st.error("Nama kategori tidak boleh kosong.")

# Fungsi untuk mengambil dan menampilkan daftar kategori dalam bentuk tabel
def show_categories():
    st.write("___")
    st.subheader("Daftar Kategori")
    try:
        conn = sqlite3.connect(db_path_kategori)
        cursor = conn.cursor()
        cursor.execute("SELECT id, kategori FROM Daftar_Kategori")
        rows = cursor.fetchall()
        
        if rows:
            df = pd.DataFrame(rows, columns=['ID', 'Nama Kategori'])
            st.markdown(df.to_html(index=False), unsafe_allow_html=True)

            # Dropdown untuk menghapus kategori berdasarkan ID
            st.write("___")
            delete_id = st.selectbox("Pilih ID untuk menghapus kategori:", df['ID'].tolist())
            if st.button("Hapus Kategori"):
                if delete_category_by_id(delete_id):
                    st.success(f'Kategori dengan ID {delete_id} berhasil dihapus.')
                else:
                    st.error(f'Gagal menghapus kategori dengan ID {delete_id}.')
                
                # Perbarui tampilan setelah penghapusan
                cursor.execute("SELECT id, kategori FROM Daftar_Kategori")
                updated_rows = cursor.fetchall()
                if updated_rows:
                    updated_df = pd.DataFrame(updated_rows, columns=['ID', 'Nama Kategori'])
                    st.markdown(updated_df.to_html(index=False), unsafe_allow_html=True)
                    st.session_state['categories'] = Stack()
                    for row in updated_rows:
                        st.session_state['categories'].push(row[1])
                else:
                    st.write("Belum ada kategori yang ditambahkan.")
        else:
            st.write("Belum ada kategori yang ditambahkan.")

        conn.close()
    except sqlite3.Error as e:
        st.error(f"Error fetching categories: {e}")

# Fungsi utama
def main():
    st.title("Manajemen Kategori")
    
    # Deskripsi aplikasi
    st.write("""
    Selamat datang di aplikasi Manajemen Kategori! 
    Aplikasi ini memungkinkan Anda untuk menambahkan, menampilkan, dan menghapus kategori dalam database inventaris Anda.
    Berikut adalah fitur utama aplikasi ini:
    - **Tambah Kategori**: Menambahkan kategori baru ke dalam database.
    - **Tampilkan Kategori**: Menampilkan daftar kategori yang sudah ada dalam database.
    - **Hapus Kategori**: Menghapus kategori berdasarkan ID yang dipilih.
    """)

    # Tambah kategori
    add_category()

    # Tampilkan daftar kategori dari database
    show_categories()
    
    # Sidebar dengan informasi anggota
st.sidebar.title("Daftar Anggota")

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

# Menampilkan informasi anggota di sidebar 
st.sidebar.markdown("### Daftar Anggota:")
for nama, nim in anggota:
    st.sidebar.markdown(f"- **{nama}** ({nim})")

if __name__ == "__main__":
    main()
