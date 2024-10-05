from bs4 import BeautifulSoup
from pathlib import Path
from typing import List, Dict
import numpy as np
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

def parse_raw_wp_vals(content: str) -> List[int]:
    soup = BeautifulSoup(content, "html.parser")
    path_elements = soup.find_all("path")
    raw_wp_vals:List[int] = []

    for path_element in path_elements:
        rect_element = path_element.find_previous_sibling("rect")

        if rect_element and rect_element.has_attr("y"):
            raw_wp_vals.append(math.floor(float(rect_element["y"])))

    return raw_wp_vals

def get_interpolation() -> Dict[int, int]:
    raw_points = [30, 150, 269]
    norm_points = [0, 50, 100]

    percentages = np.arange(0, 101, 1)
    interpolation = np.interp(percentages, norm_points, raw_points)

    return dict(zip([math.floor(i) for i in interpolation], percentages))

def get_normalized_wp(raw_wp_vals: List[int], interpolation: dict) -> List[int]:
    normalized_vals = []

    for v in raw_wp_vals:
        normalized_val: int

        if not v in interpolation:
            normalized_val = interpolation[v - 1]
        else:
            normalized_val = interpolation[v]

        normalized_vals.append(normalized_val)

    return normalized_vals

if __name__ == "__main__":
    # url = "https://www.baseball-reference.com/boxes/MIL/MIL202410030.shtml"
    # response_text = download(url)
    # save(response_text, Path("python.html"))
    content = load("page_content.html")
    raw_wp_vals = parse_raw_wp_vals(content)
    interpolation = get_interpolation()
    normalized_wp_vals = get_normalized_wp(raw_wp_vals, interpolation)

    for v in normalized_wp_vals:
        print(v)