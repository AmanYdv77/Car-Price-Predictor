# Car Price Predictor Web App

A clean, structured machine learning project that predicts car prices using **Linear Regression**, packaged inside a modern **FastAPI** web server and a premium, responsive **HTML5/CSS3/JS** frontend.

---

## 🌟 Key Features

*   **Linear Regression Model**: Achieves an **$R^2$ score of ~0.798** in estimating car prices.
*   **FastAPI Backend**: Provides real-time predictions via validated JSON payloads (utilizing **Pydantic**).
*   **Premium Glassmorphism UI**: Built with a responsive dark-mode layout, blur-filtered backdrops, and animated background elements.
*   **Multi-Step wizard Form**: Groups the 23 model inputs into 4 digestible steps to maximize usability.
*   **Custom Range Sliders**: Numeric specs (like horsepower, curb weight, and engine size) feature drag controls with real-time value badges.
*   **Dual-Currency Outputs**: Displays predictions in both **USD ($)** and **INR (₹)** with an animated ease-out count-up rolling animation.
*   **Lucide Icons**: Styled with modern vectors to signpost sections and interactive controls.

---

## 📁 Repository Structure

```
├── models/                     # Trained ML model weights and encoders
│   ├── model.pkl               # Pickled Linear Regression model
│   ├── encoders.pkl            # Pickled LabelEncoders for text fields
│   └── expected_columns.pkl    # Order of columns expected by the model
├── static/                     # Frontend UI assets
│   ├── index.html              # Responsive multi-step wizard form layout
│   ├── style.css               # Glassmorphism dark-mode style sheets
│   └── script.js               # Wizard, slider logic, and rolling price anims
├── .gitignore                  # Prevents caching local virtualenvs & caches
├── CarPrice_Assignment.csv     # Training dataset
├── Car_Price_Predictor.ipynb   # Original exploratory research notebook
├── main.py                     # FastAPI application router and server
├── requirements.txt            # Python environment packages
└── train_model.py              # ML pipeline automation script
```

---

## 🚀 Getting Started

### 1. Installation & Environment Setup
Clone the repository and install the dependencies. It is recommended to use a virtual environment:

```bash
# Clone the repository
git clone https://github.com/AmanYdv77/Car_Price_Prediction.git
cd Car_Price_Prediction

# Create and activate a virtual environment
python -m venv .venv
# On Windows (PowerShell):
.venv\Scripts\Activate.ps1
# On Linux/macOS:
source .venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### 2. Train the Model
To train the model and save the pickles locally inside the `models/` directory, run the training pipeline:

```bash
python train_model.py
```

### 3. Run the FastAPI Server
Launch the development server using **Uvicorn**:

```bash
python -m uvicorn main:app --reload
```

Once running, navigate to the local address in your web browser:
👉 **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

---

## 📊 Model Details

The model is trained on the standard CarPrice assignment dataset. We drop identifiers like `car_ID` and `CarName` to prevent overfitting on string labels, encode categorical columns (like `fueltype`, `carbody`, and `enginetype`) using `LabelEncoder`, and fit a `LinearRegression` model.

*   **R² Score**: `0.798` (Explains ~80% of the price variance)
*   **Mean Absolute Error (MAE)**: `$2526.41`
*   **Root Mean Squared Error (RMSE)**: `$3989.54`