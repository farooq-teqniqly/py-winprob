import requests
from pathlib import Path

def download(url: str) -> str:
    response = requests.get(url)

    if response.status_code == 200:
        return response.text

    response.raise_for_status()

def save(response_text: str, target_file_path: Path) -> None:
    with open(target_file_path, "w", encoding="utf-8") as file:
        file.write(response_text)

def load(source_file_path: Path) -> str:
    with open(source_file_path, "r", encoding="utf-8") as file:
        return file.read()