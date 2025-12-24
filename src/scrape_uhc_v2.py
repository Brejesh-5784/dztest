import os
import time
import io
import requests
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pypdf import PdfWriter, PdfReader

# --- CONFIGURATION ---
OUTPUT_DIR = "/Users/brejesh/portfolio/Developer/healthcare-agent-system/data/raw_policies"
FINAL_FILENAME = "Combined_UHC_Policies.pdf"
FULL_OUTPUT_PATH = os.path.join(OUTPUT_DIR, FINAL_FILENAME)

os.makedirs(OUTPUT_DIR, exist_ok=True)

# The specific library page for Commercial Medical Policies
UHC_URL = "https://www.uhcprovider.com/en/policies-protocols/commercial-policies/commercial-medical-drug-policies.html"

def main():
    print("🚀 Starting UHC Policy Scraper (v2)...")
    print(f"📂 Target: {FULL_OUTPUT_PATH}\n")

    merger = PdfWriter()
    
    # Launch Stealth Browser
    options = uc.ChromeOptions()
    options.add_argument("--no-first-run")
    # options.add_argument("--headless") # Keep headless OFF to verify visual load
    
    driver = uc.Chrome(options=options)
    
    try:
        driver.get(UHC_URL)
        
        print("⏳ Waiting for page to load...")
        
        # Wait specifically for the 'c-link' class often used by UHC, or just body
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Scroll to bottom to trigger any lazy loading
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5) 

        # Find ALL links
        links = driver.find_elements(By.TAG_NAME, "a")
        print(f"👀 Scanned {len(links)} total links on page. Filtering now...")

        pdf_urls = []
        debug_count = 0
        
        for link in links:
            href = link.get_attribute("href")
            text = link.text.strip()
            
            # DEBUG: Print the first 5 links to see what the bot sees
            if href and debug_count < 5:
                print(f"   [Debug Link]: {href}")
                debug_count += 1

            # --- FIXED FILTER LOGIC ---
            # 1. Must be a PDF
            # 2. Must contain 'comm-medical-drug' (UHC's folder name) OR 'commercial'
            if href and href.endswith(".pdf"):
                if "comm-medical-drug" in href or "commercial" in href:
                    if href not in pdf_urls:
                        pdf_urls.append(href)

        print(f"\n🔎 Found {len(pdf_urls)} VALID policy documents.")
        
        if len(pdf_urls) == 0:
            print("❌ Still 0? The page might require clicking a 'View All' button or is blocking the bot.")
            return

        # Prepare Download Session
        selenium_cookies = driver.get_cookies()
        session = requests.Session()
        for cookie in selenium_cookies:
            session.cookies.set(cookie['name'], cookie['value'])
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

       # Download & Merge Loop
        count = 0
        limit = 2000  # Safety limit for testing
        
        for url in pdf_urls:
            # OPTIONAL: Keep this if you want a safety brake, otherwise delete these 3 lines
            if count >= limit:
                print(f"🛑 Test limit of {limit} reached.")
                break

            filename = url.split("/")[-1]
            print(f"⬇️ Downloading ({count + 1}/{len(pdf_urls)}): {filename[:40]}...", end=" ")

            try:
                response = session.get(url, headers=headers, stream=True, timeout=15)
                
                if response.status_code == 200:
                    file_in_memory = io.BytesIO(response.content)
                    reader = PdfReader(file_in_memory)
                    for page in reader.pages:
                        merger.add_page(page)
                    print("✅ Merged")
                    count += 1
                else:
                    print(f"❌ Status {response.status_code}")
                
                # Sleep is important here! 253 requests is a lot.
                time.sleep(1.5) 

            except Exception as e:
                print(f"⚠️ Error: {e}")

        # Save Final File
        if count > 0:
            print(f"\n💾 Saving master PDF...")
            with open(FULL_OUTPUT_PATH, "wb") as f_out:
                merger.write(f_out)
            print(f"🎉 SUCCESS! Saved to: {FULL_OUTPUT_PATH}")
        else:
            print("\n⚠️ No policies were downloaded.")

    except Exception as e:
        print(f"❌ Critical Error: {e}")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()