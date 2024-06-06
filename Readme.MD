# Manajemen Inventaris Barang

**Projek ini bertujuan untuk mengelola inventaris barang dengan beberapa fitur yang berguna.**

## Tutorial Menjalankan Aplikasi

1. Clone repositori ini ke dalam direktori lokal Anda:
    ```bash
    git clone https://github.com/username/manajemen-inventaris-barang.git
    cd manajemen-inventaris-barang
    ```

2. Install semua dependensi yang diperlukan menggunakan `pip`:
    ```bash
    pip install -r requirements.txt
    ```

3. Jalankan aplikasi menggunakan perintah berikut:
    ```bash
    python main.py
    ```

4. Akses aplikasi pada alamat localhost berikut di browser anda:
    ```
    http://localhost:5000
    ```

## Anggota Kelompok
- **Josia Given Santoso**
- **Fazrina Ramadhani**
- **Vania Devina Devara**
- **Vinsensius Erik Kie**
- **Zebina Jhon**
- **Natzwa Novena Rantung**

## Deskripsi Aplikasi
Projek ini bertujuan untuk mengelola inventaris barang dengan beberapa fitur di bawah ini.

## Penjelasan Fitur Aplikasi
1. **Input Inventaris Baru** - Fitur ini memungkinkan pengguna untuk menambahkan barang baru ke dalam inventaris.
    - **Teknologi**: Python, Streamlit, SQLite3
    - **Struktur Data**: Stack
    - **File**: `1_Input_Inventaris_Baru.py`
    - **Path**: `app/pages/1_Input_Inventaris_Baru.py`

2. **Input Inventaris Hilang/Rusak** - Fitur ini memungkinkan pengguna untuk mencatat barang yang hilang atau rusak dalam inventaris.
    - **Teknologi**: Python, Streamlit, SQLite3
    - **Struktur Data**: Stack
    - **File**: `2_Input_Defektif.py`
    - **Path**: `app/pages/2_Input_Defektif.py`

3. **Daftar Kategori** - Fitur ini memungkinkan pengguna untuk melihat daftar kategori inventaris.
    - **Teknologi**: Python, Streamlit, SQLite3
    - **Struktur Data**: Stack
    - **File**: `3_Daftar_Kategori.py`
    - **Path**: `app/pages/3_Daftar_Kategori.py`

4. **Cek Inventaris** - Fitur ini memungkinkan pengguna untuk melihat daftar inventaris yang tersedia.
    - **Teknologi**: Python, Streamlit, SQLite3
    - **Struktur Data**: BST (Binary Search Tree)
    - **File**: `4_Check_Inventaris.py`
    - **Path**: `app/pages/4_Check_Inventaris.py`

5. **Cetak Inventaris** - Fitur ini memungkinkan pengguna untuk mencetak laporan inventaris dalam format CSV.
    - **Teknologi**: Python, Streamlit, SQLite3
    - **Struktur Data**: Queue
    - **File**: `5_Cetak_Inventaris.py`
    - **Path**: `app/pages/5_Cetak_Inventaris.py`

## Struktur Folder Aplikasi

📁 app  
│&nbsp;&nbsp;&nbsp;&nbsp;📁 pages  
│&nbsp;&nbsp;&nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;&nbsp;📄 1_Input_Inventaris_Baru.py  
│&nbsp;&nbsp;&nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;&nbsp;📄 2_Input_Defektif.py  
│&nbsp;&nbsp;&nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;&nbsp;📄 3_Daftar_Kategori.py  
│&nbsp;&nbsp;&nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;&nbsp;📄 4_Check_Inventaris.py  
│&nbsp;&nbsp;&nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;&nbsp;📄 5_Cetak_Inventaris.py  
│&nbsp;&nbsp;&nbsp;&nbsp;📄 Beranda_🏠_.py  
📁 assets  
│&nbsp;&nbsp;&nbsp;&nbsp;📁 app  
│&nbsp;&nbsp;&nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;&nbsp;📄 logo_UBM.png  
│&nbsp;&nbsp;&nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;&nbsp;📄 no-image-placeholder.jpg  
│&nbsp;&nbsp;&nbsp;&nbsp;📁 login-page  
│&nbsp;&nbsp;&nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;&nbsp;📄 abstrac-ba.png  
│&nbsp;&nbsp;&nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;&nbsp;📄 abstract-loop.mp4  
📁 authenticator  
│&nbsp;&nbsp;&nbsp;&nbsp;📁 flask_session  
│&nbsp;&nbsp;&nbsp;&nbsp;📁 templates  
│&nbsp;&nbsp;&nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;&nbsp;📄 login.html  
│&nbsp;&nbsp;&nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;&nbsp;📄 welcome.html  
│&nbsp;&nbsp;&nbsp;&nbsp;📄 app.py  
📁 database  
│&nbsp;&nbsp;&nbsp;&nbsp;📄 create-database.py  
│&nbsp;&nbsp;&nbsp;&nbsp;📄 inventaris.db  
📄 dockerfile  
📄 main.py  
📄 Readme.MD  
📄 requirements.txt  



## Alur Jalannya Software
1. **main.py** ⟶ **authenticator/app.py**: File utama yang dijalankan untuk memulai aplikasi.
    - **Deskripsi**: File utama yang menjalankan aplikasi dan mengarahkan pengguna ke halaman login.

2. **authenticator/app.py** ⟶ **app/Beranda_🏠_.py**: Halaman login aplikasi mengarahkan pengguna ke beranda atau halaman utama aplikasi.
    - **Deskripsi**: Halaman login yang memvalidasi pengguna dan mengarahkannya ke beranda aplikasi.

3. **app/Beranda_🏠_.py** ⟶ **app/pages**: Beranda atau halaman utama aplikasi mengarahkan pengguna ke halaman-halaman aplikasi seperti input data, cek inventaris, dll.
    - **Deskripsi**: Halaman utama aplikasi yang memperkenalkan fitur-fitur utama dan memberikan akses ke halaman-halaman aplikasi lainnya.

4. **app/pages**: Direktori berisi halaman-halaman aplikasi seperti input data, cek inventaris, dll.
    - **Deskripsi**: Direktori yang berisi berbagai halaman aplikasi yang dapat diakses oleh pengguna untuk melakukan berbagai tugas terkait inventaris.

## Penjelasan Database
Database yang digunakan untuk menyimpan data inventaris terdiri dari beberapa tabel:
1. **Daftar Inventaris**: Tabel ini digunakan untuk menyimpan informasi tentang semua barang dalam inventaris.
2. **Users**: Tabel ini digunakan untuk menyimpan informasi tentang pengguna aplikasi.
3. **Inventaris Rusak**: Tabel ini digunakan untuk mencatat barang-barang yang rusak atau hilang.
4. **Daftar Kategori**: Tabel ini digunakan untuk menyimpan daftar kategori barang.
