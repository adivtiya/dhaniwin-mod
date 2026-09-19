import time
import requests
from datetime import datetime, timedelta

SupabaseUrl = "https://ridnmxfctzfntbfpzjnd.supabase.co/rest/v1/rounds"
SupabaseKey = "sb_publishable_AvI5aU3gVjj2r7PxCcfaWA_L7WOiy7m"
ApiUrl = "https://draw.ar-lottery01.com/WinGo/WinGo_30S/GetHistoryIssuePage.json"

Headers = {
    "apikey": SupabaseKey,
    "Authorization": f"Bearer {SupabaseKey}",
    "Content-Type": "application/json",
    "Prefer": "return=representation",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

print("🚀 GitHub Actions Cloud Scraper Started!")

# 5 hours 45 minutes run time
end_time = datetime.now() + timedelta(hours=5, minutes=45)

while datetime.now() < end_time:
    try:
        # Check last saved period from Supabase
        last_req = requests.get(f"{SupabaseUrl}?select=period&order=period.desc&limit=1", headers=Headers)
        last_saved_period = "0"
        if last_req.status_code == 200 and len(last_req.json()) > 0:
            last_saved_period = str(last_req.json()[0]['period'])

        # Get API Data
        api_req = requests.get(ApiUrl, headers=Headers)
        
        if api_req.status_code == 200:
            data = api_req.json()
            records = data.get('data', {}).get('list') or data.get('data', {}).get('records') or data.get('data', [])
            
            new_rounds = []
            for item in records:
                period = str(item.get('issueNumber', item.get('period', '')))
                size = str(item.get('size', '')).strip().upper()
                number = str(item.get('number', ''))
                
                # Check for valid number
                if not number or number == "?" or not number.strip():
                    continue
                
                if size in ["BIG", "SMALL"] and int(period) > int(last_saved_period):
                    new_rounds.append({"period": period, "outcome": size})
            
            if len(new_rounds) > 0:
                new_rounds.sort(key=lambda x: int(x["period"])) 
                res = requests.post(SupabaseUrl, headers=Headers, json=new_rounds)
                if res.status_code == 201:
                    print(f"✅ HACK SUCCESS: Saved {len(new_rounds)} rounds! Latest: {new_rounds[-1]['period']}")
                else:
                    print(f"❌ Supabase Error: {res.text}")
        else:
            print(f"❌ API Blocked! Status: {api_req.status_code}")
                
    except Exception as e:
        print(f"⚠️ Code Crash Error: {e}") 
        
    time.sleep(10)

print("⏳ Cycle complete.")
