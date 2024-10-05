from pathlib import Path
from typing import List, Dict
import numpy as np
import io_operations as iops
import parser_operations as pops

def get_interpolation() -> Dict[int, int]:
    raw_points = [30, 150, 269]
    norm_points = [0, 50, 100]

    percentages = np.arange(0, 101, 1)
    interpolation = np.interp(percentages, norm_points, raw_points)

    return dict(zip([np.floor(i) for i in interpolation], percentages))

def get_normalized_wp(raw_wp_vals: List[int], interpolation: dict) -> List[int]:
    normalized_vals = []

    for v in raw_wp_vals:
        if v not in interpolation:
            while v not in interpolation:
                v -= 1
                if v < 0:
                    v = 0
                    break

        normalized_val = interpolation[v]
        normalized_vals.append(normalized_val)

    return normalized_vals

if __name__ == "__main__":
    # url = "https://www.baseball-reference.com/boxes/MIL/MIL202410030.shtml"
    # response_text = iops.download(url)
    # iops.save(response_text, Path("python.html"))
    content = iops.load(Path("page_content.html"))
    raw_wp_vals = pops.parse_raw_wp_vals(content)
    interpolation = get_interpolation()
    normalized_wp_vals = get_normalized_wp(raw_wp_vals, interpolation)

    for v in normalized_wp_vals:
        print(v)