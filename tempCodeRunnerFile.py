
from flask import Flask, render_template, request
import pandas as pd
import os
import pickle

# Initialize Flask app
app = Flask(__name__)

# Load ML model
with open('model.pkl', 'rb') as file:
    model = pickle.load(file)

# Load CSV files
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
laptops_df = pd.read_csv(os.path.join(DATA_DIR, 'laptops.csv'))
mobiles_df = pd.read_csv(os.path.join(DATA_DIR, 'mobiles.csv'))

@app.route('/')
def index():
    gadget_types = ['Mobile', 'Laptop']
    phone_brands = mobiles_df['Brand'].dropna().unique().tolist()
    laptop_brands = laptops_df['Brand'].dropna().unique().tolist()
    problem_types = [
    'Screen Cracked',
    'Battery Issue',
    'Charging Issue',
    'Water Damage',
    'Speaker Issue',
    'Camera Problem',
    'Microphone Not Working',
    'Software Crash',
    'Overheating',
    'Network Issue'
]

    severity_levels = ['Low', 'Medium', 'High']

    return render_template('index.html',
                           gadget_types=gadget_types,
                           phone_brands=phone_brands,
                           laptop_brands=laptop_brands,
                           problem_types=problem_types,
                           severity_levels=severity_levels,
                           prediction_text=None)

@app.route('/', methods=['POST'])
def predict():
    # Collect input from form
    gadget_type = request.form['gadget_type']
    brand = request.form['brand']
    problem_type = request.form['problem_type']
    severity = request.form['severity']

    # Mapping
    gadget_type_mapping = {'Phone': 0, 'Laptop': 1}
    problem_type_mapping = {
    'Screen Cracked': 0,
    'Battery Issue': 1,
    'Charging Issue': 2,
    'Water Damage': 3,
    'Speaker Issue': 4,
    'Camera Problem': 5,
    'Microphone Not Working': 6,
    'Software Crash': 7,
    'Overheating': 8,
    'Network Issue': 9
}

    severity_mapping = {'Low': 0, 'Medium': 1, 'High': 2}

    all_brands = list(set(mobiles_df['Brand'].dropna().tolist() + laptops_df['Brand'].dropna().tolist()))
    brand_mapping = {b: i for i, b in enumerate(all_brands)}

    input_features = [[
        gadget_type_mapping.get(gadget_type, 0),
        brand_mapping.get(brand, 0),
        problem_type_mapping.get(problem_type, 0),
        severity_mapping.get(severity, 0)
    ]]

    prediction = model.predict(input_features)
    cost = round(prediction[0], 2)

    return render_template('index.html',
                           gadget_types=['Phone', 'Laptop'],
                           phone_brands=mobiles_df['Brand'].dropna().unique().tolist(),
                           laptop_brands=laptops_df['Brand'].dropna().unique().tolist(),
                           problem_types=list(problem_type_mapping.keys()),
                           severity_levels=list(severity_mapping.keys()),
                           prediction_text=f"Estimated Repair Cost: ₹{cost}")

@app.route('/devices')
def show_devices():
    laptops_html = laptops_df.head(10).to_html(classes='table table-striped')
    mobiles_html = mobiles_df.head(10).to_html(classes='table table-striped')
    return render_template('devices.html', laptops=laptops_html, mobiles=mobiles_html)

if __name__ == '__main__':
    app.run(debug=True)
