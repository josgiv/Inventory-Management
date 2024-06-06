import sqlite3

# Fungsi untuk membuat koneksi ke database
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("Koneksi ke database berhasil: SQLite version", sqlite3.version)
    except sqlite3.Error as e:
        print(e)
    return conn

# Fungsi untuk membuat tabel Daftar Inventaris
def create_table_daftar_inventaris(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Daftar_Inventaris (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tanggal TEXT,
                nama_barang TEXT,
                kategori TEXT,
                jumlah INTEGER,
                gambar BLOB
            )
        """)
        print("Tabel Daftar Inventaris berhasil dibuat.")
    except sqlite3.Error as e:
        print(e)

# Fungsi untuk membuat tabel Inventaris Rusak
def create_table_inventaris_rusak(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Inventaris_Rusak (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tanggal TEXT,
                nama_barang TEXT,
                kategori TEXT,
                jumlah INTEGER,
                alasan TEXT,
                gambar BLOB
            )
        """)
        print("Tabel Inventaris Rusak berhasil dibuat.")
    except sqlite3.Error as e:
        print(e)

# Fungsi untuk membuat tabel Users
def create_table_users(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        """)
        print("Tabel Users berhasil dibuat.")
    except sqlite3.Error as e:
        print(e)

# Fungsi untuk membuat tabel Daftar Kategori
def create_table_daftar_kategori(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Daftar_Kategori (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                kategori TEXT NOT NULL UNIQUE
            )
        """)
        print("Tabel Daftar Kategori berhasil dibuat.")
    except sqlite3.Error as e:
        print(e)

# Fungsi utama
def main():
    database = "database/inventaris.db"

    # Membuat koneksi ke database
    conn = create_connection(database)

    if conn is not None:
        # Membuat tabel-tabel jika belum ada
        create_table_daftar_inventaris(conn)
        create_table_inventaris_rusak(conn)
        create_table_users(conn)
        create_table_daftar_kategori(conn)

        # Menutup koneksi ke database
        conn.close()
    else:
        print("Koneksi ke database gagal.")

if __name__ == "__main__":
    main()
