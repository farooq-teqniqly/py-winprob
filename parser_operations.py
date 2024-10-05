from bs4 import BeautifulSoup
from typing import List, Dict
import numpy as np

def parse_teams(content: str) -> Dict[str, str]:
    soup = BeautifulSoup(content, "html.parser")
    scorebox_div = soup.find("div", class_="scorebox")

    strong_elements = scorebox_div.find_all("strong")

    teams = []

    for strong in strong_elements[:2]:
        a_tag = strong.find("a")
        teams.append(a_tag.get_text())

    return dict(zip(["away_team", "home_team"], teams))

def parse_raw_wp_vals(content: str) -> List[int]:
    soup = BeautifulSoup(content, "html.parser")
    path_elements = soup.find_all("path")
    raw_wp_vals:List[int] = []

    for path_element in path_elements:
        rect_element = path_element.find_previous_sibling("rect")

        if rect_element and rect_element.has_attr("y"):
            raw_wp_vals.append(np.floor(float(rect_element["y"])))

    return raw_wp_vals