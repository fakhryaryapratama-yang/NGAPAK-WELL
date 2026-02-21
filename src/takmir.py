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