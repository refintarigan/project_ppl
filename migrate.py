import sqlite3

conn = sqlite3.connect("data_barang.db")
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE barang ADD COLUMN harga INTEGER")
    print("Kolom 'harga' ditambahkan.")
except sqlite3.OperationalError:
    print("Kolom 'harga' sudah ada.")

try:
    cursor.execute("ALTER TABLE barang ADD COLUMN supplier TEXT")
    print("Kolom 'supplier' ditambahkan.")
except sqlite3.OperationalError:
    print("Kolom 'supplier' sudah ada.")

try:
    cursor.execute("ALTER TABLE barang ADD COLUMN tanggal_masuk TEXT")
    print("Kolom 'tanggal_masuk' ditambahkan.")
except sqlite3.OperationalError:
    print("Kolom 'tanggal_masuk' sudah ada.")

conn.commit()
conn.close()
print("Migrasi selesai.")
