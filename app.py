from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'rahasia_gudang'

def init_db():
    with sqlite3.connect("data_barang.db") as conn:
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS barang (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                kode TEXT,
                nama TEXT,
                kategori TEXT,
                stok INTEGER,
                harga INTEGER,
                supplier TEXT,
                tanggal_masuk TEXT
            )
        """)
        conn.commit()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == '123':
            session['user'] = 'admin'
            return redirect(url_for('index'))
        return "Login gagal"
    return render_template('login.html')

@app.route('/index')
def index():
    if 'user' not in session:
        return redirect(url_for('login'))
    conn = sqlite3.connect("data_barang.db")
    barang = conn.execute("SELECT * FROM barang").fetchall()
    conn.close()
    return render_template('index.html', barang=barang)

@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if 'user' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        kode = int(request.form['kode'])
        nama = request.form['nama']
        kategori = request.form['kategori']
        stok = int(request.form['stok'])
        harga = int(request.form['harga'])
        supplier = request.form['supplier']
        tanggal_masuk = request.form['tanggal_masuk']
        conn = sqlite3.connect("data_barang.db")
        conn.execute(
            "INSERT INTO barang (kode, nama, kategori, stok, harga, supplier, tanggal_masuk) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (kode, nama, kategori, stok, harga, supplier, tanggal_masuk)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add_item.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_item(id):
    if 'user' not in session:
        return redirect(url_for('login'))
    conn = sqlite3.connect("data_barang.db")
    cursor = conn.cursor()
    if request.method == 'POST':
        kode = int(request.form['kode'])
        nama = request.form['nama']
        kategori = request.form['kategori']
        stok = int(request.form['stok'])
        harga = int(request.form['harga'])
        supplier = request.form['supplier']
        tanggal_masuk = request.form['tanggal_masuk']
        cursor.execute("""
            UPDATE barang
            SET kode=?, nama=?, kategori=?, stok=?, harga=?, supplier=?, tanggal_masuk=?
            WHERE id=?
        """, (kode, nama, kategori, stok, harga, supplier, tanggal_masuk, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    cursor.execute("SELECT * FROM barang WHERE id=?", (id,))
    barang = cursor.fetchone()
    conn.close()
    return render_template('edit_item.html', barang=barang)

@app.route('/delete/<int:id>')
def delete_item(id):
    if 'user' not in session:
        return redirect(url_for('login'))
    conn = sqlite3.connect("data_barang.db")
    conn.execute("DELETE FROM barang WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/distribusi')
def distribusi():
    if 'user' not in session:
        return redirect(url_for('login'))
    conn = sqlite3.connect("data_barang.db")
    barang = conn.execute("SELECT * FROM barang").fetchall()
    conn.close()
    return render_template('distribusi.html', barang=barang)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
