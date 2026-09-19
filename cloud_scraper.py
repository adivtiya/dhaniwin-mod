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
    "Prefer": "return=representation"
}

print("🚀 GitHub Actions 24/7 Cloud Scraper Started!")

# 5 ghante 45 min baad script ruk jayegi taaki naya action fresh start ho sake
end_time = datetime.now() + timedelta(hours=5, minutes=45)

while datetime.now() < end_time:
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
                
                if size in ["BIG", "SMALL"] and int(period) > int(last_saved_period):
                    new_rounds.append({"period": period, "outcome": size})
            
            if len(new_rounds) > 0:
                new_rounds.sort(key=lambda x: int(x["period"])) 
                requests.post(SupabaseUrl, headers=Headers, json=new_rounds)
                print(f"✅ Saved {len(new_rounds)} rounds to Supabase!")
                
    except Exception as e:
        pass 
        
    time.sleep(10)

print("⏳ Cycle complete. Exiting gracefully to let the next server take over.")
