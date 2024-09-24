from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
import os
import time
from dotenv import load_dotenv

load_dotenv()

chrome_prefs = {"profile.default_content_settings.popups": 0}
options = webdriver.ChromeOptions()
options.add_experimental_option("prefs", chrome_prefs)
options.add_argument("--disable-notifications")

root_path = os.getenv("ROOT_DIRECTORY")
service = Service(os.path.join(root_path, "drivers", "chromedriver"))

browser = webdriver.Chrome(service=service, options=options)
browser.set_window_size(1200, 800)
browser.get("https://social-support-data.com/login")

user = WebDriverWait(browser, 15).until(
    EC.element_to_be_clickable((By.NAME, "username"))
)
password = WebDriverWait(browser, 15).until(
    EC.element_to_be_clickable((By.NAME, "password"))
)

user.send_keys(os.getenv("USER_LOGIN"))
password.send_keys(os.getenv("USER_PASS"))

login_button = WebDriverWait(browser, 5).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.submit"))
)
login_button.click()

time.sleep(3)
browser.get(os.getenv("FAMILY_DATA_PAGE"))

electricity_data = []
income_data = []

for _ in range(int(os.getenv("MAX_SUPPORT_ENTRIES"))):
    details = browser.find_elements(By.CSS_SELECTOR, ".data-row")
    for detail in details:
        fields = detail.text.split("\n")
        if "Electricity" in fields[0]:
            electricity_data.append(fields)
        elif "Income" in fields[0]:
            income_data.append(fields)

    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

df_electricity = pd.DataFrame(electricity_data, columns=["Category", "Amount", "Date"])
df_income = pd.DataFrame(income_data, columns=["Category", "Amount", "Date"])

output_dir = os.path.join(root_path, "family_data")
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

df_electricity.to_csv(os.path.join(output_dir, "electricity_support.csv"), index=False)
df_income.to_csv(os.path.join(output_dir, "income_support.csv"), index=False)

browser.quit()
