import os.path
import time

from flask import Flask, render_template
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
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

    wait = WebDriverWait(browser, 30)

    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Close']"))).click() #Close modalPage
    wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@id='navbarDropdown']"))).click() #Click Choose Election
    wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@data-target='#collapse6']"))).click()  #
    wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@aria-labelledby='heading6'][1]"))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/secim-sonuc-istatistik/secim-sonuc']"))).click()

    wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@class='country-svg']//*[@il_id='1']")))
    browser.execute_script("document.querySelector('#map > svg > g > path:nth-child(1)')")

    time.sleep(10)

    # browser.close()
    # try:
    #     wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "country-svg")))
    #     file_path = "C:\\Users\\umitg\\Downloads\\SecimSonucIl.json"
    #     if not os.path.exists(file_path):
    #         browser.find_element(By.XPATH, "//button[@class='btn btn-sm btn-outline-dark mr-2'][2]").click()
    #         browser.find_element(By.XPATH, "//*[@id='map']/svg/g/path[1]").click()
    #         time.sleep(10)
    #         print("Cities Json File is downloaded...")
    #     else:
    #         print("Json File is already exist...")
    # except Exception as err:
    #     print(err)
    # finally:
    #     browser.close()



@app.route("/")
def main():
    fetch()
    return "aaaa"

if __name__ == "__main__":
    app.run()
