import time
import os
import pyautogui
from PIL import Image, ImageChops
import requests
import cv2
import numpy as np
from flask import Flask, request, jsonify, send_file

# Configuration
CHECK_INTERVAL = 60  # Interval in seconds to check for changes
SCREENSHOT_DIR = 'screenshots'
MAX_LOGS = 5
ZAPIER_WEBHOOK_URL = "https://ntfy.sh/yadp"# 'https://hooks.zapier.com/hooks/catch/your_zapier_webhook_id/'

# Ensure the screenshot directory exists
if not os.path.exists(SCREENSHOT_DIR):
    os.makedirs(SCREENSHOT_DIR)

# Flask app for manual trigger (optional)
app = Flask(__name__)

def take_screenshot():
    timestamp = int(time.time())
    screenshot_path = os.path.join(SCREENSHOT_DIR, f'screenshot_{timestamp}.png')
    screenshot = pyautogui.screenshot()
    screenshot.save(screenshot_path)
    return screenshot_path

def get_latest_screenshots():
    screenshots = sorted(
        [os.path.join(SCREENSHOT_DIR, f) for f in os.listdir(SCREENSHOT_DIR) if f.startswith('screenshot_')],
        key=os.path.getmtime,
        reverse=True
    )
    return screenshots[:2]

def compare_screenshots(img1_path, img2_path):
    img1 = cv2.imread(img1_path, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(img2_path, cv2.IMREAD_GRAYSCALE)
    diff = cv2.absdiff(img1, img2)
    _, diff = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
    return diff

def save_diff_image(diff):
    diff_path = os.path.join(SCREENSHOT_DIR, 'diff.png')
    cv2.imwrite(diff_path, diff)
    return diff_path

def cleanup_old_screenshots():
    screenshots = sorted(
        [os.path.join(SCREENSHOT_DIR, f) for f in os.listdir(SCREENSHOT_DIR) if f.startswith('screenshot_')],
        key=os.path.getmtime
    )
    while len(screenshots) > MAX_LOGS:
        os.remove(screenshots.pop(0))

def send_signal_to_zapier():
    # response = requests.post(ZAPIER_WEBHOOK_URL, json={"message": "Change detected!"})
    response = requests.post(ZAPIER_WEBHOOK_URL, data="Zapier Triggered".encode(encoding='utf-8'))
    return response.status_code

@app.route('/trigger', methods=['POST'])
def manual_trigger():
    # Take a new screenshot
    new_screenshot = take_screenshot()
    
    # Get the latest two screenshots
    latest_screenshots = get_latest_screenshots()
    
    # If there are at least two screenshots, compare them
    if len(latest_screenshots) == 2:
        diff = compare_screenshots(latest_screenshots[0], latest_screenshots[1])
        diff_path = save_diff_image(diff)
        
        # Send signal to Zapier if there are differences
        if np.sum(diff) > 0:
            send_signal_to_zapier()
        
        # Clean up old screenshots
        cleanup_old_screenshots()
        
        # Return the diff image
        return send_file(diff_path, mimetype='image/png')
    else:
        return jsonify({"status": "Not enough screenshots for comparison"}), 200

def main():
    while True:
        # Take a new screenshot and clean up old ones
        take_screenshot()
        cleanup_old_screenshots()
        
        # Wait for the next interval
        time.sleep(CHECK_INTERVAL)

if __name__ == '__main__':
    # Run the Flask app in a separate thread if you want to manually trigger the process
    from threading import Thread
    flask_thread = Thread(target=lambda: app.run(host='0.0.0.0', port=5000))
    flask_thread.start()
    
    # Run the main monitoring loop
    main()