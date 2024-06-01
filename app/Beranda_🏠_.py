import streamlit as st
from pathlib import Path
import importlib.util

# Set konfigurasi halaman
st.set_page_config(page_title="Manajemen Inventaris Barang", page_icon="👋")

# Menampilkan anggota kelompok di sidebar
st.sidebar.title("Anggota Kelompok:")
st.sidebar.write('- Josia Given Santoso')
st.sidebar.write('- Fazrina Ramadhani')
st.sidebar.write('- Vania Devina Devara')
st.sidebar.write('- Vinsensius Erik Kie')
st.sidebar.write('- Zebina Jhon')
st.sidebar.write('- Natzwa')

# Konfigurasi halaman utama
st.title("Manajemen Inventaris Barang")
st.subheader("Ujian Akhir Semester (UAS) - Struktur Data")
st.write('\n')
st.write('\n')
st.subheader("Kelompok 1 - Universitas Bunda Mulia")
st.write('\n')
st.markdown("Projek ini bertujuan untuk mengelola inventaris barang dengan beberapa fitur dibawah ini. Silakan pilih opsi di bawah ini:\n")
st.write('\n')
st.write('\n')
st.markdown("### Fitur Aplikasi:")

st.write("1. **Input Inventaris Baru** - Menambahkan barang baru ke dalam inventaris.")
st.write("2. **Input Inventaris Hilang/Rusak** - Melakukan pencatatan barang yang hilang atau rusak.")
st.write("3. **Cek Inventaris** - Melihat daftar inventaris yang tersedia.")
st.write("4. **Export CSV Laporan Inventaris** - Mengunduh laporan inventaris dalam format CSV.")
st.write("5. **Informasi Kelompok** - Menampilkan informasi tentang kelompok pengembang aplikasi.")
st.write("6. **Keluar** - Keluar dari program.")
