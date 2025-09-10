import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle

# Load dataset
df = pd.read_csv('repair_data.csv')

# Mapping
gadget_type_mapping = {'Phone': 0, 'Laptop': 1, 'Tablet': 2}
brand_mapping = {'Samsung': 0, 'Dell': 1, 'Apple': 2}
problem_type_mapping = {'Screen Cracked': 0, 'Battery Issue': 1, 'Charging Issue': 2}
severity_mapping = {'Low': 0, 'Medium': 1, 'High': 2}

# Apply mapping
df['gadget_type'] = df['gadget_type'].map(gadget_type_mapping)
df['brand'] = df['brand'].map(brand_mapping)
df['problem_type'] = df['problem_type'].map(problem_type_mapping)
df['severity'] = df['severity'].map(severity_mapping)

# Features and target
X = df[['gadget_type', 'brand', 'problem_type', 'severity']]
y = df['repair_cost']

# Train model
model = LinearRegression()
model.fit(X, y)

# Save model
with open('model.pkl', 'wb') as file:
    pickle.dump(model, file)

print("✅ Model trained and saved as model.pkl")
