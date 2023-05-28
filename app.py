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

    wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@class='country-svg']")))
    # browser.find_element(By.XPATH, "//div[@role='combobox']//input").click()

    try:
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "country-svg")))
        file_path="C:/Users/umitg/Downloads/SecimSonucIl.json"
        if not os.path.exists(file_path):
            wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='btn btn-sm btn-outline-dark mr-2'][2]"))).click()
            time.sleep(10)
            print("SecimSonucIl.json is downloaded...")
        else:
            print("SecimSonucIl.json is already exist...")
    except Exception as err:
        print(err)
    finally:
        browser.close()

    df = pd.read_json(file_path)
    df.columns = ['Plaka', 'İl', 'Kayıtlı Seçmen Sayısı', 'Oy Kullanan Seçmen Sayısı',
                  'Geçerli Oy Toplamı', 'MUHARREM İNCE', 'MERAL AKŞENER',
                  'RECEP TAYYİP ERDOĞAN', 'SELAHATTİN DEMİRTAŞ',
                  'TEMEL KARAMOLLAOĞLU', 'DOĞU PERİNÇEK']

    df = df.drop(df.index[df.index % 2 != 0])

    return df

def GetData(data):
    data['Geçerli Oy Toplamı'] = data['Geçerli Oy Toplamı'].str.replace('.', '').astype(int)
    data['MUHARREM İNCE'] = data['MUHARREM İNCE'].str.replace('.', '').astype(int)
    data['MERAL AKŞENER'] = data['MERAL AKŞENER'].str.replace('.', '').astype(int)
    data['RECEP TAYYİP ERDOĞAN'] = data['RECEP TAYYİP ERDOĞAN'].str.replace('.', '').astype(int)
    data['SELAHATTİN DEMİRTAŞ'] = data['SELAHATTİN DEMİRTAŞ'].str.replace('.', '').astype(int)
    data['TEMEL KARAMOLLAOĞLU'] = data['TEMEL KARAMOLLAOĞLU'].str.replace('.', '').astype(int)
    data['DOĞU PERİNÇEK'] = data['DOĞU PERİNÇEK'].str.replace('.', '').astype(int)

    return data

@app.route("/")
def main():
    df_main = fetch()
    data_main = GetData(df_main)
    election_result={}
    for x in range(4,len(data_main.columns)):
        election_result={data_main}

    return render_template("index.html",
                           sumOfVotes="{:,.0f}".format(data_main['Geçerli Oy Toplamı'].sum()).replace(',', '.'),
                           cand1_name=data_main.columns[5],
                           cand1_votes="{:.0f}".format(data_main['MUHARREM İNCE'].sum()).replace(',', '.'),
                           content=df_main.to_html()
                           )

if __name__ == "__main__":
    app.run()
