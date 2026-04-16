from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# เชื่อม database
def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# หน้าแรก (แสดงสินค้า + JOIN category)
@app.route('/')
def menu():
    conn = get_db()
    items = conn.execute('''
        SELECT items.*, categories.name AS category_name
        FROM items
        LEFT JOIN categories ON items.category_id = categories.id
    ''').fetchall()

    return render_template('menu.html', items=items)

# เพิ่มสินค้า
@app.route('/add', methods=['GET', 'POST'])
def add():
    conn = get_db()
    categories = conn.execute('SELECT * FROM categories').fetchall()

    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        image = request.form['image']
        stock = request.form['stock']
        category_id = request.form['category_id']

        conn.execute('''
            INSERT INTO items (name, price, image, stock, category_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, price, image, stock, category_id))
        conn.commit()

        return redirect('/')

    return render_template('add.html', categories=categories)

# แก้ไขสินค้า
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_db()
    item = conn.execute('SELECT * FROM items WHERE id = ?', (id,)).fetchone()
    categories = conn.execute('SELECT * FROM categories').fetchall()

    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        image = request.form['image']
        stock = request.form['stock']
        category_id = request.form['category_id']

        conn.execute('''
            UPDATE items
            SET name=?, price=?, image=?, stock=?, category_id=?
            WHERE id=?
        ''', (name, price, image, stock, category_id, id))
        conn.commit()

        return redirect('/')

    return render_template('edit.html', item=item, categories=categories)

# ลบสินค้า
@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db()
    conn.execute('DELETE FROM items WHERE id = ?', (id,))
    conn.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)