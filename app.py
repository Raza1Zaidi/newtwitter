from flask import Flask, render_template, request, jsonify
import os
from scraper import fetch_profile_metrics, init_driver

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        auth_token = request.form.get("auth_token")
        ct0 = request.form.get("ct0")
        profiles = request.form.get("profiles")

        if not auth_token or not ct0 or not profiles:
            return jsonify({"error": "All fields are required!"}), 400

        screen_names = [name.strip() for name in profiles.split(",") if name.strip()]

        driver = init_driver()
        results = fetch_profile_metrics(driver, auth_token, ct0, screen_names)

        return jsonify(results)

    return render_template("index.html")
    
if __name__ == "__main__":
    app.run(debug=True)
