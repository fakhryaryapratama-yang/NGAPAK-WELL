import os
import sqlite3
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

DB_FILE = "kas_takmir.db"
FILE_PDF = "laporan_kas_takmir.pdf"

# ===============================
# FORMAT & INPUT RUPIAH
# ===============================
def format_rupiah(angka):   
    return f"Rp {angka:,}".replace(",", ".")

def input_rupiah(prompt):
    while True:
        try:
            nilai = input(prompt)
            nilai_bersih = nilai.replace(".", "").replace(",", "")
            return int(nilai_bersih)
        except ValueError:
            print("❌ Masukkan angka yang benar! Contoh: 100.000")
