import json
import os
import time
from pathlib import Path
from typing import List

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

ROOT_URL = "https://www.baseball-reference.com"
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)


def download_boxscore_links(year: int) -> str:
    """
    Args:
        year: The year for which the boxscore links need to be downloaded.

    Returns:
        A JSON string containing the list of boxscore links for the specified year.
    """
    try:
        soup = _get_soup_for_page(f"{ROOT_URL}/leagues/majors/{year}-schedule.shtml")
        a_tags = soup.find_all("a")

        boxscore_links = []

        for a_tag in a_tags:
            if a_tag.get_text() == "Boxscore":
                boxscore_links.append(f"{ROOT_URL}{a_tag["href"]}")

        boxscore_links_json = json.dumps(boxscore_links)

        return boxscore_links_json
    finally:
        driver.quit()


def download_box_scores(links: List[str], output_dir: Path, delay_between_downloads_seconds=2):
    """
    Args:
        links: List of URLs to download box scores from.
        output_dir: Directory where the downloaded box scores will be saved.
        delay_between_downloads_seconds: Number of seconds to wait between downloads.
    """
    for link in links:
        filename = os.path.join(output_dir, f"{link.split('/')[-1]}")

        if os.path.exists(filename):
            continue

        soup = _get_soup_for_page(link)

        with open(filename, "w", encoding="utf-8") as file:
            file.write(str(soup.prettify()))

        print(f"Saved boxscore to {filename}")
        time.sleep(delay_between_downloads_seconds)


def _scroll_to_bottom(sleep_time_sec=2):
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(sleep_time_sec)
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break

        last_height = new_height


def _get_soup_for_page(url: str) -> BeautifulSoup:
    driver.get(url)
    _scroll_to_bottom()
    return BeautifulSoup(driver.page_source, "html.parser")
