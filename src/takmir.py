# ===============================
# EXPORT PDF
# ===============================
def export_pdf():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT tanggal, jenis, jumlah, keterangan, petugas FROM kas")
    rows = cur.fetchall()
    conn.close()
