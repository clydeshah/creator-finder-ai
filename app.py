import streamlit as st
import requests
import gspread
from google.oauth2.service_account import Credentials

# --- SETUP ---
# Load service account credentials and connect to Google Sheets
SHEET_ID = "1Aom8I91pr_1Exc120VKP7cIIKtbHPCiN-HipmoleTvg"
YOUTUBE_API_KEY = "AIzaSyAmHGkn5Omnot9JtOCe95FyeQeGlWNvG50Y"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("service_account.json", scopes=SCOPES)
client = gspread.authorize(creds)
sheet = client.open_by_key(SHEET_ID).sheet1

# --- FUNCTIONS ---
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

def save_to_sheet(creators):
    for creator in creators:
        sheet.append_row([
            creator["platform"],
            creator["name"],
            "",
            creator["bio"],
            "",
            creator["link"],
            creator["email"]
        ])

# --- STREAMLIT UI ---
st.title("🎯 Creator Finder AI Tool")
st.markdown("Enter keywords below and we'll find YouTube creators who match!")

keywords_input = st.text_input("Enter keywords (comma separated):", "fitness, wellness")

if st.button("Find Creators"):
    keywords = [kw.strip() for kw in keywords_input.split(",") if kw.strip()]
    if not keywords:
        st.error("Please enter at least one keyword.")
    else:
        with st.spinner("Searching YouTube..."):
            results = search_youtube_creators(keywords)
            if results:
                st.success(f"Found {len(results)} creators.")
                for creator in results:
                    st.write(f"**{creator['name']}**")
                    st.write(f"🔗 [Channel Link]({creator['link']})")
                    st.write(f"📝 {creator['bio']}")
                    st.write("---")
                save_to_sheet(results)
                st.info("Results also saved to your Google Sheet ✅")
            else:
                st.warning("No creators found. Try different keywords.")
