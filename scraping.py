import json
import time
from tabulate import tabulate
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Konfigurasi Browser
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def auto_scroll():
    # Scroll sampai bawah agar semua berita muncul
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        if new_height == last_height:
            break
        last_height = new_height

def scrape_dan_tampilkan():
    url = "https://www.racingmaster.game/sea/"
    data_list = []

    try:
        print(f"Mengakses {url}...")
        driver.get(url)
        time.sleep(5)

        # Scroll supaya semua berita muncul
        auto_scroll()

        elements = driver.find_elements(By.TAG_NAME, "a")

        seen = set()
        no = 1

        for el in elements:
            text = el.text.strip()
            link = el.get_attribute("href")

            if len(text) > 20 and link and text not in seen:
                data_list.append({
                    "NO": no,
                    "JUDUL": text,
                    "LINK": link
                })
                seen.add(text)
                no += 1

        # Simpan ke JSON
        with open("data_racing.json", "w", encoding="utf-8") as f:
            json.dump(data_list, f, indent=4, ensure_ascii=False)

        # Tampilkan tabel
        if data_list:
            print("\n" + "="*100)
            print(" HASIL SCRAPING RACING MASTER ".center(100))
            print("="*100)
            print(tabulate(data_list, headers="keys", tablefmt="grid", maxcolwidths=[5, 50, 40]))
            print(f"\nTotal data: {len(data_list)}")
        else:
            print("Tidak ada data ditemukan")

    except Exception as e:
        print("Error:", e)

    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_dan_tampilkan()