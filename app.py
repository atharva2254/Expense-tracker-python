from flask import Flask, render_template, request, redirect, url_for
import sqlite3

# Initialize Flask app
app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect("expenses.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT,
                    description TEXT,
                    category TEXT,
                    amount REAL)''')
    conn.commit()
    conn.close()

def add_expense(date, description, category, amount):
    conn = sqlite3.connect("expenses.db")
    c = conn.cursor()
    c.execute("INSERT INTO expenses (date, description, category, amount) VALUES (?, ?, ?, ?)",
              (date, description, category, amount))
    conn.commit()
    conn.close()

def view_expenses():
    conn = sqlite3.connect("expenses.db")
    c = conn.cursor()
    c.execute("SELECT * FROM expenses")
    rows = c.fetchall()
    conn.close()
    return rows

def delete_expense(expense_id):
    conn = sqlite3.connect("expenses.db")
    c = conn.cursor()
    c.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()

# Routes
@app.route('/')
def index():
    expenses = view_expenses()
    return render_template('index.html', expenses=expenses)

@app.route('/add', methods=['POST'])
def add():
    date = request.form['date']
    description = request.form['description']
    category = request.form['category']
    amount = request.form['amount']
    try:
        add_expense(date, description, category, float(amount))
        return redirect(url_for('index'))
    except ValueError:
        return "Amount must be a number."

@app.route('/delete/<int:expense_id>')
def delete(expense_id):
    delete_expense(expense_id)
    return redirect(url_for('index'))

# Initialize database
init_db()

if __name__ == '__main__':
    app.run(debug=True)
