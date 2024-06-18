from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pyautogui
import time

# Set up the Chrome WebDriver
service = Service('/path/to/chromedriver')  # Adjust the path to your ChromeDriver
driver = webdriver.Chrome(service=service)

# Open a website
driver.get("https://www.tumblr.com")

# Give some time for the page to load
time.sleep(3)

# Use Selenium to find the element location (example coordinates)
element = driver.find_element_by_id("exampleElementId")
location = element.location
size = element.size
center_x = location['x'] + size['width'] / 2
center_y = location['y'] + size['height'] / 2

# Use PyAutoGUI to move the cursor and click precisely
pyautogui.moveTo(center_x, center_y, duration=1)
pyautogui.click()

# Close the browser
driver.quit()