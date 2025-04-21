# app.py
from flask import Flask, render_template, jsonify
import firebase_admin
from firebase_admin import db
import pickle
import numpy as np
import joblib  # Import joblib for loading the scaler parameters
from firebase_config import *

app = Flask(__name__)

# Initialize Firebase app (assuming firebase_config.py handles this)

# Load the model
model_path = 'random_forest_model2.pkl'
with open(model_path, 'rb') as file:
    model = pickle.load(file)

# Load the scaler parameters
scaler_params = joblib.load('scaler_params.pkl')

# Create a new StandardScaler instance and set its mean and scale
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaler.mean_ = scaler_params['mean']
scaler.scale_ = scaler_params['scale']

@app.route('/')
def index():
    return render_template('newindex.html')

@app.route('/get_data')
def get_data():
    meanaz = db.reference('MPU6050/meanaz').get()
    meangz = db.reference('MPU6050/meangz').get()
    meanay = db.reference('MPU6050/meanay').get()
    meangy = db.reference('MPU6050/meangy').get()
    meangx = db.reference('MPU6050/meangx').get()
    meanax = db.reference('MPU6050/meanax').get()
    
    values = [meanax, meanay, meanaz, meangx, meangy, meangz]
    input_data = np.array(values).reshape(1, -1)

    # Scale the input data using the loaded scaler
    input_data_scaled = scaler.transform(input_data)

    # Make prediction using the scaled data
    prediction = model.predict(input_data_scaled)[0]
    prediction_proba = model.predict_proba(input_data_scaled)[0]

    confidence = {
        'fall': prediction_proba[0] * 100,
        'sit': prediction_proba[1] * 100,
        'stand': prediction_proba[2] * 100,
        'walk': prediction_proba[3] * 100,
    }

    return jsonify({
        'values': values,
        'prediction': prediction,
        'confidence': confidence
    })

if __name__ == '__main__':
    app.run(debug=True)
