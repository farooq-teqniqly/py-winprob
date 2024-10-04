from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Setup the Chrome web driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

try:
    # Navigate to the desired page
    driver.get('https://www.baseball-reference.com/boxes/MIL/MIL202410030.shtml')  # Replace with the actual URL

    # Scroll to the bottom of the page
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to the bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(2)  # Adjust the sleep time if necessary

        # Calculate new scroll height and compare with the last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Get the page source (HTML content)
    html_content = driver.page_source

    # Save the HTML content to a file
    with open('page_content.html', 'w', encoding='utf-8') as file:
        file.write(html_content)

    print("Page HTML has been saved successfully.")
finally:
    # Close the browser
    driver.quit()
