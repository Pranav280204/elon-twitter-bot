import time
import requests
import xml.etree.ElementTree as ET

# ==========================
# CONFIGURATION
# ==========================

BOT_TOKEN = "8596301585:AAH2BuU-0BCUlP5lLirY-iyeb8IRRA7qKQg"   # <-- paste your token
CHAT_ID = 5792224870                         # <-- your chat id

# Working RSS feed URL
RSS_URL = "https://rss.app/feeds/Qq4DGdFXk7TXxxgN.xml"

# Poll every second
POLL_INTERVAL = 1  # seconds


# ==========================
# TELEGRAM
# ==========================

def send_telegram_message(text: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": text,
        "disable_web_page_preview": False,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, data=data, timeout=5)
        print("[SENT] Notification delivered.")
    except Exception as e:
        print(f"[ERROR] Telegram send failed: {e}")


# ==========================
# FETCH & PARSE RSS
# ==========================

def get_latest_tweet():
    try:
        r = requests.get(RSS_URL, timeout=5)
        r.raise_for_status()
    except Exception as e:
        print(f"[ERROR] Failed to fetch RSS: {e}")
        return None, None

    try:
        root = ET.fromstring(r.text)
        item = root.find("channel").find("item")

        title = item.find("title").text
        link = item.find("link").text
        guid = item.find("guid").text if item.find("guid") is not None else link

        message = f"🚨 *Elon Musk Tweeted!*\n\n📝 {title}\n🔗 {link}"
        return guid, message
    except Exception as e:
        print(f"[ERROR] RSS parsing failed: {e}")
        return None, None


# ==========================
# MAIN LOOP
# ==========================

def main():
    last_seen = None
    print("\n🔥 Elon Tweet Live Monitor Running... (checking every 1 sec)\n")

    while True:
        tweet_id, message = get_latest_tweet()

        if tweet_id and tweet_id != last_seen:
            # avoid sending the first time so we start clean
            if last_seen is not None:
                print("[NEW] Tweet detected, sending to Telegram...")
                send_telegram_message(message)
            else:
                print("[INIT] Latest tweet stored, watcher now active.")

            last_seen = tweet_id

        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    main()
