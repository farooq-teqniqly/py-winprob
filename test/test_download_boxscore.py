import json
import os.path

from download import download_boxscore_links, download_box_scores

year = 2023
filename = f"boxscore_links_{year}.json"

def test_can_download_and_save_boxscore_links():
    boxscore_links_json = download_boxscore_links(year)

    with open(filename, "w", encoding="utf-8") as file:
        file.write(boxscore_links_json)

    print("Boxscore links has been saved successfully.")


def test_can_download_boxscores():
    with open(filename, "r", encoding="utf-8") as file:
        links = json.load(file)
        output_dir = os.path.join(os.getcwd(), "boxscores", str(year))

        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        download_box_scores(links, output_dir)
