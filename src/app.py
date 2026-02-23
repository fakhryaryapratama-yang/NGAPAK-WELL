# ===============================
# IMPORT (dari import.py)
# ===============================
import os
import sqlite3
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

DB_FILE = "kasnya.db"
FILE_PDF = "laporan_kas_takmir.pdf"


def get_tanggal_sekarang():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def input_rupiah(prompt):
    while True:
        try:
            nilai = input(prompt).strip()
            
            if not nilai:
                print("❌ Input tidak boleh kosong!")
                continue

            nilai_bersih = (
                nilai.replace("Rp", "")
                    .replace("rp", "")
                    .replace(".", "")
                    .replace(",", "")
                    .strip()
            )
            return int(nilai_bersih)
        except ValueError:
            print("❌ Masukkan angka yang benar! Contoh: 100.000")


def get_connection():
    return sqlite3.connect(DB_FILE)


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("CREATE INDEX IF NOT EXISTS idx_tanggal ON kas(tanggal)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_jenis ON kas(jenis)")

    cur.execute("""
        CREATE TABLE IF NOT EXISTS kas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tanggal TEXT,
            petugas TEXT,
            jenis TEXT,
            keterangan TEXT,
            jumlah INTEGER
        )
    """)

    conn.commit()
    conn.close()


def get_petugas():
    try:
        user = os.getlogin()
    except:
        user = os.environ.get("USERNAME") or os.environ.get("USER")
    
    return user.strip() if user else "Unknown"


def format_rupiah(angka):
    return f"Rp {angka:,}".replace(",", ".")


# ===============================
# SALDO (dari saldo.py)
# ===============================
def hitung_saldo():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT
        SUM(CASE WHEN jenis='masuk' THEN jumlah ELSE -jumlah END)
        FROM kas
    """)
    saldo = cur.fetchone()[0]
    conn.close()
    return saldo if saldo else 0


def input_kas(jenis):
    conn = get_connection()
    cur = conn.cursor()

    petugas = get_petugas()
    keterangan = input("Keterangan      : ")
    jumlah = input_rupiah("Jumlah (Rp)     : ")

    cur.execute("""
        INSERT INTO kas (tanggal, petugas, jenis, keterangan, jumlah)
        VALUES (?, ?, ?, ?, ?)
    """, (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        petugas,
        jenis,
        keterangan,
        jumlah
    ))

    conn.commit()
    conn.close()

    print("\n✅ Transaksi berhasil dicatat")
    print(f"Saldo saat ini : {format_rupiah(hitung_saldo())}")


def laporan():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT tanggal, jenis, jumlah, keterangan, petugas FROM kas")
    rows = cur.fetchall()
    conn.close()

    print("\n========== LAPORAN KAS TAKMIR ==========")

    if not rows:
        print("Belum ada transaksi.")
        return

    for t in rows:
        print(
            f"{t[0]} | "
            f"{t[1].upper():6} | "
            f"{format_rupiah(t[2]):>15} | "
            f"{t[3]} | {t[4]}"
        )

    print("---------------------------------------")
    print(f"Saldo Akhir : {format_rupiah(hitung_saldo())}")


# ===============================
# TAKMIR (dari takmir.py)
# ===============================
def export_pdf():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT tanggal, jenis, jumlah, keterangan, petugas FROM kas")
    rows = cur.fetchall()
    conn.close()

    if not rows:
        print("❌ Tidak ada data untuk diexport.")
        return
    
    c = canvas.Canvas(FILE_PDF, pagesize=A4)
    width, height = A4
    y = height - 50
    
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "LAPORAN KAS TAKMIR")
    y -= 30

    c.setFont("Helvetica", 10)
    c.drawString(50, y, f"Tanggal Cetak : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    y -= 25
    
    c.line(50, y, width - 50, y)
    y -= 20

    for t in rows:
        if y < 50:
            c.showPage()
            y = height - 50

        teks = f"{t[0]} | {t[1]} | {format_rupiah(t[2])} | {t[3]} | {t[4]}"
        c.drawString(50, y, teks[:110])
        y -= 15
        
    y -= 15
    c.line(50, y, width - 50, y)
    y -= 20

    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y, f"Saldo Akhir : {format_rupiah(hitung_saldo())}")

    c.save()
    print(f"\n📄 Laporan PDF berhasil dibuat: {FILE_PDF}")


def menu():
    init_db()
    petugas = get_petugas()

    print("======================================")
    print(" SISTEM PENGELOLAAN KAS TAKMIR ")
    print("======================================")
    print(f"Petugas : {petugas}")
    
    while True:
        print("\nMenu:")
        print("1. Input Kas Masuk")
        print("2. Input Kas Keluar")
        print("3. Lihat Laporan Kas")
        print("4. Export Laporan ke PDF")
        print("5. Keluar")

        pilih = input("Pilih menu (1-5): ")
        
        if pilih == "1":
            input_kas("masuk")
        elif pilih == "2":
            input_kas("keluar")
        elif pilih == "3":
            laporan()
        elif pilih == "4":
            export_pdf()
        elif pilih == "5":
            print("\nAplikasi ditutup.")
            break
        else:
            print("❌ Pilihan tidak valid!")


if __name__ == "__main__":
    menu()