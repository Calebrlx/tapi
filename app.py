import os
import subprocess
from flask import Flask, send_file, request
from PIL import Image

app = Flask(__name__)

@app.route('/screenshot', methods=['GET'])
def take_screenshot():
    filename = "screenshot.png"
    # Use scrot to take a screenshot
    subprocess.run(["scrot", filename])
    
    return send_file(filename, mimetype='image/png')

@app.route('/screenshot/process', methods=['POST'])
def process_screenshot():
    filename = "screenshot.png"
    processed_filename = "processed_screenshot.png"
    
    # Take a screenshot
    subprocess.run(["scrot", filename])
    
    # Open the screenshot for processing
    with Image.open(filename) as img:
        # Example processing: convert to grayscale
        gray_img = img.convert('L')
        gray_img.save(processed_filename)
    
    return send_file(processed_filename, mimetype='image/png')

if __name__ == '__main__':
    app.run(host=:: port=5000)