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

