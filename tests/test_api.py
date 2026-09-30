import unittest
from fastapi.testclient import TestClient
from main import app

class TestCarPriceAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        cls.valid_payload = {
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
            "highwaympg": 27,
        }

    def test_health_check(self):
        """GET /health should return 200 with operational status."""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")
        self.assertTrue(data["model_loaded"])

    def test_root_serves_html(self):
        """GET / should serve the frontend application index.html."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/html", response.headers.get("content-type", ""))

    def test_predict_success(self):
        """POST /predict with valid payload should return a positive price."""
        response = self.client.post("/predict", json=self.valid_payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("predicted_price", data)
        self.assertGreater(data["predicted_price"], 0)

    def test_predict_unseen_category_returns_400(self):
        """POST /predict with an invalid categorical value must return 400 Bad Request."""
        invalid_payload = dict(self.valid_payload, fueltype="hydrogen")
        response = self.client.post("/predict", json=invalid_payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid or unseen value", response.json().get("detail", ""))

    def test_predict_missing_fields_returns_422(self):
        """POST /predict with missing required fields must return 422 Unprocessable Entity."""
        incomplete_payload = {"symboling": 3, "fueltype": "gas"}
        response = self.client.post("/predict", json=incomplete_payload)
        self.assertEqual(response.status_code, 422)

if __name__ == "__main__":
    unittest.main()
