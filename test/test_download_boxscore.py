import os.path

import pytest
from download import download_boxscore_links, download_box_scores
from pathlib import Path
import json

def test_can_download_and_save_boxscore_links():
    year = 2024
    boxscore_links_json = download_boxscore_links(year)

    with open("boxscore_links_2024.json", "w", encoding="utf-8") as file:
        file.write(boxscore_links_json)

    print("Boxscore links has been saved successfully.")

def test_can_download_boxscores():
    with open("boxscore_links_2024.json", "r", encoding="utf-8") as file:
        links = json.load(file)
        output_dir = os.path.join(os.getcwd(), "boxscores")

        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        download_box_scores(links, output_dir)