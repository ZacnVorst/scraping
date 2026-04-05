import json
import time
from tabulate import tabulate
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Setup Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def scrape_mobil():
    url = "https://racingmaster.info/cars/"
    data = []

    try:
        print("Membuka halaman mobil...")
        driver.get(url)
        time.sleep(5)

        # Ambil semua baris tabel
        rows = driver.find_elements(By.XPATH, "//table//tr")

        no = 1
        for row in rows[1:]:  # skip header
            cols = row.find_elements(By.TAG_NAME, "td")

            if len(cols) >= 12:
                car_class = cols[0].text
                car_name = cols[1].text
                hp = cols[2].text
                kg = cols[4].text
                grip = cols[6].text
                acc = cols[8].text
                brake = cols[10].text

                data.append({
                    "NO": no,
                    "CLASS": car_class,
                    "NAMA MOBIL": car_name,
                    "HP": hp,
                    "BERAT(KG)": kg,
                    "GRIP": grip,
                    "ACC": acc,
                    "BRAKE": brake
                })
                no += 1

        # Simpan JSON
        with open("data_mobil.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        # Tampilkan tabel
        print("\n" + "="*110)
        print("DATA MOBIL RACING MASTER".center(110))
        print("="*110)
        print(tabulate(data, headers="keys", tablefmt="grid"))

        print(f"\nTotal mobil: {len(data)}")
        print("Data disimpan ke data_mobil.json")

    except Exception as e:
        print("Error:", e)

    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_mobil()