import streamlit as st
import sqlite3
import pandas as pd
import queue
import os
import subprocess

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from PyPDF2 import PdfMerger

st.set_page_config(page_title="Cetak Daftar Inventaris", page_icon="📃")

class ExportManager:
    def __init__(self):
        self.export_queue = queue.Queue()

    def add_to_queue(self, table_name, table_data, pdf_file_path):
        self.export_queue.put((table_name, table_data, pdf_file_path))

    def process_queue(self):
        while not self.export_queue.empty():
            table_name, table_data, pdf_file_path = self.export_queue.get()
            export_table_to_pdf(table_name, table_data, pdf_file_path)
            self.export_queue.task_done()

def fetch_data_from_table(table_name):
    db_path = os.path.join(os.path.dirname(__file__), '..', '..', 'database', 'inventaris.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    data = cursor.fetchall()
    conn.close()
    return data

def export_table_to_pdf(table_name, table_data, pdf_file_path):
    doc = SimpleDocTemplate(pdf_file_path, pagesize=letter)
    elements = []

    logo_path = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'logo-UBM.png')
    logo = Image(logo_path, width=1.5 * inch, height=0.75 * inch)
    logo.hAlign = 'CENTER'
    elements.append(logo)

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('Title', parent=styles['Title'], fontName='Helvetica-Bold', fontSize=18, textColor=colors.black, spaceAfter=14, alignment=1)
    normal_style = ParagraphStyle('Normal', parent=styles['Normal'], fontName='Helvetica', fontSize=12, textColor=colors.black, spaceAfter=14)

    title = Paragraph(f"<b>PT Bapak Maju Bersamaa</b><br/><br/><b>{table_name.replace('_', ' ')}</b>", title_style)
    elements.append(title)
    elements.append(Spacer(1, 12))

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

def add_footer(canvas, doc):
    canvas.saveState()
    styles = getSampleStyleSheet()
    footer_style = ParagraphStyle('Footer', parent=styles['Normal'], fontName='Helvetica', fontSize=10, textColor=colors.black, spaceAfter=14, alignment=0)
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
    export_manager = ExportManager()

    st.sidebar.title("Anggota Kelompok:")
    st.sidebar.write("- Josia Given Santoso", unsafe_allow_html=True)
    st.sidebar.write("- Fazrina Ramadhani", unsafe_allow_html=True)
    st.sidebar.write("- Vania Devina Devara", unsafe_allow_html=True)
    st.sidebar.write("- Vinsensius Erik Kie", unsafe_allow_html=True)
    st.sidebar.write("- Zebina Jhon", unsafe_allow_html=True)
    st.sidebar.write("- Natzwa Rantung", unsafe_allow_html=True)

    st.title("Laporan Inventaris")

    tables = ["Daftar_Inventaris", "Inventaris_Rusak"]
    pdf_file_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'reports')
    os.makedirs(pdf_file_dir, exist_ok=True)
    pdf_file_paths = []

    for table in tables:
        table_data = fetch_data_from_table(table)
        column_count = len(table_data[0]) if table_data else 0

        if column_count == 6:
            columns = ["ID", "Tanggal Masuk", "Nama", "Kategori", "Stock", "Status"]
        elif column_count == 5:
            columns = ["ID", "Tanggal Masuk", "Nama", "Kategori", "Status"]
        else:
            st.error(f"Unexpected column count ({column_count}) for table {table}")
            continue

        df = pd.DataFrame(table_data, columns=columns)
        st.write(f"Data untuk {table.replace('_', ' ')}")
        st.dataframe(df)

        if st.button(f"Export {table.replace('_', ' ')} to PDF", key=f"export_{table}"):
            pdf_file_path = os.path.join(pdf_file_dir, f'{table}.pdf')
            export_manager.add_to_queue(table, table_data, pdf_file_path)
            pdf_file_paths.append(pdf_file_path)
            st.success(f"File {pdf_file_path} telah ditambahkan ke dalam antrian untuk diekspor.")
            export_manager.process_queue()

            with open(pdf_file_path, "rb") as pdf_file:
                st.download_button(label=f"Download {table.replace('_', ' ')} PDF", data=pdf_file, file_name=f"{table}.pdf", mime="application/pdf")

    if len(pdf_file_paths) > 1:
        if st.button("Gabungkan semua PDF"):
            merged_pdf_file_path = os.path.join(pdf_file_dir, 'merged_invoice_report.pdf')
            merge_pdfs(pdf_file_paths, merged_pdf_file_path)
            st.success(f"Semua faktur telah digabungkan menjadi satu dan diekspor ke {merged_pdf_file_path}")
            with open(merged_pdf_file_path, "rb") as merged_pdf:
                st.download_button(label="Download Merged PDF", data=merged_pdf, file_name="merged_invoice_report.pdf", mime="application/pdf")

    if st.button("Proses Antrian Ekspor"):
        export_manager.process_queue()
        st.success("Semua file dalam antrian telah diproses.")

if __name__ == "__main__":
    main()
