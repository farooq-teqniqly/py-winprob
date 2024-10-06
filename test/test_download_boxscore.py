import pytest
from download import download_boxscore_links
from pathlib import Path

def test_can_download_and_save_boxscore_links():
    year = 2024
    boxscore_links_json = download_boxscore_links(year)

    with open("boxscore_links_2024.json", "w", encoding="utf-8") as file:
        file.write(boxscore_links_json)

    print("Boxscore links has been saved successfully.")