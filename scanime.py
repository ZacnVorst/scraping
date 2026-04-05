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

def scrape_anime():
    url = "https://otakotaku.com/anime/season/later"
    data = []

    try:
        print("Membuka halaman...")
        driver.get(url)
        time.sleep(5)

        items = driver.find_elements(By.XPATH, "//div[contains(@class,'col')]")

        no = 1
        for item in items:
            text = item.text.split("\n")

            judul = ""
            tahun = ""

            for t in text:
                if len(t) > 3 and not t.isdigit():
                    judul = t
                    break

            for t in text:
                if t.isdigit() and len(t) == 4:
                    tahun = t
                    break

            if judul:
                data.append({
                    "NO": no,
                    "JUDUL ANIME": judul,
                    "TAHUN": tahun if tahun else "-"
                })
                no += 1

        # Simpan JSON
        with open("anime_otakotaku.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        # Tampilkan tabel rapi
        print("\n" + "="*60)
        print("DATA ANIME OTAKOTAKU".center(60))
        print("="*60)
        print(tabulate(
            data,
            headers="keys",
            tablefmt="grid",
            maxcolwidths=[5, 40, 10]  # INI YANG BIKIN RAPI
        ))

        print("\nTotal anime:", len(data))
        print("Data disimpan ke anime_otakotaku.json")

    except Exception as e:
        print("Error:", e)

    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_anime()