import json
import pandas as pd
from tabulate import tabulate
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Konfigurasi Browser
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def scrape_dan_tampilkan():
    url = "https://www.racingmaster.game/sea/"
    data_list = []

    try:
        print(f"Mengakses {url}...")
        driver.get(url)
        
        wait = WebDriverWait(driver, 15)
        # Menunggu elemen link atau berita muncul
        elements = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "a")))

        seen_texts = set()
        id_counter = 1

        for el in elements:
            text = el.text.strip()
            # Filter hanya teks yang panjang (asumsi judul berita/update)
            if len(text) > 25 and text not in seen_texts:
                data_list.append({
                    "NO": id_counter,
                    "JUDUL UPDATE / BERITA": text[:70] + "..." if len(text) > 70 else text,
                    "SUMBER": "Racing Master"
                })
                seen_texts.add(text)
                id_counter += 1

        # 1. SIMPAN KE JSON (Format Indentasi Rapi)
        with open('data_racing.json', 'w', encoding='utf-8') as f:
            json.dump(data_list, f, indent=4, ensure_ascii=False)
        
        # 2. TAMPILKAN TABEL YANG RAPI
        if data_list:
            # Menggunakan Tabulate untuk format grid (bergaris)
            print("\n" + "="*80)
            print(" HASIL SCRAPING DATA RACING MASTER ".center(80))
            print("="*80)
            
            # tablefmt="grid" akan membuat tabel dengan garis kotak yang rapi
            print(tabulate(data_list, headers="keys", tablefmt="grid", maxcolwidths=[None, 50, None]))
            
            print(f"\n✅ Total {len(data_list)} data disimpan ke 'data_racing.json'")
        else:
            print("❌ Tidak ada data yang ditemukan. Coba cek koneksi atau URL.")

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
    
    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_dan_tampilkan()