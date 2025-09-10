from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import sqlite3
import os
import pickle

# -------------------------
# Flask App Setup
# -------------------------
app = Flask(__name__)
app.secret_key = 'secret123'  # Needed for session

# -------------------------
# Database Setup
# -------------------------
DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'repairs.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS repairs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            gadget_type TEXT,
            brand TEXT,
            problem_type TEXT,
            severity TEXT,
            estimated_cost REAL,
            parts_cost REAL,
            labor_cost REAL,
            tax REAL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# -------------------------
# Load Model & Data
# -------------------------
with open('model.pkl', 'rb') as file:
    model = pickle.load(file)

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
laptops_df = pd.read_csv(os.path.join(DATA_DIR, 'laptops.csv'))
mobiles_df = pd.read_csv(os.path.join(DATA_DIR, 'mobiles.csv'))

# Dummy login credentials
USERNAME = "admin"
PASSWORD = "admin123"

# -------------------------
# Routes
# -------------------------

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == USERNAME and password == PASSWORD:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            error = "Invalid username or password"

    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/', methods=['GET', 'POST'])
def index():
    if 'username' not in session:
        return redirect(url_for('login'))

    gadget_types = ['Phone', 'Laptop']
    phone_brands = mobiles_df['Brand'].dropna().unique().tolist()
    laptop_brands = laptops_df['Brand'].dropna().unique().tolist()
    problem_types = [
        'Screen Cracked', 'Battery Issue', 'Charging Issue', 'Water Damage',
        'Speaker Issue', 'Camera Problem', 'Microphone Not Working',
        'Software Crash', 'Overheating', 'Network Issue'
    ]
    severity_levels = ['Low', 'Medium', 'High']

    if request.method == 'POST':
        gadget_type = request.form.get('gadget_type')
        brand = request.form.get('brand')
        problem_type = request.form.get('problem_type')
        severity = request.form.get('severity')

        # Feature mappings
        gadget_type_mapping = {'Phone': 0, 'Laptop': 1}
        problem_type_mapping = {p: i for i, p in enumerate(problem_types)}
        severity_mapping = {'Low': 0, 'Medium': 1, 'High': 2}
        all_brands = list(set(phone_brands + laptop_brands))
        brand_mapping = {b: i for i, b in enumerate(all_brands)}

        input_features = [[
            gadget_type_mapping.get(gadget_type, 0),
            brand_mapping.get(brand, 0),
            problem_type_mapping.get(problem_type, 0),
            severity_mapping.get(severity, 0)
        ]]

        prediction = model.predict(input_features)
        cost = round(prediction[0], 2)
        parts_cost = round(cost * 0.6, 2)
        labor_cost = round(cost * 0.3, 2)
        tax = round(cost * 0.1, 2)

        # Save to DB
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO repairs (username, gadget_type, brand, problem_type, severity,
                                 estimated_cost, parts_cost, labor_cost, tax)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (session['username'], gadget_type, brand, problem_type, severity,
              cost, parts_cost, labor_cost, tax))
        conn.commit()
        conn.close()

        # Store submission in session for display
        session['submitted_data'] = {
            'gadget_type': gadget_type,
            'brand': brand,
            'problem_type': problem_type,
            'severity': severity,
            'cost': cost
        }

        return redirect(url_for('submitted'))

    return render_template('index.html',
                           gadget_types=gadget_types,
                           phone_brands=phone_brands,
                           laptop_brands=laptop_brands,
                           problem_types=problem_types,
                           severity_levels=severity_levels)


@app.route('/submitted')
def submitted():
    if 'username' not in session:
        return redirect(url_for('login'))

    data = session.get('submitted_data')
    if not data:
        return redirect(url_for('index'))

    return render_template('submitted.html', submitted_data=data)


@app.route('/history')
def history():
    if 'username' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM repairs WHERE username = ?', (session['username'],))
    rows = cursor.fetchall()
    conn.close()
    return render_template('history.html', records=rows)


# -------------------------
# Run App
# -------------------------
if __name__ == '__main__':
    app.run(debug=True)
