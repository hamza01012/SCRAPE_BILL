from DISCObill import DISCOBill
from real_scraper import scrape
from contact_Scrape import scrape_contact
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import time

desco = DISCOBill("fesco")

START = 1130000001
END =   1131000000

MAX_THREADS = 15  # Safe start (do NOT use 100)

# Ensure folder exists
os.makedirs("templates/fesco", exist_ok=True)

def fetch_bill(app_no):
    try:
        desco = DISCOBill("fesco")  # new instance per thread
        if "Bill not found" in desco.r.text:
            return ("not_found", app_no)
        post_text = desco.show(app_no)

        if post_text:
            
            result = scrape(post_text , app_no)
            ref_no = result.get("reference_no").replace(" ", "") if "reference_no" in result else None
            output = scrape_contact(ref_no[:14]) if ref_no else {"error": "Reference number not found in bill data"}

            return ("success", app_no)
        else:
            return ("failed", app_no)

    except Exception as e:
        return ("error", app_no)

try:
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        futures = [executor.submit(fetch_bill, app_no) for app_no in range(START, END)]

        for future in as_completed(futures):
            pass
except Exception as e:
    with open("Bill_Scraperd/error_log.txt", "a") as log_file:
        log_file.write(f"{time.ctime()}: Critical error - {str(e)}\n")
    
