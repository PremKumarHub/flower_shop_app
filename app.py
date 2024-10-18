from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key for production

# Database setup
db_file = 'local_database.db'

def get_db_connection():
    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_farmer', methods=['GET', 'POST'])
def add_farmer():
    if request.method == 'POST':
        farmer_id = request.form['farmer_id']
        name = request.form['name']
        if name and farmer_id:
            try:
                conn = get_db_connection()
                conn.execute('INSERT INTO farmers (id, name) VALUES (?, ?)', (farmer_id, name))
                conn.commit()
                conn.close()
                flash('Farmer added successfully!')
                return redirect(url_for('index'))
            except sqlite3.IntegrityError:
                flash('Farmer ID must be unique!')
        else:
            flash('Farmer name and ID cannot be empty!')
    return render_template('add_farmer.html')

@app.route('/log_transaction', methods=['GET', 'POST'])
def log_transaction():
    if request.method == 'POST':
        farmer_id = request.form['farmer_id']
        amount = request.form['amount']
        description = request.form['description']
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if amount and description:
            conn = get_db_connection()
            conn.execute('INSERT INTO transactions (farmer_id, amount, description, date) VALUES (?, ?, ?, ?)',
                         (farmer_id, amount, description, date_time))
            conn.commit()
            conn.close()
            flash('Transaction logged successfully!')
            return redirect(url_for('index'))
        else:
            flash('Amount and Description cannot be empty!')

    return render_template('log_transaction.html')

@app.route('/transactions')
def transactions():
    conn = get_db_connection()
    trans = conn.execute('SELECT f.id as farmer_id, f.name, t.amount, t.description, t.date FROM transactions t JOIN farmers f ON t.farmer_id = f.id').fetchall()
    conn.close()
    return render_template('transactions.html', transactions=trans)

if __name__ == '__main__':
    app.run(debug=True)
