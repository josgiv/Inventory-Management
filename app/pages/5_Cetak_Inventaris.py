import os
import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, PageBreak
from reportlab.lib import colors
from reportlab.lib.units import inch
import sqlite3
from PyPDF2 import PdfMerger
from io import BytesIO
from PIL import Image as PILImage
from queue import Queue
import threading

# Path untuk aset
ASSETS_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'app')
DEFAULT_IMAGE_PATH = os.path.join(ASSETS_DIR, 'no-image-placeholder.jpg')  # Placeholder image
db_path_cetak = os.path.join(os.path.dirname(__file__), '..', '..',  'database', 'inventaris.db')

def get_image_from_blob(blob_data):
    if blob_data:
        image = PILImage.open(BytesIO(blob_data))
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)
        return buffer
    else:
        return None

def create_pdf(file_buffer, inventaris_data, title, is_damaged=False):
    # Menyiapkan dokumen PDF
    doc = SimpleDocTemplate(file_buffer, pagesize=A4)
    elements = []
    
    # Path ke logo UBM
    logo_path = os.path.join(ASSETS_DIR, 'logo_ubm.png')

    # Menambahkan logo UBM
    ubm_logo = Image(logo_path, width=80, height=60)
    elements.append(ubm_logo)

    # Menambahkan jarak antara logo dan judul
    elements.append(Table([[" "]], colWidths=[6 * inch]))
    elements[-1].setStyle(TableStyle([
        ('BOTTOMPADDING', (0, 0), (-1, -1), 20),
    ]))

    # Menambahkan judul
    elements.append(Table([[title]], colWidths=[6 * inch]))
    elements[-1].setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 20),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12), 
    ]))

    # Menambahkan jarak antara judul dan tabel
    elements.append(Table([[" "]], colWidths=[6 * inch]))
    elements[-1].setStyle(TableStyle([
        ('BOTTOMPADDING', (0, 0), (-1, -1), 20),  
    ]))

    # Menambahkan tabel inventaris
    table_data = [['ID', 'Tanggal', 'Nama Barang', 'Kategori', 'Jumlah', 'Alasan' if is_damaged else 'Foto']]
    for row in inventaris_data:
        image_buffer = get_image_from_blob(row[-1]) if not is_damaged else None
        if image_buffer:
            image = Image(image_buffer, width=50, height=50)
        else:
            image = Image(DEFAULT_IMAGE_PATH, width=50, height=50)
        table_data.append(list(row[:-1]) + [image])

    table = Table(table_data, colWidths=[inch]*7)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),  # Warna teks hitam
    ]))
    
    elements.append(table)
    doc.build(elements)
    file_buffer.seek(0)


# Fungsi untuk membuat PDF Daftar Inventaris
def create_inventory_pdf():
    # Koneksi ke database SQLite
    conn = sqlite3.connect(db_path_cetak)
    cursor = conn.cursor()

    # Query untuk mengambil data dari tabel Daftar_Inventaris
    cursor.execute("SELECT ID, tanggal, nama_barang, kategori, jumlah, gambar FROM Daftar_Inventaris")
    inventaris_data = cursor.fetchall()

    # Menyiapkan file PDF dalam memori
    buffer = BytesIO()
    create_pdf(buffer, inventaris_data, "Inventaris CV. Di Lobby Terus")
    return buffer

# Fungsi untuk membuat PDF Inventaris Rusak
def create_damaged_inventory_pdf():
    # Koneksi ke database SQLite
    conn = sqlite3.connect(db_path_cetak)
    cursor = conn.cursor()

    # Query untuk mengambil data dari tabel Inventaris_Rusak
    cursor.execute("SELECT ID, tanggal, nama_barang, kategori, jumlah, alasan, gambar FROM Inventaris_Rusak")
    inventaris_rusak_data = cursor.fetchall()

    # Menyiapkan file PDF dalam memori
    buffer = BytesIO()
    create_pdf(buffer, inventaris_rusak_data, "Inventaris Rusak CV. Di Lobby Terus", is_damaged=True)
    return buffer

# Fungsi untuk membuat PDF gabungan
def create_combined_pdf(queue):
    # Membuat PDF Daftar Inventaris
    inventory_pdf = create_inventory_pdf()
    # Membuat PDF Inventaris Rusak
    damaged_inventory_pdf = create_damaged_inventory_pdf()

    # Menggabungkan kedua PDF dalam memori
    combined_buffer = BytesIO()
    pdf_merger = PdfMerger()
    pdf_merger.append(inventory_pdf)
    pdf_merger.append(damaged_inventory_pdf)
    pdf_merger.write(combined_buffer)
    pdf_merger.close()

    # Menambahkan hasil ke queue
    queue.put(combined_buffer)

def main():
    # Menjalankan aplikasi
    st.title("Cetak Laporan Inventaris CV. Di Lobby Terus")

    st.subheader("Daftar Inventaris")
    inventory_pdf = create_inventory_pdf()
    st.download_button(
        label="Download PDF Daftar Inventaris",
        data=inventory_pdf,
        file_name="Daftar_Inventaris.pdf",
        mime="application/pdf"
    )

    st.subheader("Inventaris Rusak")
    damaged_inventory_pdf = create_damaged_inventory_pdf()
    st.download_button(
        label="Download PDF Inventaris Rusak",
        data=damaged_inventory_pdf,
        file_name="Inventaris_Rusak.pdf",
        mime="application/pdf"
    )

    st.subheader("Laporan Inventaris Barang CV. Di Lobby Terus")
    queue = Queue()  # Membuat queue untuk menyimpan hasil PDF gabungan

    # Fungsi untuk menghasilkan PDF gabungan dan menambahkannya ke dalam queue
    def generate_combined_pdf():
        create_combined_pdf(queue)

    # Menjalankan fungsi untuk menghasilkan PDF gabungan secara asinkron
    thread = threading.Thread(target=generate_combined_pdf)
    thread.start()

    # Menunggu hasil dari queue
    combined_pdf = queue.get()
    st.download_button(
        label="Download PDF gabungan",
        data=combined_pdf,
        file_name="Laporan_Inventaris_CV_Di_Lobby_Terus.pdf",
        mime="application/pdf"
    )

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
    main()
