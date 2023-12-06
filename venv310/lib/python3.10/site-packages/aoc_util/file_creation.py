"""Help create files and pull input for AOC"""
from argparse import ArgumentParser
from pathlib import Path
import datetime as dt
import warnings
from rich import print
import pytz

# HTTP Requests
from requests.models import HTTPError

# local module to request pages from AOC
from aoc_util.aoc_requests import get_aoc_page

# EASTERN TIME FOR EVERYTHING
EASTERN = pytz.timezone("US/Eastern")

def is_valid_date(day: int, year: int) -> bool:
    """
    checks to validate the passed in day is
    less than or equal to today's date in order to
    not send any unnecessary requests

    Args:
        day (int): day of requested input
        year (int): year of requested input

    Returns:
        bool:
            True -> requested input can be queried,
            False -> requested input is in the future and cannot be accessed
    """
    today_date = dt.datetime.now(EASTERN)
    return year <= today_date.year and day <= today_date.day


def is_aoc_input_ready(day: int, year: int) -> bool:
    """
    checks to see if the input is ready to be pulled
    """
    today = dt.datetime.now(EASTERN)
    if EASTERN.localize(dt.datetime(year, 12, day)) <= today:
        return True
    warnings.warn_explicit(
        "\nInput is not ready. Please request a valid day, or wait for your input to be ready.",
        UserWarning,
        f"src/file_creation.py : get_input(day={day},year={year}) : line ",
        50,
        "newday",
    )
    return False


def create_input_file(day: int, year: int) -> None:
    """
    Uses your session cookie (to get your specific login) to pull your
    Puzzle Inputs. You can find session cookie
    in the developer portal of your browswer.

    For Chrome "Application" > "Storage" > "Cookies" >
    Find the session and retreave the value.

    Accepts a day, saves the input if it doesn't exist already
    Will create "./inputs" folder if it doesn't exist

    Note:
        This does not create the test input (from the question),
        you will have to create that file yourself
    """
    file_path = Path(f"./{year}/inputs/{day}.txt")
    # if the folder doesn't exists, create it
    if not file_path.parent.exists():
        file_path.parent.mkdir(parents=True)
    # if the file doesn't exists, create it and save the request data
    if not file_path.exists():
        # HTTP request
        r = get_aoc_page(f"https://adventofcode.com/{year}/day/{day}/input")
        if not r.ok:
            raise HTTPError(
                f"Did not get status 200. STATUS: {r.status_code}, "
                "verify session cookie is correct"
            )
        with open(file_path, "w") as f:
            f.write(r.text)
        print(f"INPUT SAVED: {file_path}")
    else:
        print(f"{file_path} already exists. Will not overwrite")


def create_python_file(day: int, year: int) -> None:
    """
    Will create a python file will all the lines of code I normally use
    Also will create the "./solutions" directory if it doesn't exists

    What is included in the Python File Template:
    1. Doc String with URL to today's challenge
    2. import statement to get the file reader
    3. code line to read the input
    4. part1 & part2 answer print statements

    TO RUN from the main directory in terminal:
        $ python solutions/helper.py {day int to create}
    """
    # read in the tempalte file
    with open("TEMPLATE_FILE.py", "r") as f:
        file_text = f.read()

    # alter the template to include the actual year and day
    file_text = file_text.replace("{year}", str(year)).replace("{day}", str(day))

    # creates the python file in solutions
    file_path = Path(f"./{year}/solutions/day{day}.py")
    if not file_path.parent.exists():
        file_path.parent.mkdir(parents=True)
    if not file_path.exists():
        with open(file_path, "a") as f:
            f.write(file_text)
        print(f"FILE CREATED FROM TEMPLATE: {file_path}")
    else:
        print(f"{file_path} already exists. Will not overwrite")


def newday() -> None:
    parser = ArgumentParser(description="Create AOC Python Files from template.")
    parser.add_argument(
        "-d",
        "--day",
        nargs="?",
        default=None,
        type=int,
        help="Defaults to today's date (day), can change to any day (1-25)",
    )
    parser.add_argument(
        "-y",
        "--year",
        nargs="?",
        default=None,
        type=int,
        help="Defaults to this year, can change to any previous year (2015-).",
    )
    parser.add_argument(
        "-i",
        "--input",
        nargs="?",
        default=False,
        const=True,
        type=bool,
        help="If tagged retrives the selected day's input. Requires session cookie as env variable.",
    )
    args = parser.parse_args()

    if args.day is None and args.year is None and dt.datetime.now(EASTERN).month != 12:
        raise ValueError("Sorry. Default values are only available in December.")

    if args.day is None:
        args.day = dt.datetime.now(EASTERN).day
    if args.year is None:
        args.year = dt.datetime.now(EASTERN).year

    if not is_valid_date(args.day, args.year):
        raise ValueError(f"Selections for newday are invalid.\n{args}")

    # CHECK VALUES to make sure they are in range
    if args.day not in range(1, 26):
        raise ValueError("Day needs to be in range (1-25)")
    if args.year not in range(2015, dt.datetime.now(EASTERN).year + 1):
        raise ValueError(
            f"Year needs to be in range {range(2015,dt.datetime.now(EASTERN).year+1)}"
        )

    print(args)
    print("CREATING PYTHON FILE")
    create_python_file(args.day, args.year)
    if args.input and is_aoc_input_ready(args.day, args.year):
        print("CREATING INPUT FILE")
        create_input_file(args.day, args.year)
    print("PROCESS COMPLETE")


if __name__ == "__main__":
    newday()
