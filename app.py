import os.path
import time

from flask import Flask, render_template
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd

app = Flask(__name__)

def fetch():
    options = webdriver.ChromeOptions()
    #options.add_argument("--headless")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--incognito")
    service = Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=service, options=options)
    link = "https://acikveri.ysk.gov.tr/"

    il_file_path = "SecimSonucIl.json"
    ilce_file_path = "SecimSonucIlce.json"
    not_exist_ilce_json = []

    for ilce_file_index in range(0, 81):
        ilce_file_path = "SecimSonucIlce (" + str(ilce_file_index) + ").json"
        if not os.path.exists(il_file_path):
            not_exist_ilce_json.append(ilce_file_index + 1)

    if os.path.exists(il_file_path) and len(not_exist_ilce_json) == 0:
        print("SecimSonucIl.json is already exist...")
        print("81 SecimSonucIlce.json is already exist...")
    else:
        browser.get(link)

        wait = WebDriverWait(browser, 10)

        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Close']"))).click()  # Close ModalPage
        wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@id='navbarDropdown']"))).click()  # Choose Election
        wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[@data-target='#collapse6']"))).click()  # Presidential Election
        wait.until(EC.element_to_be_clickable((By.XPATH,
                                               "//div[@aria-labelledby='heading6']//*[text()=' CUMHURBAŞKANI VE 27.DÖNEM MİLLETVEKİLİ GENEL SEÇİMİ (24 Haziran 2018) ']"))).click()
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//a[@href='/secim-sonuc-istatistik/secim-sonuc']"))).click()  # Presidential Election Results

        try:
            wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "country-svg")))
            wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()=' Json İndir '][1]"))).click()
            time.sleep(3)
            print("SecimSonucIl.json is downloaded...")

            cities = []

            for i in not_exist_ilce_json:
                city_name_xpath = "//div[@id='map']//*[@class='text-dark'][" + str(i) + "]"
                wait.until(EC.presence_of_element_located((By.XPATH, city_name_xpath)))
                c = browser.find_element(By.XPATH, city_name_xpath)  # Select city name text on map
                cities.append(c.text)  # Append city name in list

            if len(cities) > 0:
                for city in cities:
                    wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@class='country-svg']")))
                    strXpath = "//*[text()='" + city + "'][1]"
                    wait.until(
                        EC.presence_of_element_located((By.XPATH, strXpath))).click()  # Click the city in the list
                    wait.until(EC.element_to_be_clickable(
                        (By.XPATH, "//button[text()=' Json İndir '][1]"))).click()  # Click 'Json İndir' for District
                    time.sleep(3)
                    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()=' Geri ']"))).click()

        except Exception as err:
            print(err)
        finally:
            browser.close()


    il_file_path = "SecimSonucIl.json"
    df_il = pd.read_json(il_file_path)
    df_il.columns = ['City ID', 'City', 'Registered Voter', 'Current Voter',
                  'Valid Vote', 'Muharrem İnce', 'Meral Akşener',
                  'Recep Tayyip Erdoğan', 'Selahattin Demirtaş',
                  'Temel Karamollaoğlu', 'Doğu Perinçek']

    df_il = df_il.drop(df_il.index[df_il.index % 2 != 0])
    df_il['City ID'] = df_il['City ID'].astype('int')

    df_temp = pd.DataFrame()
    df_ilce = pd.DataFrame()

    for i in range(81):
        ilce_file_path = "SecimSonucIlce (" + str(i) + ").json"
        df_temp = pd.read_json(ilce_file_path)
        df_temp = df_temp.drop(columns=["Belde Adı", "Mahaller Bazlı Veri İndir"])
        df_temp['İlçe Id'] = pd.to_numeric(df_temp['İlçe Id'], errors='coerce')
        df_temp = df_temp.dropna(subset=['İlçe Id'])
        df_temp['İlçe Id'] = df_temp['İlçe Id'].astype('int')
        df_temp['İl Id'] = i + 1
        df_ilce = pd.concat([df_ilce, df_temp], ignore_index=True)

    df_ilce.columns = ['ID', 'District', 'Registered Voter', 'Current Voter',
                     'Valid Vote', 'Muharrem İnce', 'Meral Akşener',
                     'Recep Tayyip Erdoğan', 'Selahattin Demirtaş',
                     'Temel Karamollaoğlu', 'Doğu Perinçek', 'City Id']

    df_ilce['City Id']=df_ilce['City Id'].astype('int')

    return df_il, df_ilce

def getData(data):
    df_data_vote=pd.DataFrame()
    df_data_vote['Muharrem İnce'] = data['Muharrem İnce'].str.replace('.', '').astype(int)
    df_data_vote['Meral Akşener'] = data['Meral Akşener'].str.replace('.', '').astype(int)
    df_data_vote['Recep Tayyip Erdoğan'] = data['Recep Tayyip Erdoğan'].str.replace('.', '').astype(int)
    df_data_vote['Selahattin Demirtaş'] = data['Selahattin Demirtaş'].str.replace('.', '').astype(int)
    df_data_vote['Temel Karamollaoğlu'] = data['Temel Karamollaoğlu'].str.replace('.', '').astype(int)
    df_data_vote['Doğu Perinçek'] = data['Doğu Perinçek'].str.replace('.', '').astype(int)

    sum_data = df_data_vote.sum()

    sum_votes=[]
    for sd in sum_data:
        sum_votes.append(sd)

    return sum_votes

@app.route("/")
def main():
    df_il_main, df_ilce_main = fetch()
    votes = getData(df_il_main)


    return render_template("index.html",
                           title="2018 Presidential Election Results",
                           il_results_headers=df_il_main.columns,
                           il_results=df_il_main.values,
                           ilce_results_headers=df_ilce_main.columns,
                           ilce_results=df_ilce_main.values,
                           votes=votes
                           )

if __name__ == "__main__":
    app.run()
