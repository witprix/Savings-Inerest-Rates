import json
import requests
from bs4 import BeautifulSoup

def fetch_latest_rates():
    # Load your current baseline file
    with open('rates.json', 'r') as f:
        data = json.load(f)

    print("Checking live bank reference portals...")

    # --- EXAMPLE SCRAIPING LOGIC (Using slice Repo Rate as an example) ---
    try:
        # Requesting slice's public documentation endpoint
        url = "https://help.slice.bank.in/support/solutions/articles/84000396024-what-is-the-interest-rate-on-savings-account-"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Look for percentage metrics inside their help layout article body text
            article_body = soup.find(class_="article-body")
            if article_body and "5.25%" in article_body.text:
                print("Confirmed slice tracking matches baseline 5.25%")
                data["slice"] = 5.25
    except Exception as e:
        print(f"Failed parsing live nodes: {e}. Keeping existing structural fallback values.")

    # Write the checked/updated data back into the repository file
    with open('rates.json', 'w') as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    fetch_latest_rates()
