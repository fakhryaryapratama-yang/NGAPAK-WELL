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