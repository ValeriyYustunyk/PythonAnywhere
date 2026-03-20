from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


# --- Celsius to Fahrenheit ---
@app.route("/api/celsius", methods=["POST"])
def celsius_to_fahrenheit():
    data = request.get_json()
    celsius = float(data["celsius"])
    fahrenheit = (celsius * 9 / 5) + 32
    return jsonify({"fahrenheit": round(fahrenheit, 2)})


# --- Budget Helper ---
@app.route("/api/budget", methods=["POST"])
def budget_helper():
    data = request.get_json()
    income = float(data["income"])
    expenses = [float(e) for e in data["expenses"] if str(e).strip()]
    total_expenses = sum(expenses)
    remaining = income - total_expenses
    return jsonify({
        "total_expenses": round(total_expenses, 2),
        "remaining": round(remaining, 2),
        "status": "surplus" if remaining >= 0 else "deficit",
    })


# --- Pizza Ordering ---
@app.route("/api/pizza", methods=["POST"])
def pizza_order():
    data = request.get_json()
    size = data["size"]
    toppings = data.get("toppings", [])
    size_prices = {"small": 8.99, "medium": 11.99, "large": 14.99}
    topping_price = 1.50
    base_price = size_prices.get(size, 8.99)
    total = base_price + (len(toppings) * topping_price)
    return jsonify({
        "size": size,
        "toppings": toppings,
        "base_price": base_price,
        "total": round(total, 2),
    })


# --- Ride Fare Guesser ---
@app.route("/api/fare", methods=["POST"])
def ride_fare():
    data = request.get_json()
    distance = float(data["distance"])
    minutes = float(data["minutes"])
    base_fare = 2.50
    per_mile = 1.75
    per_minute = 0.25
    fare = base_fare + (distance * per_mile) + (minutes * per_minute)
    return jsonify({"fare": round(fare, 2)})


if __name__ == "__main__":
    app.run(debug=True)
