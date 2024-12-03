from datetime import date, datetime
from pathlib import Path
import csv

# Constants
VALID_REGIONS = {"w": "West", "m": "Mountain", "c": "Central", "e": "East"}
DATE_FORMAT = "%Y-%m-%d"
FILEPATH = Path(__file__).parent.parent / 'p01_files'
ALL_SALES = 'all_sales.csv'
IMPORTED_FILES = 'imported_files.txt'
NAMING_CONVENTION = "sales_qn_yyyy_r.csv"


def get_region_name(region_code: str) -> str:
    """Returns the region name corresponding to the region code."""
    return VALID_REGIONS.get(region_code, "Unknown")


def cal_quarter(month: int) -> int:
    """Calculates the quarter for a given month."""
    if month in (1, 2, 3):
        return 1
    elif month in (4, 5, 6):
        return 2
    elif month in (7, 8, 9):
        return 3
    elif month in (10, 11, 12):
        return 4
    return 0


def is_leap_year(year: int) -> bool:
    """Checks if a year is a leap year."""
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)


def cal_max_day(year: int, month: int) -> int:
    """Calculates the maximum number of days in a given month for a specific year."""
    if month == 2:  # February
        return 29 if is_leap_year(year) else 28
    elif month in [4, 6, 9, 11]:  # April, June, September, November
        return 30
    else:  # All other months
        return 31


def correct_data_types(row: list):
    """Converts a row's data types to the expected types."""
    try:
        row[0] = float(row[0])  # Convert amount to float
    except ValueError:
        row[0] = "?"  # Mark invalid amount
    try:
        row[1] = datetime.strptime(row[1], DATE_FORMAT).date()  # Convert date to date object
    except ValueError:
        row[1] = "?"  # Mark invalid date


def from_input1():
    """Collects sales input details (year, month, day)."""
    amount = float(input("Enter amount: "))
    year = int(input("Enter year: "))
    month = int(input("Enter month: "))
    day = int(input("Enter day: "))
    sales_date = date(year, month, day)
    region_code = input("Enter region code (w/m/c/e): ").lower()
    return {"amount": amount, "sales_date": str(sales_date), "region": region_code}


def from_input2():
    """Collects sales input details (full date)."""
    amount = float(input("Enter amount: "))
    sales_date = input("Enter sales date (YYYY-MM-DD): ")
    region_code = input("Enter region code (w/m/c/e): ").lower()
    return {"amount": amount, "sales_date": sales_date, "region": region_code}


def get_region_code(filename: str) -> str:
    """Extracts the region code from the filename."""
    return filename.split('_')[-1][0]


def already_imported(filepath_name: Path) -> bool:
    """Checks if a file has already been imported."""
    try:
        with open(FILEPATH / IMPORTED_FILES) as file:
            files = [line.strip() for line in file.readlines()]
            return str(filepath_name) in files
    except FileNotFoundError:
        return False


def add_imported_file(filepath_name: Path):
    """Adds a file to the list of imported files."""
    with open(FILEPATH / IMPORTED_FILES, "a") as file:
        file.write(f"{filepath_name}\n")


def import_sales(filepath_name: Path) -> list:
    """Imports sales data from a CSV file."""
    sales_list = []
    try:
        with open(filepath_name, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if len(row) != 3:
                    continue
                correct_data_types(row)
                sales_list.append({
                    "amount": row[0],
                    "sales_date": row[1],
                    "region": get_region_code(filepath_name.name)
                })
    except FileNotFoundError:
        print(f"File '{filepath_name}' not found.")
    except Exception as e:
        print(f"An error occurred while importing: {e}")
    return sales_list


def import_sales_file(filepath_name: Path) -> list:
    """Reads sales data from a file and returns a list of sales."""
    sales_list = []
    try:
        with open(filepath_name, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if len(row) == 3:  # Expecting amount, date, region
                    correct_data_types(row)
                    sales_list.append({
                        "amount": row[0],
                        "sales_date": row[1],
                        "region": row[2]
                    })
    except Exception as e:
        print(f"Error reading file '{filepath_name}': {e}")
    return sales_list
