import time
import requests

SupabaseUrl = "https://ridnmxfctzfntbfpzjnd.supabase.co/rest/v1/rounds"
SupabaseKey = "sb_publishable_AvI5aU3gVjj2r7PxCcfaWA_L7WOiy7m"
ApiUrl = "https://draw.ar-lottery01.com/WinGo/WinGo_30S/GetHistoryIssuePage.json"

Headers = {
    "apikey": SupabaseKey,
    "Authorization": f"Bearer {SupabaseKey}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

print("🚀 24/7 Cloud Scraper Started! Laptop band hone par bhi data aayega...")

while True:
    try:
        # 1. Supabase se last period check karo
        last_req = requests.get(f"{SupabaseUrl}?select=period&order=period.desc&limit=1", headers=Headers)
        last_saved_period = "0"
        if last_req.status_code == 200 and len(last_req.json()) > 0:
            last_saved_period = str(last_req.json()[0]['period'])

        # 2. API se naya result laao
        api_req = requests.get(ApiUrl)
        if api_req.status_code == 200:
            data = api_req.json()
            # Handle different API structures safely
            records = data.get('data', {}).get('list') or data.get('data', {}).get('records') or data.get('data', [])
            
            new_rounds = []
            
            for item in records:
                period = str(item.get('issueNumber', item.get('period', '')))
                size = str(item.get('size', '')).strip().upper()
                number = str(item.get('number', ''))
                
                # 🔥 STRICT RULE: Agar number khali hai ya '?' hai, toh ignore!
                if not number or number == "?" or not number.strip():
                    continue
                
                # Sirf final result save karo
                if size in ["BIG", "SMALL"]:
                    if int(period) > int(last_saved_period):
                        new_rounds.append({"period": period, "outcome": size})
            
            # 3. Supabase mein bhej do
            if len(new_rounds) > 0:
                new_rounds.reverse() # Purana pehle
                post_req = requests.post(SupabaseUrl, headers=Headers, json=new_rounds)
                if post_req.status_code == 201:
                    print(f"✅ HACK SUCCESS: {len(new_rounds)} naye rounds cloud se save hue!")

    except Exception as e:
        pass # Cloud par error aaye toh bas agle 10 second ka wait kare
        
    time.sleep(10) # 10 second ruk kar wapas check karega