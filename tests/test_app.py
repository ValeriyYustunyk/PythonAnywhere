import unittest
import json
from app import app


class AppTestCase(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def post(self, url, payload):
        return self.client.post(
            url,
            data=json.dumps(payload),
            content_type="application/json",
        )

    # ------------------------------------------------------------------ #
    # Index page                                                           #
    # ------------------------------------------------------------------ #

    def test_index_returns_200(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    # ------------------------------------------------------------------ #
    # Celsius → Fahrenheit                                                 #
    # ------------------------------------------------------------------ #

    def test_celsius_freezing(self):
        data = self.post("/api/celsius", {"celsius": 0}).get_json()
        self.assertEqual(data["fahrenheit"], 32.0)

    def test_celsius_boiling(self):
        data = self.post("/api/celsius", {"celsius": 100}).get_json()
        self.assertEqual(data["fahrenheit"], 212.0)

    def test_celsius_body_temp(self):
        data = self.post("/api/celsius", {"celsius": 37}).get_json()
        self.assertEqual(data["fahrenheit"], 98.6)

    def test_celsius_negative(self):
        data = self.post("/api/celsius", {"celsius": -40}).get_json()
        self.assertEqual(data["fahrenheit"], -40.0)

    # ------------------------------------------------------------------ #
    # Budget Helper                                                        #
    # ------------------------------------------------------------------ #

    def test_budget_surplus(self):
        data = self.post(
            "/api/budget", {"income": 3000, "expenses": [500, 200, 100]}).get_json()
        self.assertEqual(data["total_expenses"], 800.0)
        self.assertEqual(data["remaining"], 2200.0)
        self.assertEqual(data["status"], "surplus")

    def test_budget_deficit(self):
        data = self.post(
            "/api/budget", {"income": 500, "expenses": [400, 300]}).get_json()
        self.assertEqual(data["status"], "deficit")
        self.assertEqual(data["remaining"], -200.0)

    def test_budget_break_even(self):
        data = self.post(
            "/api/budget", {"income": 1000, "expenses": [600, 400]}).get_json()
        self.assertEqual(data["remaining"], 0.0)
        self.assertEqual(data["status"], "surplus")

    def test_budget_no_expenses(self):
        data = self.post(
            "/api/budget", {"income": 2000, "expenses": []}).get_json()
        self.assertEqual(data["total_expenses"], 0.0)
        self.assertEqual(data["remaining"], 2000.0)

    # ------------------------------------------------------------------ #
    # Pizza Order                                                          #
    # ------------------------------------------------------------------ #

    def test_pizza_small_no_toppings(self):
        data = self.post(
            "/api/pizza", {"size": "small", "toppings": []}).get_json()
        self.assertEqual(data["total"], 8.99)
        self.assertEqual(data["base_price"], 8.99)

    def test_pizza_medium_two_toppings(self):
        data = self.post(
            "/api/pizza", {"size": "medium", "toppings": ["Pepperoni", "Olives"]}).get_json()
        self.assertEqual(data["total"], round(11.99 + 2 * 1.50, 2))

    def test_pizza_large_all_toppings(self):
        toppings = ["Pepperoni", "Mushrooms", "Olives",
                    "Onions", "Bell Peppers", "Extra Cheese"]
        data = self.post(
            "/api/pizza", {"size": "large", "toppings": toppings}).get_json()
        self.assertEqual(data["total"], round(14.99 + 6 * 1.50, 2))

    def test_pizza_returns_toppings_list(self):
        toppings = ["Pepperoni", "Olives"]
        data = self.post(
            "/api/pizza", {"size": "small", "toppings": toppings}).get_json()
        self.assertEqual(data["toppings"], toppings)

    # ------------------------------------------------------------------ #
    # Ride Fare Guesser                                                    #
    # ------------------------------------------------------------------ #

    def test_fare_base_only(self):
        # 0 miles, 0 minutes → base fare only
        data = self.post("/api/fare", {"distance": 0, "minutes": 0}).get_json()
        self.assertEqual(data["fare"], 2.50)

    def test_fare_5_miles_15_minutes(self):
        # 2.50 + (5 * 1.75) + (15 * 0.25) = 2.50 + 8.75 + 3.75 = 15.00
        data = self.post(
            "/api/fare", {"distance": 5, "minutes": 15}).get_json()
        self.assertEqual(data["fare"], 15.00)

    def test_fare_10_miles_30_minutes(self):
        expected = round(2.50 + 10 * 1.75 + 30 * 0.25, 2)
        data = self.post(
            "/api/fare", {"distance": 10, "minutes": 30}).get_json()
        self.assertEqual(data["fare"], expected)

    def test_fare_returns_float(self):
        data = self.post(
            "/api/fare", {"distance": 3, "minutes": 10}).get_json()
        self.assertIsInstance(data["fare"], float)


if __name__ == "__main__":
    unittest.main()
