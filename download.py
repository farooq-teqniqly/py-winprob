from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup
from pathlib import Path
import json

ROOT_URL = "https://www.baseball-reference.com"
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

def _scroll_to_bottom(sleep_time_sec=2):
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(sleep_time_sec)
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break

        last_height = new_height

def _get_soup_for_page(url:str) -> BeautifulSoup:
    driver.get(url)
    _scroll_to_bottom()
    return BeautifulSoup(driver.page_source, "html.parser")

def download_boxscore_links(year:int) -> str:
    try:
        soup =_get_soup_for_page(f"{ROOT_URL}/leagues/majors/{year}-schedule.shtml")
        a_tags = soup.find_all("a")

        boxscore_links = []

        for a_tag in a_tags:
            if a_tag.get_text() == "Boxscore":
                boxscore_links.append(f"{ROOT_URL}{a_tag["href"]}")

        boxscore_links_json = json.dumps(boxscore_links)

        return boxscore_links_json
    finally:
        driver.quit()
