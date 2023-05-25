from flask import Flask, render_template
from selenium import webdriver
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
    browser.find_element(By.CLASS_NAME, "modal-content").click()
    # browser.find_element(By.LINK_TEXT, " Seçim Seçiniz ").click()
    return "aaaa"


@app.route("/")
def main():
    fetch()



if __name__ == "__main__":
    app.run()