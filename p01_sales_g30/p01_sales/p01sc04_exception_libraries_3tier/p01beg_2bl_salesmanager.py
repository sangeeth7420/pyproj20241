import csv
from decimal import Decimal, ROUND_HALF_UP
import locale
from p01_sales.p01sc04_exception_libraries_3tier.p01beg_1da_sales import (
    FILEPATH, ALL_SALES, correct_data_types, get_region_name, cal_quarter,
    cal_max_day, from_input1, from_input2, VALID_REGIONS,
    date, datetime, DATE_FORMAT, already_imported, add_imported_file, get_region_code,
    NAMING_CONVENTION, import_sales_file
)

locale.setlocale(locale.LC_ALL, "en_US.UTF-8")


def import_all_sales() -> list:
    """Imports all sales from the main sales file."""
    sales_list = []
    try:
        with open(FILEPATH / ALL_SALES, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for line in reader:
                if len(line) != 3:
                    continue
                amount, sales_date, region_code = line
                sales_list.append({
                    "amount": float(amount),
                    "sales_date": sales_date,
                    "region": region_code
                })
    except FileNotFoundError:
        print("Sales file not found. Starting with an empty list.")
    return sales_list


def view_sales(sales_list: list) -> bool:
    """Displays all sales in a formatted table."""
    if not sales_list:
        print("No sales to view.\n")
        return False

    col_widths = [5, 15, 15, 15, 15]
    header = f"{'Index':<{col_widths[0]}}{'Date':<{col_widths[1]}}{'Quarter':<{col_widths[2]}}{'Region':<{col_widths[3]}}{'Amount':>{col_widths[4]}}"
    print(header)
    print('-' * sum(col_widths))

    total = Decimal("0.00")
    for idx, sale in enumerate(sales_list, start=1):
        amount = Decimal(sale["amount"]).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        total += amount
        sales_date = sale["sales_date"]
        region = get_region_name(sale["region"])
        quarter = cal_quarter(int(sales_date.split('-')[1]))
        print(f"{idx:<{col_widths[0]}}{sales_date:<{col_widths[1]}}{quarter:<{col_widths[2]}}{region:<{col_widths[3]}}{locale.currency(amount, grouping=True):>{col_widths[4]}}")

    print('-' * sum(col_widths))
    print(f"{'Total':<{col_widths[0] + col_widths[1] + col_widths[2] + col_widths[3]}}{locale.currency(total, grouping=True):>{col_widths[4]}}")
    return True


def add_sales1(sales_list: list):
    """Adds a new sale using detailed input with validation."""
    amount, year, month, day, region_code = None, None, None, None, None

    while amount is None:
        try:
            value = float(input("Amount: "))
            if value > 0:
                amount = value
            else:
                print("Amount must be greater than zero.")
        except ValueError:
            print("Invalid input. Please enter a valid amount.")

    while year is None:
        try:
            value = int(input("Year (2000-2999): "))
            if 2000 <= value <= 2999:
                year = value
            else:
                print("Year must be between 2000 and 2999.")
        except ValueError:
            print("Invalid input. Please enter a valid year.")

    while month is None:
        try:
            value = int(input("Month (1-12): "))
            if 1 <= value <= 12:
                month = value
            else:
                print("Month must be between 1 and 12.")
        except ValueError:
            print("Invalid input. Please enter a valid month.")

    while day is None:
        try:
            max_day = cal_max_day(year, month)
            value = int(input(f"Day (1-{max_day}): "))
            if 1 <= value <= max_day:
                day = value
            else:
                print(f"Day must be between 1 and {max_day}.")
        except ValueError:
            print("Invalid input. Please enter a valid day.")

    while region_code is None:
        value = input("Region ('w', 'm', 'c', 'e'): ").lower()
        if value in VALID_REGIONS:
            region_code = value
        else:
            print(f"Region must be one of the following: {tuple(VALID_REGIONS.keys())}.")

    sales_date = date(year, month, day)
    sales_list.append({"amount": amount, "sales_date": str(sales_date), "region": region_code})
    print(f"Sales for {sales_date} is added.\n")


def add_sales2(sales_list: list):
    """Adds a new sale using date input with validation."""
    amount, sales_date, region_code = None, None, None

    while amount is None:
        try:
            value = float(input("Amount: "))
            if value > 0:
                amount = value
            else:
                print("Amount must be greater than zero.")
        except ValueError:
            print("Invalid input. Please enter a valid amount.")

    while sales_date is None:
        value = input("Date (YYYY-MM-DD): ").strip()
        try:
            parsed_date = datetime.strptime(value, DATE_FORMAT).date()
            if 2000 <= parsed_date.year <= 2999:
                sales_date = parsed_date
            else:
                print("Year of the date must be between 2000 and 2999.")
        except ValueError:
            print(f"{value} is not in a valid date format.")

    while region_code is None:
        value = input("Region ('w', 'm', 'c', 'e'): ").lower()
        if value in VALID_REGIONS:
            region_code = value
        else:
            print(f"Region must be one of the following: {tuple(VALID_REGIONS.keys())}.")

    sales_list.append({"amount": amount, "sales_date": str(sales_date), "region": region_code})
    print(f"Sales for {sales_date} is added.\n")


def import_sales(sales_list: list):
    """Imports sales data from a file."""
    filename = input("Enter name of file to import: ").strip()
    filepath_name = FILEPATH / filename

    # Validate the filename format
    if not filename.endswith(".csv"):
        print(f"Filename '{filename}' doesn't follow the expected format of '{NAMING_CONVENTION}'.")
        return

    if already_imported(filepath_name):
        print(f"File '{filename}' has already been imported.")
        return

    try:
        imported_sales = import_sales_file(filepath_name)
        if not imported_sales:
            print("No valid data imported.")
            return
        sales_list.extend(imported_sales)
        print(f"Sales from file '{filename}' have been added.")
        add_imported_file(filepath_name)
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    except Exception as e:
        print(f"An error occurred while importing: {e}")


def save_all_sales(sales_list: list, delimiter: str = ','):
    """Saves all sales data to the main sales file."""
    sales_records = [[sale["amount"], sale["sales_date"], sale["region"]] for sale in sales_list]
    try:
        with open(FILEPATH / ALL_SALES, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=delimiter)
            writer.writerows(sales_records)
            print("Saved sales records.")
    except Exception as e:
        print(f"Failed to save sales records: {e}")


def main():
    """Main function for testing."""
    sales_list = import_all_sales()
    view_sales(sales_list)
    add_sales1(sales_list)
    view_sales(sales_list)
    add_sales2(sales_list)
    view_sales(sales_list)
    import_sales(sales_list)
    view_sales(sales_list)
    save_all_sales(sales_list)


if __name__ == "__main__":
    main()
