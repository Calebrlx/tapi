from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up the Chrome WebDriver
service = Service('/usr/local/bin/chromedriver')  # Path to your ChromeDriver
driver = webdriver.Chrome(service=service)

# Open a website
driver.get('https://www.tumblr.com')

# Wait for the element to be present
wait = WebDriverWait(driver, 10)
element = wait.until(EC.presence_of_element_located((By.ID, 'exampleElementId')))

# Take a screenshot of the element
element.screenshot('element_screenshot.png')

# Close the browser
driver.quit()