from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np
import os

app = FastAPI(title="Car Price Predictor API")

# Load model, encoders, and expected columns globally
try:
    model = joblib.load('models/model.pkl')
    encoders = joblib.load('models/encoders.pkl')
    expected_columns = joblib.load('models/expected_columns.pkl')
except Exception as e:
    print(f"Error loading model files: {e}. Make sure to run train_model.py first.")
    model, encoders, expected_columns = None, None, None

class CarFeatures(BaseModel):
    symboling: int
    fueltype: str
    aspiration: str
    doornumber: str
    carbody: str
    drivewheel: str
    enginelocation: str
    wheelbase: float
    carlength: float
    carwidth: float
    carheight: float
    curbweight: int
    enginetype: str
    cylindernumber: str
    enginesize: int
    fuelsystem: str
    boreratio: float
    stroke: float
    compressionratio: float
    horsepower: int
    peakrpm: int
    citympg: int
    highwaympg: int

# Mount static directory for HTML/CSS/JS
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return FileResponse("static/index.html")

@app.post("/predict")
async def predict_price(features: CarFeatures):
    if model is None:
        raise HTTPException(status_code=500, detail="Model is not loaded.")
        
    try:
        # Convert input to dictionary
        input_data = features.dict()
        
        # Apply LabelEncoders for categorical columns
        for col, le in encoders.items():
            if col in input_data:
                # Handle unseen labels by setting to a default or error
                try:
                    # We pass it as a list to transform
                    input_data[col] = le.transform([input_data[col]])[0]
                except ValueError:
                    # If unseen label, you might want to handle it, but for now we raise
                    raise HTTPException(status_code=400, detail=f"Invalid or unseen value for {col}: {input_data[col]}")
        
        # Create DataFrame in the exact order the model expects
        df = pd.DataFrame([input_data])[expected_columns]
        
        # Predict
        prediction = model.predict(df)[0]
        
        # Return price (ensure no negative values are returned)
        predicted_price = max(0, float(prediction))
        
        return {"predicted_price": round(predicted_price, 2)}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
