import requests
import os
from dotenv import load_dotenv

load_dotenv()


def get_aoc_page(url: str) -> requests.Response:
    """
    Makes HTTP requests to the advent of code website
    Pulls in the COOKIE_SESSION enviornment variable
    and standardized User-Agent as was requested

    Args:
        url (str): url that we will pull

    Returns:
        requests.Response: object response
    """
    return requests.get(
        url=url,
        cookies={"session": os.environ["COOKIE_SESSION"]},
        headers={
            "User-agent": "github.com/jaceiverson/aoc-util by iverson.jace@gmail.com"
        },
    )
