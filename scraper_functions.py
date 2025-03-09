import os
import subprocess
from flask import Flask, render_template, request, jsonify
from scraper_functions import fetch_profile_metrics, init_driver  # ✅ FIXED

app = Flask(__name__)

def install_chrome():
    """Install Google Chrome and Chromedriver on Render"""
    if not os.path.exists("/usr/bin/google-chrome"):
        print("Installing Google Chrome...")
        subprocess.run("wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb", shell=True)
        subprocess.run("sudo dpkg -i google-chrome-stable_current_amd64.deb", shell=True)
        subprocess.run("sudo apt-get install -f -y", shell=True)

    if not os.path.exists("/usr/bin/chromedriver"):
        print("Installing ChromeDriver...")
        subprocess.run("wget -q https://chromedriver.storage.googleapis.com/115.0.5790.102/chromedriver_linux64.zip", shell=True)
        subprocess.run("unzip -o chromedriver_linux64.zip", shell=True)
        subprocess.run("sudo mv chromedriver /usr/bin/chromedriver", shell=True)
        subprocess.run("sudo chmod +x /usr/bin/chromedriver", shell=True)

# Ensure Chrome is installed before anything else runs
install_chrome()

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
