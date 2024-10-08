import json
import pytest
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup
from download import download_boxscore_links


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


if __name__ == "__main__":
    pytest.main()
