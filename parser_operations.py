from bs4 import BeautifulSoup
from typing import List
import numpy as np

def parse_raw_wp_vals(content: str) -> List[int]:
    soup = BeautifulSoup(content, "html.parser")
    path_elements = soup.find_all("path")
    raw_wp_vals:List[int] = []

    for path_element in path_elements:
        rect_element = path_element.find_previous_sibling("rect")

        if rect_element and rect_element.has_attr("y"):
            raw_wp_vals.append(np.floor(float(rect_element["y"])))

    return raw_wp_vals