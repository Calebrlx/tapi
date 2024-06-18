import time
import os
import pyautogui
from PIL import Image, ImageChops
import requests
from flask import Flask, request, jsonify

# Configuration
CHECK_INTERVAL = 60  # Interval in seconds to check for changes
SCREENSHOT_PATH = 'screenshot.png'
PREVIOUS_SCREENSHOT_PATH = 'previous_screenshot.png'
ZAPIER_WEBHOOK_URL = 'https://hooks.zapier.com/hooks/catch/your_zapier_webhook_id/'

# Flask app for manual trigger (optional)
app = Flask(__name__)

def take_screenshot():
    screenshot = pyautogui.screenshot()
    screenshot.save(SCREENSHOT_PATH)

def compare_screenshots(img1_path, img2_path):
    img1 = Image.open(img1_path)
    img2 = Image.open(img2_path)
    diff = ImageChops.difference(img1, img2)
    return diff.getbbox() is not None

def send_signal_to_zapier():
    response = requests.post(ZAPIER_WEBHOOK_URL, json={"message": "Change detected!"})
    return response.status_code

@app.route('/trigger', methods=['POST'])
def manual_trigger():
    take_screenshot()
    if os.path.exists(PREVIOUS_SCREENSHOT_PATH):
        if compare_screenshots(SCREENSHOT_PATH, PREVIOUS_SCREENSHOT_PATH):
            send_signal_to_zapier()
    if os.path.exists(SCREENSHOT_PATH):
        os.rename(SCREENSHOT_PATH, PREVIOUS_SCREENSHOT_PATH)
    return jsonify({"status": "Triggered"}), 200

def main():
    while True:
        # Take a screenshot
        take_screenshot()
        
        # If there is a previous screenshot, compare it with the new one
        if os.path.exists(PREVIOUS_SCREENSHOT_PATH):
            if compare_screenshots(SCREENSHOT_PATH, PREVIOUS_SCREENSHOT_PATH):
                print("Change detected!")
                # send_signal_to_zapier()
            else:
                print("No change detected.")
        
        # Move the current screenshot to previous screenshot
        if os.path.exists(SCREENSHOT_PATH):
            os.rename(SCREENSHOT_PATH, PREVIOUS_SCREENSHOT_PATH)
        
        # Wait for the next interval
        time.sleep(CHECK_INTERVAL)

if __name__ == '__main__':
    # Run the Flask app in a separate thread if you want to manually trigger the process
    from threading import Thread
    flask_thread = Thread(target=lambda: app.run(port=5000))
    flask_thread.start()
    
    # Run the main monitoring loop
    main()