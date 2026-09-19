import time
import cloudscraper
from datetime import datetime, timedelta

SupabaseUrl = "https://ridnmxfctzfntbfpzjnd.supabase.co/rest/v1/rounds"
SupabaseKey = "sb_publishable_AvI5aU3gVjj2r7PxCcfaWA_L7WOiy7m"
ApiUrl = "https://draw.ar-lottery01.com/WinGo/WinGo_30S/GetHistoryIssuePage.json"

SupabaseHeaders = {
    "apikey": SupabaseKey,
    "Authorization": f"Bearer {SupabaseKey}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

# API ko dhokha dene ke liye dhaniwin ka reference
ApiHeaders = {
    "Referer": "https://dhaniwin.org/",
    "Origin": "https://dhaniwin.org"
}

print("🚀 GitHub Actions + Cloudflare Bypass Scraper Started!")

# Cloudscraper ka bypass engine (Real Chrome ki tarah act karega)
scraper = cloudscraper.create_scraper(browser={
    'browser': 'chrome',
    'platform': 'windows',
    'desktop': True
})

end_time = datetime.now() + timedelta(hours=5, minutes=45)

while datetime.now() < end_time:
    try:
        last_req = scraper.get(f"{SupabaseUrl}?select=period&order=period.desc&limit=1", headers=SupabaseHeaders)
        last_saved_period = "0"
        if last_req.status_code == 200 and len(last_req.json()) > 0:
            last_saved_period = str(last_req.json()[0]['period'])

        # API ko nakli headers ke sath hit karo
        api_req = scraper.get(ApiUrl, headers=ApiHeaders)
        
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
                res = scraper.post(SupabaseUrl, headers=SupabaseHeaders, json=new_rounds)
                if res.status_code == 201:
                    print(f"✅ HACK SUCCESS: Saved {len(new_rounds)} rounds! Latest: {new_rounds[-1]['period']}")
                else:
                    print(f"❌ Supabase Error: {res.text}")
        else:
            print(f"❌ API Blocked! Status: {api_req.status_code}")
                
    except Exception as e:
        print(f"⚠️ Code Crash Error: {e}") 
        
    time.sleep(10)

print("⏳ Cycle complete. Exiting for next worker.")
