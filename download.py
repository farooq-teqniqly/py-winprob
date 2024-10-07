import argparse
import json
import os
import time
from pathlib import Path
from typing import List
from tqdm import tqdm

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

        for a_tag in tqdm(a_tags):
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
    for link in tqdm(links):
        filename = os.path.join(output_dir, f"{link.split('/')[-1]}")

        if os.path.exists(filename):
            print(f"Skipping {filename}")
            continue

        soup = _get_soup_for_page(link)

        with open(filename, "w", encoding="utf-8") as file:
            file.write(str(soup.prettify()))

        print(f"Saved boxscore to {filename}")
        time.sleep(delay_between_downloads_seconds)

def main():
    """
    Command-line interface (CLI) tool for downloading links and boxscores.

    Parses command-line arguments and executes the corresponding functionality:
    - Downloads boxscore links for a given year.
    - Downloads boxscores from a provided links file.

    Functions:
        main(): Parses arguments and executes the appropriate command.
    """
    parser = argparse.ArgumentParser(description="CLI tool for downloading links and boxes.")

    subparsers = parser.add_subparsers(dest="command", required=True, help="Commands")

    download_links_parser = subparsers.add_parser("download-links",
                                                  help='Download links for a given year and target directory')
    download_links_parser.add_argument(
        "--year", required=True, type=int, help="Year for which to download links")

    download_links_parser.add_argument("--target-dir", required=True, type=str,
                                       help="Target directory to save the links")

    download_boxes_parser = subparsers.add_parser("download-boxes", help="Download boxes from a links file")

    download_boxes_parser.add_argument("--links-file", required=True, type=str,
                                       help="File containing the download links")

    download_boxes_parser.add_argument("--target-dir", required=True, type=str,
                                       help="Target directory to save the boxscores.")

    args = parser.parse_args()

    if args.command == "download-links":
        boxscore_links_json = download_boxscore_links(args.year)
        _write_boxscores_to_target(args, boxscore_links_json)

    elif args.command == "download-boxes":
        with open(args.links_file, "r", encoding="utf-8") as file:
            links = json.load(file)
            output_dir = _create_boxscore_target_dir(args)
            download_box_scores(links, output_dir)


def _create_boxscore_target_dir(args):
    year = args.links_file.replace(".json", "").split("_")[-1]
    output_dir = os.path.join(args.target_dir, "boxscores", str(year))
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    return output_dir


def _write_boxscores_to_target(args, boxscore_links_json):
    if not os.path.exists(args.target_dir):
        os.makedirs(args.target_dir)

    with open(os.path.join(args.target_dir, f"boxscore_links_{args.year}.json"), "w", encoding="utf-8") as file:
        file.write(boxscore_links_json)

    print("Boxscore links has been saved successfully.")

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

if __name__ == "__main__":
    main()