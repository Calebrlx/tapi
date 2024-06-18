import requests
import random
import pyautogui
import time
from datetime import datetime, timedelta
import schedule
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# API URL for the database
API_URL = "http://10.0.0.25:8000"

# Example greetings and follow-up messages
greetings = [
    "Hey there! How are you doing today?",
    "Hi! Hope you’re having a great day!",
    "Hello! How’s it going?",
    "Hi! How are things with you?",
    "Hey! How’s your day been?",
    "Good morning! How are you?",
    "Hi there! How are things on your end?",
    "Hello! What’s up?",
    "Hey! How’s your day treating you?",
    "Hi! How’s everything going?",
    "Good afternoon! How have you been?",
    "Hello! How’s it going for you today?",
    "Hi! How’s your day shaping up?",
    "Hey there! How’s your day been so far?",
    "Hi! Hope your day is going well!",
    "Hello! How’s everything with you?",
    "Hi! How are you feeling today?",
    "Hey! How have you been?",
    "Hello! How’s your day progressing?",
    "Hi! How’s it going for you?"
]

follow_up = [
    "Hi again! Just wanted to introduce myself properly. I’m Peyton Hassan, an indie artist, and I create unique die-cut stickers. Would you be interested in checking them out?",
    "Hey! Following up from yesterday. I wanted to share that I design fun and whimsical die-cut stickers. Let me know if you’d like to see them!",
    "Hello again! I realized I didn’t mention this yesterday—I’m an indie artist and I make custom die-cut stickers. Would you like to see some of my designs?",
    "Hi there! I forgot to tell you yesterday that I create unique die-cut stickers. Are you interested in seeing some of my work?",
    "Hey! Just wanted to let you know that I design original die-cut stickers. If you’re interested, I’d love to share some of my designs with you."
]

def send_greeting():
    try:
        response = requests.get(f"{API_URL}/prospects?skip=0&limit=1")
        response.raise_for_status()
        prospects = response.json()
        if prospects:
            prospect = prospects[0]
            if prospect['status'] == 'not_contacted':
                message = random.choice(greetings)
                logging.info(f"Sending greeting to {prospect['slug']}: {message}")
                automate_task(prospect['slug'], message)
                update_prospect_status(prospect['id'], 'contacted')
    except requests.RequestException as e:
        logging.error(f"Error while sending greeting: {e}")

def follow_up_check():
    try:
        response = requests.get(f"{API_URL}/prospects?skip=0&limit=100")
        response.raise_for_status()
        prospects = response.json()
        for prospect in prospects:
            if prospect['status'] == 'contacted':
                updated_at = datetime.strptime(prospect['updated_at'], "%Y-%m-%dT%H:%M:%S.%f")
                if datetime.utcnow() - updated_at > timedelta(days=1):
                    message = random.choice(follow_up)
                    logging.info(f"Sending follow-up to {prospect['slug']}: {message}")
                    automate_task(prospect['slug'], message)
                    update_prospect_status(prospect['id'], 'followed_up')
    except requests.RequestException as e:
        logging.error(f"Error while checking follow-ups: {e}")

def update_prospect_status(prospect_id, status):
    try:
        response = requests.put(f"{API_URL}/prospects/{prospect_id}", json={"status": status})
        response.raise_for_status()
        logging.info(f"Updated prospect {prospect_id} status to {status}")
    except requests.RequestException as e:
        logging.error(f"Failed to update prospect {prospect_id} status to {status}: {e}")

def automate_task(slug, msg):
    try:
        logging.info(f"Automating task for {slug}: {msg}")
        pyautogui.moveTo(300, 300, duration=0.5)
        pyautogui.click()
        pyautogui.moveTo(670, 130, duration=0.5)
        pyautogui.click()
        pyautogui.typewrite(slug, interval=0.1)
        pyautogui.press('enter')
        pyautogui.typewrite(msg, interval=0.1)
        pyautogui.press('enter')
        time.sleep(2)  # Adjust sleep time as needed
    except pyautogui.FailSafeException as e:
        logging.error(f"Failed to automate task for {slug}: {e}")

if __name__ == "__main__":
    send_greeting()

    # Uncomment the following lines for scheduled tasks
    # schedule.every(30).minutes.do(send_greeting)
    # schedule.every().day.at("12:00").do(follow_up_check)

    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)