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

