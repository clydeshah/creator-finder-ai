import requests
import gspread
from google.oauth2.service_account import Credentials

# 🔑 Your YouTube API key goes here (from Step 5 earlier)
YOUTUBE_API_KEY = "AIzaSyAmHGkn5Omnot9JtOCe95FyeQeGlWNvG50"

# 📄 Your Google Sheet ID (from the sheet URL)
SHEET_ID = "1Aom8I91pr_1Exc120VKP7cIIKtbHPCiN-HipmoleTvg"

# 📁 Your service account credentials file (must be in the same folder)
scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("service_account.json", scopes=scopes)

# 📊 Authorize and connect to Google Sheets
client = gspread.authorize(creds)
sheet = client.open_by_key(SHEET_ID).sheet1

# 🔍 Function to search YouTube for creators based on keywords
def search_youtube_creators(keywords):
    query = "+".join(keywords)
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&type=channel&maxResults=10&key={YOUTUBE_API_KEY}"
    response = requests.get(url).json()
    results = []

    for item in response.get('items', []):
        channel_id = item['snippet']['channelId']
        name = item['snippet']['channelTitle']
        bio = item['snippet']['description']
        link = f"https://www.youtube.com/channel/{channel_id}"

        results.append({
            "platform": "YouTube",
            "name": name,
            "bio": bio,
            "link": link,
            "email": "TBD"
        })

    return results

# 📝 Save results to Google Sheet
def save_to_sheet(results):
    for creator in results:
        sheet.append_row([
            creator["platform"],
            creator["name"],
            "",
            creator["bio"],
            "",
            creator["link"],
            creator["email"]
        ])

# ▶️ Run the tool
if __name__ == "__main__":
    keywords = ["fitness", "wellness"]  # <- you can change these
    creators = search_youtube_creators(keywords)
    print(creators)
    save_to_sheet(creators)
    print("✅ Done! Creators added to Google Sheets.")
