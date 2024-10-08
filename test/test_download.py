import json
import os
import pytest
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup
from download import download_boxscore_links, download_box_scores
from unittest.mock import patch, mock_open, MagicMock
from pathlib import Path

@pytest.fixture
def mock_driver():
    with patch("download.webdriver.Chrome") as mock_driver:
        yield mock_driver


@pytest.fixture
def mock_soup():
    with patch("download.BeautifulSoup") as mock_soup:
        yield mock_soup


def test_download_boxscore_links(mock_driver, mock_soup):
    year = 2022
    mock_driver_instance = mock_driver.return_value
    mock_driver_instance.page_source = ("<html>"
                                        "<a href='/boxscore/123'>Boxscore</a>"
                                        "<a href='/boxscore/456'>Boxscore</a>"
                                        "</html>")

    mock_soup_object = BeautifulSoup(mock_driver_instance.page_source, "html.parser")
    mock_soup.return_value = mock_soup_object

    with patch("download._get_soup_for_page", return_value=mock_soup_object):
        result = download_boxscore_links(year)

    expected_links = json.dumps([
        "https://www.baseball-reference.com/boxscore/123",
    "https://www.baseball-reference.com/boxscore/456"])

    assert result == expected_links


@pytest.fixture
def mock_open_file():
    with patch("builtins.open", mock_open()) as mock_file:
        yield mock_file


@pytest.fixture
def mock_time_sleep():
    with patch("time.sleep") as mock_sleep:
        yield mock_sleep


@pytest.fixture
def mock_os_path_exists():
    with patch("os.path.exists", return_value=False) as mock_exists:
        yield mock_exists

def test_download_box_scores(mock_driver, mock_soup, mock_open_file, mock_time_sleep, mock_os_path_exists):
    links = ["https://www.baseball-reference.com/boxscore/123"]
    output_dir = Path("/fake_directory")

    mock_driver_instance = mock_driver.return_value
    mock_driver_instance.page_source = "<html><div>Boxscore content</div></html>"
    mock_soup_object = BeautifulSoup(mock_driver_instance.page_source, "html.parser")
    mock_soup.return_value = mock_soup_object

    with patch("download._get_soup_for_page", return_value=mock_soup_object):
        download_box_scores(links, output_dir, delay_between_downloads_seconds=0)

    expected_filename = os.path.join(output_dir, "123")
    mock_open_file.assert_called_once_with(expected_filename, "w", encoding="utf-8")
    mock_open_file().write.assert_called_once_with(str(mock_soup_object.prettify()))
    mock_time_sleep.assert_called_once_with(0)

if __name__ == "__main__":
    pytest.main()
