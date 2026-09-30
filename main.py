from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np

BASE_DIR = Path(__file__).resolve().parent
MODELS_DIR = BASE_DIR / "models"
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(title="Car Price Predictor API")

# Load model, encoders, and expected columns globally
try:
    model = joblib.load(MODELS_DIR / "model.pkl")
    encoders = joblib.load(MODELS_DIR / "encoders.pkl")
    expected_columns = joblib.load(MODELS_DIR / "expected_columns.pkl")
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
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "encoders_loaded": encoders is not None,
    }

@app.get("/")
async def root():
    index_file = STATIC_DIR / "index.html"
    if not index_file.exists():
        raise HTTPException(status_code=404, detail="Frontend index.html not found.")
    return FileResponse(index_file)

@app.post("/predict")
async def predict_price(features: CarFeatures):
    if model is None or encoders is None or expected_columns is None:
        raise HTTPException(status_code=500, detail="Model is not loaded.")
        
    try:
        # Convert input to dictionary (compatible with Pydantic v1 & v2)
        input_data = (
            features.model_dump()
            if hasattr(features, "model_dump")
            else features.dict()
        )
        
        # Apply LabelEncoders for categorical columns
        for col, le in encoders.items():
            if col in input_data:
                try:
                    input_data[col] = le.transform([input_data[col]])[0]
                except ValueError:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Invalid or unseen value for {col}: {input_data[col]}"
                    )
        
        # Create DataFrame in the exact order the model expects
        df = pd.DataFrame([input_data])[expected_columns]
        
        # Predict
        prediction = model.predict(df)[0]
        
        # Return price (ensure non-negative)
        predicted_price = max(0.0, float(prediction))
        
        return {"predicted_price": round(predicted_price, 2)}
        
    except HTTPException:
        # Re-raise explicit HTTP exceptions (e.g. 400 Bad Request)
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
