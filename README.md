<div align="center">

# Car Price Predictor

**Machine Learning Valuation Engine and Interactive FastAPI Web Application**

A production-ready predictive service estimating automobile market valuations based on vehicle specifications, powertrain metrics, and dimensional features.

<br/>

[![CI](https://github.com/AmanYdv77/Car-Price-Predictor/actions/workflows/ci.yml/badge.svg)](https://github.com/AmanYdv77/Car-Price-Predictor/actions/workflows/ci.yml)
[![Python Version](https://img.shields.io/badge/Python-3.8%2B-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688.svg?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.0%2B-F7931E.svg?style=flat&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=flat)](LICENSE)
[![Build Status](https://img.shields.io/badge/Tests-Passing-success.svg?style=flat)](tests/)

<br/>

[Deployment](#deployment) &bull;
[Key Capabilities](#key-capabilities) &bull;
[API Specification](#api-specification) &bull;
[Model Performance](#model-performance) &bull;
[Installation & Usage](#installation--usage) &bull;
[Project Structure](#project-structure) &bull;
[License](#license)

---

</div>

## Deployment

Deploy this full-stack application instantly to **Vercel** with zero server management:

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/AmanYdv77/Car-Price-Predictor)

1. Click the **Deploy with Vercel** button above or import AmanYdv77/Car-Price-Predictor in your [Vercel Dashboard](https://vercel.com/dashboard).
2. Leave all environment settings as default (Vercel automatically detects ercel.json and Python dependencies in 
equirements.txt).
3. Click **Deploy**. Your application will be live with an automatic HTTPS domain in under 2 minutes.

---

## Key Capabilities

> **Car Price Predictor** combines an empirical machine learning pipeline with a high-performance asynchronous API and an intuitive Glassmorphism multi-step wizard interface.

* **Linear Regression Engine:** Delivers deterministic valuation estimates with an R² score of ~0.798 on unseen evaluation holdouts.
* **FastAPI Backend:** Fully asynchronous RESTful interface utilizing Pydantic schemas for strict payload validation and structured error handling.
* **Glassmorphism Interface:** Responsive multi-step wizard grouping 23 complex vehicle parameters into 4 logical steps (Profile, Dimensions, Powertrain, and Performance).
* **Dual Currency Conversion:** Real-time client-side conversion delivering valuations in both USD ($) and INR (₹).
* **Automated Test Coverage:** Complete integration test suite validating server health, HTML serving, successful inferences, and bad request error codes.

---

## API Specification

The backend exposes the following RESTful endpoints:

| Method | Endpoint | Description | Request Body | Response |
|:---|:---|:---|:---|:---|
| `GET` | `/health` | Service health status and model artifact readiness | None | `{"status": "healthy", "model_loaded": true}` |
| `GET` | `/` | Serves the interactive HTML5/CSS3 frontend | None | HTML document |
| `GET` | `/docs` | Interactive Swagger UI API documentation | None | OpenAPI interface |
| `POST` | `/predict` | Computes price valuation for given vehicle features | `CarFeatures` (JSON) | `{"predicted_price": 13119.93}` |

### Sample Inference Payload

```json
{
  "symboling": 3,
  "fueltype": "gas",
  "aspiration": "std",
  "doornumber": "two",
  "carbody": "convertible",
  "drivewheel": "rwd",
  "enginelocation": "front",
  "wheelbase": 88.6,
  "carlength": 168.8,
  "carwidth": 64.1,
  "carheight": 48.8,
  "curbweight": 2548,
  "enginetype": "dohc",
  "cylindernumber": "four",
  "enginesize": 130,
  "fuelsystem": "mpfi",
  "boreratio": 3.47,
  "stroke": 2.68,
  "compressionratio": 9.0,
  "horsepower": 111,
  "peakrpm": 5000,
  "citympg": 21,
  "highwaympg": 27
}
```

---

## Model Performance

The predictive model is trained on standard automotive benchmark telemetry. Unique identifiers (such as `car_ID` and `CarName`) are discarded to avoid high-cardinality overfitting, categorical variables are mapped using fitted label encoders, and continuous features are regressed against market price.

| Metric | Score | Interpretation |
|:---|:---|:---|
| **R² Score** | `0.798` | Explains approximately 80% of total price variance |
| **Mean Absolute Error (MAE)** | `$2,526.41` | Average absolute divergence across predictions |
| **Root Mean Squared Error (RMSE)** | `$3,989.54` | Penalized metric reflecting variance on extreme luxury trims |

---

## Installation & Usage

### 1. Environment Setup

```bash
# Clone the repository
git clone https://github.com/AmanYdv77/Car-Price-Predictor.git
cd Car-Price-Predictor

# Create and activate virtual environment
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On macOS / Linux:
source .venv/bin/activate

# Install required dependencies
pip install -r requirements.txt
```

### 2. Model Training Pipeline
To retrain the regression model and export serialized artifacts into `models/`:

```bash
python train_model.py
```

### 3. Launching the Web Server
Start the FastAPI server via Uvicorn:

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Access the interface in your browser:
* **Application Interface:** `http://127.0.0.1:8000`
* **Interactive API Documentation:** `http://127.0.0.1:8000/docs`

### 4. Running Verification Tests
Execute the automated test suite locally:

```bash
python -m unittest discover -s tests -v
```

---

## Project Structure

```text
Car-Price-Predictor/
|-- .github/
|   `-- workflows/
|       `-- ci.yml                  # Automated CI test pipeline
|-- models/
|   |-- encoders.pkl                # Serialized categorical encoders
|   |-- expected_columns.pkl        # Deterministic feature column ordering
|   `-- model.pkl                   # Trained Linear Regression model
|-- static/
|   |-- index.html                  # Responsive multi-step wizard form layout
|   |-- script.js                   # Client-side wizard transitions and dual currency logic
|   `-- style.css                   # Glassmorphism dark theme stylesheets
|-- api/
|   -- index.py              # Vercel serverless function entrypoint
|-- tests/
|   `-- test_api.py                 # Health, static serving, and prediction tests
|-- .gitignore                      # Git exclusion rules
|-- CarPrice_Assignment.csv         # Automotive dataset
|-- Car_Price_Predictor.ipynb       # Exploratory analysis and training notebook
|-- LICENSE                         # MIT License
|-- main.py                         # FastAPI application backend and routing
|-- README.md
|-- vercel.json               # Vercel deployment and routing configuration                       # Platform documentation
|-- requirements.txt                # Python environment specifications
`-- train_model.py                  # Model training and artifact generation pipeline
```

---

## Author

**Aman Yadav**
* GitHub: [@AmanYdv77](https://github.com/AmanYdv77)

---

## License

This project is licensed under the [MIT License](LICENSE).
