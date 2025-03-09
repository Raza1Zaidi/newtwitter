import json
import time
import random
import gzip
import csv
from seleniumwire import webdriver  
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

def init_driver():
    """Initialize a headless Chrome browser with Selenium Wire."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    )

    service = Service(executable_path="chromedriver")  # Render uses "chromedriver" in the same directory
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def fetch_profile_metrics(driver, auth_token, ct0, screen_names):
    """Scrape Twitter profile metrics given session cookies and a list of screen names."""
    results = {}

    driver.get("https://x.com")
    time.sleep(3)
    
    # Inject session cookies
    driver.add_cookie({"name": "auth_token", "value": auth_token, "domain": ".x.com"})
    driver.add_cookie({"name": "ct0", "value": ct0, "domain": ".x.com"})

    for screen_name in screen_names:
        driver.requests.clear()
        url = f"https://x.com/{screen_name}"
        driver.get(url)
        time.sleep(random.uniform(3, 6))

        target_request = None
        for request in driver.requests:
            if request.response and "UserByScreenName" in request.url and screen_name.lower() in request.url.lower():
                target_request = request
                break

        if target_request:
            try:
                raw_body = target_request.response.body
                try:
                    body = raw_body.decode('utf-8')
                except UnicodeDecodeError:
                    body = gzip.decompress(raw_body).decode('utf-8')

                data = json.loads(body)
                legacy = data.get("data", {}).get("user", {}).get("result", {}).get("legacy", {})

                metrics = {
                    "followers_count": legacy.get("followers_count"),
                    "friends_count": legacy.get("friends_count"),
                    "listed_count": legacy.get("listed_count"),
                    "location": legacy.get("location")
                }
                results[screen_name] = metrics
            except Exception as e:
                results[screen_name] = {"error": str(e)}

        time.sleep(random.uniform(5, 16))

    driver.quit()
    return results
