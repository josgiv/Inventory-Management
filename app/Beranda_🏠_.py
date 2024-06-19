import streamlit as st
from pathlib import Path
import importlib.util

# Set konfigurasi halaman
st.set_page_config(page_title="**Manajemen Inventaris Barang**", page_icon="👋")

# Menambahkan catatan dan informasi tambahan di sidebar
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

# Konfigurasi halaman utama
st.title("**Manajemen Inventaris Barang**")
st.subheader("**Ujian Akhir Semester (UAS) - Struktur Data**")
st.write("___")

# Deskripsi Aplikasi
st.subheader("**Deskripsi Aplikasi**:")
st.write("**Projek ini bertujuan untuk mengelola inventaris barang dengan beberapa fitur dibawah ini.")

# Penjelasan Fitur Aplikasi
st.subheader("**Penjelasan Fitur Aplikasi**:")
st.write("\n")
st.write("**1. Input Inventaris Baru** - Fitur ini memungkinkan pengguna untuk menambahkan barang baru ke dalam inventaris.")
st.write("    - **Teknologi**: Python, Streamlit, SQLite3")
st.write("    - **Struktur Data**: Stack")
st.write("    - **File**: `1_Input_Inventaris_Baru.py`")
st.write("    - **Path**: `app/pages/1_Input_Inventaris_Baru.py`")
st.write("**2. Input Inventaris Hilang/Rusak** - Fitur ini memungkinkan pengguna untuk mencatat barang yang hilang atau rusak dalam inventaris.")
st.write("    - **Teknologi**: Python, Streamlit, SQLite3")
st.write("    - **Struktur Data**: Stack")
st.write("    - **File**: `2_Input_Defektif.py`")
st.write("    - **Path**: `app/pages/2_Input_Defektif.py`")
st.write("**3. Daftar Kategori** - Fitur ini memungkinkan pengguna untuk melihat daftar kategori inventaris.")
st.write("    - **Teknologi**: Python, Streamlit, SQLite3")
st.write("    - **Struktur Data**: Stack")
st.write("    - **File**: `3_Daftar_Kategori.py`")
st.write("    - **Path**: `app/pages/3_Daftar_Kategori.py`")
st.write("**4. Cek Inventaris** - Fitur ini memungkinkan pengguna untuk melihat daftar inventaris yang tersedia.")
st.write("    - **Teknologi**: Python, Streamlit, SQLite3")
st.write("    - **Struktur Data**: BST (Binary Search Tree)")
st.write("    - **File**: `4_Check_Inventaris.py`")
st.write("    - **Path**: `app/pages/4_Check_Inventaris.py`")
st.write("**5. Cetak Inventaris** - Fitur ini memungkinkan pengguna untuk mencetak laporan inventaris dalam format CSV.")
st.write("    - **Teknologi**: Python, Streamlit, SQLite3")
st.write("    - **Struktur Data**: Queue")
st.write("    - **File**: `5_Cetak_Inventaris.py`")
st.write("    - **Path**: `app/pages/5_Cetak_Inventaris.py`")

# Struktur Folder Aplikasi'
st.write("___")
st.subheader("**Struktur Folder Aplikasi**")
st.write("\n")
st.text("📁 app")
st.text("│   📁 pages")
st.text("│   │   📄 1_Input_Inventaris_Baru.py")
st.text("│   │   📄 2_Input_Defektif.py")
st.text("│   │   📄 3_Daftar_Kategori.py")
st.text("│   │   📄 4_Check_Inventaris.py")
st.text("│   │   📄 5_Cetak_Inventaris.py")
st.text("│   📄 Beranda_🏠_.py")
st.text("📁 assets")
st.text("📁 authenticator")
st.text("│   📁 flask_session")
st.text("│   📁 templates")
st.text("│   │   📄 login.html")
st.text("│   │   📄 welcome.html")
st.text("│   📄 app.py")
st.text("📁 database")
st.text("│   📄 create-database.py")
st.text("│   📄 inventaris.db")
st.text("📄 main.py")
st.text("📄 requirements.txt")

# Alur Jalannya Software
st.write("___")
st.subheader("**Alur Jalannya Software**:")
st.write("\n")
# main.py -> authenticator/app.py
st.write("**1. main.py** ⟶ **authenticator/app.py**: File utama yang dijalankan untuk memulai aplikasi.")
st.write("    - **Deskripsi**: File utama yang menjalankan aplikasi dan mengarahkan pengguna ke halaman login.")

# authenticator/app.py -> app/Beranda_🏠_.py
st.write("**2. authenticator/app.py** ⟶ **app/Beranda_🏠_.py**: Halaman login aplikasi mengarahkan pengguna ke beranda atau halaman utama aplikasi.")
st.write("    - **Deskripsi**: Halaman login yang memvalidasi pengguna dan mengarahkannya ke beranda aplikasi.")

# app/Beranda_🏠_.py -> app/pages
st.write("**3. app/Beranda_🏠_.py** ⟶ **app/pages**: Beranda atau halaman utama aplikasi mengarahkan pengguna ke halaman-halaman aplikasi seperti input data, cek inventaris, dll.")
st.write("    - **Deskripsi**: Halaman utama aplikasi yang memperkenalkan fitur-fitur utama dan memberikan akses ke halaman-halaman aplikasi lainnya.")

# app/pages
st.write("**4. app/pages**: Direktori berisi halaman-halaman aplikasi seperti input data, cek inventaris, dll.")
st.write("    - **Deskripsi**: Direktori yang berisi berbagai halaman aplikasi yang dapat diakses oleh pengguna untuk melakukan berbagai tugas terkait inventaris.")

# Penjelasan Database
st.write("___")
st.subheader("**Penjelasan Database**:")
st.write("\n")
st.write("Database yang digunakan untuk menyimpan data inventaris terdiri dari beberapa tabel:")
st.write("1. **Daftar Inventaris**: Tabel ini digunakan untuk menyimpan informasi tentang semua barang dalam inventaris.")
st.write("2. **Users**: Tabel ini digunakan untuk menyimpan informasi tentang pengguna aplikasi.")
st.write("3. **Inventaris Rusak**: Tabel ini digunakan untuk mencatat barang-barang yang rusak atau hilang.")
st.write("4. **Daftar Kategori**: Tabel ini digunakan untuk menyimpan daftar kategori barang.")
