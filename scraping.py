import json
import time
import subprocess
from tabulate import tabulate
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Setup Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_options
)

def scrape_mobil():
    url = "https://racingmaster.info/cars/"
    data = []

    try:
        print("🌐 Membuka halaman mobil...")
        driver.get(url)

        # Tunggu tabel muncul
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//table"))
        )

        rows = driver.find_elements(By.XPATH, "//table//tr")

        no = 1
        for row in rows[1:]:
            cols = row.find_elements(By.TAG_NAME, "td")

            if len(cols) >= 12:
                data.append({
                    "NO": no,
                    "CLASS": cols[0].text,
                    "NAMA MOBIL": cols[1].text,
                    "HP": cols[2].text,
                    "BERAT(KG)": cols[4].text,
                    "GRIP": cols[6].text,
                    "ACC": cols[8].text,
                    "BRAKE": cols[10].text
                })
                no += 1

        # Validasi data
        if not data:
            print("⚠️ Data kosong! Scraping gagal.")
            return

        # Simpan JSON
        file_path = "data_mobile.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        print(f"✅ Data berhasil disimpan ke {file_path}")

        # Tampilkan tabel
        print("\n" + "="*110)
        print("DATA MOBIL RACING MASTER".center(110))
        print("="*110)
        print(tabulate(data, headers="keys", tablefmt="grid"))

        print(f"\nTotal mobil: {len(data)}")

        # Push ke GitHub
        push_to_github(file_path)

    except Exception as e:
        print("❌ Error:", e)

    finally:
        driver.quit()


def push_to_github(file_path):
    try:
        print("🚀 Sync & Push ke GitHub...")

        # Ambil update dari remote dulu
        subprocess.run(["git", "pull", "--rebase", "origin", "main"], check=True)

        # Add & commit
        subprocess.run(["git", "add", file_path], check=True)
        subprocess.run(["git", "commit", "-m", f"Update data mobil {time.time()}"], check=True)

        # Push
        subprocess.run(["git", "push", "origin", "main"], check=True)

        print("✅ Berhasil sync & push ke GitHub!")

    except Exception as e:
        print("❌ Gagal push GitHub:", e)


if __name__ == "__main__":
    scrape_mobil()