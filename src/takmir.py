# ===============================
# EXPORT PDF
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
    
# ===============================
# MENU
# ===============================   
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