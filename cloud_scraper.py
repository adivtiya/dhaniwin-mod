import time
import requests
import threading
import os
from flask import Flask

app = Flask(__name__)

# Tera original cloud scraper logic
def run_scraper():
    SupabaseUrl = "https://ridnmxfctzfntbfpzjnd.supabase.co/rest/v1/rounds"
    SupabaseKey = "sb_publishable_AvI5aU3gVjj2r7PxCcfaWA_L7WOiy7m"
    ApiUrl = "https://draw.ar-lottery01.com/WinGo/WinGo_30S/GetHistoryIssuePage.json"

    Headers = {
        "apikey": SupabaseKey,
        "Authorization": f"Bearer {SupabaseKey}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }

    print("🚀 24/7 Cloud Scraper Hidden Thread Mein Start Ho Gaya!")

    while True:
        try:
            last_req = requests.get(f"{SupabaseUrl}?select=period&order=period.desc&limit=1", headers=Headers)
            last_saved_period = "0"
            if last_req.status_code == 200 and len(last_req.json()) > 0:
                last_saved_period = str(last_req.json()[0]['period'])

            api_req = requests.get(ApiUrl)
            if api_req.status_code == 200:
                data = api_req.json()
                records = data.get('data', {}).get('list') or data.get('data', {}).get('records') or data.get('data', [])
                
                new_rounds = []
                
                for item in records:
                    period = str(item.get('issueNumber', item.get('period', '')))
                    size = str(item.get('size', '')).strip().upper()
                    number = str(item.get('number', ''))
                    
                    if not number or number == "?" or not number.strip():
                        continue
                    
                    if size in ["BIG", "SMALL"]:
                        if int(period) > int(last_saved_period):
                            new_rounds.append({"period": period, "outcome": size})
                
                if len(new_rounds) > 0:
                    new_rounds.reverse() 
                    post_req = requests.post(SupabaseUrl, headers=Headers, json=new_rounds)
                    if post_req.status_code == 201:
                        print(f"✅ HACK SUCCESS: {len(new_rounds)} rounds saved!")

        except Exception as e:
            pass 
            
        time.sleep(10)

# Dummy Web Server jo Render ko bewakoof banayega
@app.route('/')
def home():
    return "Dhaniwin API is Live and Running!"

if __name__ == "__main__":
    # Background mein scraper chalao
    t = threading.Thread(target=run_scraper)
    t.daemon = True
    t.start()
    
    # Web server start karo (Taki Render paise na mange)
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
