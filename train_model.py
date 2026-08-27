import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def train_and_save_model():
    print("Loading dataset...")
    df = pd.read_csv("CarPrice_Assignment.csv")  
    
    # Drop unnecessary columns
    df.drop(["car_ID", "CarName"], axis=1, inplace=True)
    
    print("Encoding categorical variables...")
    categorical_cols = df.select_dtypes(include=["object"]).columns
    
    encoders = {}
    for col in categorical_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        encoders[col] = le
        
    # Split features and target
    X = df.drop("price", axis=1)
    y = df["price"]
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    print("Training model...")
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Evaluate
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    r2 = r2_score(y_test, predictions)
    
    print("Model Performance on Test Set:")
    print(f"MAE: {round(mae, 2)}")
    print(f"RMSE: {round(rmse, 2)}")
    print(f"R2 Score: {round(r2, 3)}")
    
    print("Saving model and encoders...")
    joblib.dump(model, 'model.pkl')
    joblib.dump(encoders, 'encoders.pkl')
    # Also save the list of expected columns in order, for the FastAPI backend
    expected_columns = list(X.columns)
    joblib.dump(expected_columns, 'expected_columns.pkl')
    
    print("Done! model.pkl, encoders.pkl and expected_columns.pkl have been saved.")

if __name__ == "__main__":
    train_and_save_model()
