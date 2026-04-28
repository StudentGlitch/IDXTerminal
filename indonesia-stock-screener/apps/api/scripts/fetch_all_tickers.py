import os
import json
import random
import requests

# The path to your config.py file
CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config.py')

_IDX_API_URL = (
    "https://www.idx.co.id/primary/ListedCompany/GetStockList"
    "?start=0&length=9999&sectorCode=&subsectorCode=&industryCode="
    "&boardCode=&searchTicker="
)

def get_headers() -> dict:
    ua_pool = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
    ]
    return {
        "User-Agent": random.choice(ua_pool),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9,id;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.idx.co.id/",
        "Connection": "keep-alive",
    }

def fetch_idx_tickers():
    print("Fetching IDX tickers dynamically using your IDX API logic...")
    
    try:
        resp = requests.get(_IDX_API_URL, headers=get_headers(), timeout=30)
        resp.raise_for_status()
        data = resp.json()
        
        records = data.get("data", [])
        tickers = [r.get("StockCode", "").strip() for r in records if r.get("StockCode", "").strip()]
        
        if not tickers:
            print("IDX API returned 0 records. Cloudflare might be blocking the request locally.")
            return

        print(f"Successfully fetched {len(tickers)} tickers from the dynamic source!")
        
        # Format the new config content
        config_content = f'''# Target tickers for Full Market (Auto-fetched dynamically)
# Total Count: {len(tickers)}
TARGET_TICKERS = {json.dumps(tickers, indent=4)}
'''
        
        # Write it back to config.py
        with open(CONFIG_PATH, 'w') as f:
            f.write(config_content)
            
        print(f"Success! {CONFIG_PATH} has been updated with the full market list.")

    except Exception as e:
        print(f"Failed to fetch dynamically from IDX API: {e}")
        print("\nNote: If this fails locally with a 403, Cloudflare is blocking you. It will likely work flawlessly on your VPS as you tested before!")

if __name__ == "__main__":
    fetch_idx_tickers()
