import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import os
import sqlite3
from PyPDF2 import PdfMerger

def fetch_data_from_table(table_name):
    # Koneksi ke database SQLite
    db_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'inventaris.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Ambil data dari database
    cursor.execute(f"SELECT * FROM {table_name}")
    data = cursor.fetchall()

    # Tutup koneksi database
    conn.close()

    return data

def export_table_to_pdf(table_name, table_data, pdf_file_path):
    doc = SimpleDocTemplate(pdf_file_path, pagesize=letter)
    elements = []

    # Tambahkan logo dan judul
    logo_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'logo-UBM.png')
    logo = Image(logo_path, width=1.5*inch, height=0.75*inch)
    logo.hAlign = 'CENTER'
    elements.append(logo)

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Title'],
        fontName='Helvetica-Bold',
        fontSize=18,
        textColor=colors.black,
        spaceAfter=14,
        alignment=1  # Center alignment
    )
    normal_style = ParagraphStyle(
        'Normal',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        textColor=colors.black,
        spaceAfter=14
    )
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        textColor=colors.black,
        spaceAfter=14,
        alignment=0  # Left alignment
    )
    
    title = Paragraph(f"<b>PT Bapak Maju Bersamaa</b><br/><br/><b>{table_name.replace('_', ' ')}</b>", title_style)
    elements.append(title)
    elements.append(Spacer(1, 12))  # Tambahkan baris kosong

    # Data tabel
    header = ["ID", "Tanggal Masuk", "Nama", "Kategori", "Stock", "Status"]
    data = [header]
    data.extend(table_data)
    
    table = Table(data, colWidths=[0.5 * inch, 1.5 * inch, 2 * inch, 1.5 * inch, 0.7 * inch, 1 * inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F3BB44')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 12))
    elements.append(PageBreak())

    doc.build(elements, onFirstPage=add_footer, onLaterPages=add_footer)
    print(f"{table_name} telah diekspor ke {pdf_file_path}")

def add_footer(canvas, doc):
    canvas.saveState()
    styles = getSampleStyleSheet()
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        textColor=colors.black,
        spaceAfter=14,
        alignment=0  # Left alignment
    )
    footer = Paragraph("<b>PT Bapak Maju Bersamaa</b>", footer_style)
    width, height = letter
    footer.wrapOn(canvas, width, height)
    footer.drawOn(canvas, 0.5 * inch, 0.5 * inch)
    canvas.restoreState()

def merge_pdfs(input_paths, output_path):
    merger = PdfMerger()
    for path in input_paths:
        merger.append(path)
    merger.write(output_path)
    merger.close()

def main():
    tables = ["Daftar_Inventaris", "Inventaris_Rusak"]
    pdf_file_dir = os.path.join(os.path.dirname(__file__), '..', 'report')
    os.makedirs(pdf_file_dir, exist_ok=True)
    pdf_file_paths = []

    for table in tables:
        table_data = fetch_data_from_table(table)
        pdf_file_path = os.path.join(pdf_file_dir, f'{table}.pdf')
        export_table_to_pdf(table, table_data, pdf_file_path)
        pdf_file_paths.append(pdf_file_path)

    # Gabungkan semua file PDF menjadi satu file
    merged_pdf_file_path = os.path.join(pdf_file_dir, 'merged_invoice_report.pdf')
    merge_pdfs(pdf_file_paths, merged_pdf_file_path)
    print(f"Semua faktur telah digabungkan menjadi satu dan diekspor ke {merged_pdf_file_path}")

if __name__ == "__main__":
    main()
