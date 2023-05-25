import time

from flask import Flask, render_template
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd
import io

app = Flask(__name__)

def fetch():
    options = webdriver.ChromeOptions()
    #options.add_argument("--headless")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--incognito")
    service = Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=service, options=options)
    link = "https://acikveri.ysk.gov.tr/"
    browser.get(link)

    wait = WebDriverWait(browser, 10)
    wait.until(EC.visibility_of_element_located((By.ID, "myModalClose")))
    browser.find_element(By.XPATH, "//button[@aria-label='Close']").click() #Close modalPage
    browser.find_element(By.XPATH, "//a[@id='navbarDropdown']").click() #Click Choose Election
    browser.find_element(By.XPATH, "//a[@data-target='#collapse6']").click()  # Click Choose Election
    browser.find_element(By.XPATH, "//div[@aria-labelledby='heading6'][3]").click()
    e = browser.find_element(By.XPATH, "//a[@class ='nav-link'][8]")
    print(e.text)

    time.sleep(5)

@app.route("/")
def main():
    fetch()
    return "aaaa"


if __name__ == "__main__":
    app.run()