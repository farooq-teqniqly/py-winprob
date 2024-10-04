from bs4 import BeautifulSoup
from pathlib import Path
from typing import List
import requests
import math

def download(url: str) -> str:
    response = requests.get(url)

    if response.status_code == 200:
        return response.text

def save(response_text: str, target_file_path: Path) -> None:
    with open(target_file_path, "w", encoding="utf-8") as file:
        file.write(response_text)

def load(source_file_path: Path) -> str:
    with open(source_file_path, "r", encoding="utf-8") as file:
        return file.read()

def parse(content: str):
    soup = BeautifulSoup(content, "html.parser")
    path_elements = soup.find_all("path")
    y_coords:List[int] = []

    for path_element in path_elements:
        rect_element = path_element.find_previous_sibling("rect")

        if rect_element and rect_element.has_attr("y"):
            y_coords.append(math.floor(float(rect_element["y"])))

    pass

if __name__ == "__main__":
    # url = "https://www.baseball-reference.com/boxes/MIL/MIL202410030.shtml"
    # response_text = download(url)
    # save(response_text, Path("python.html"))
    content = load("page_content.html")
    parse(content)
