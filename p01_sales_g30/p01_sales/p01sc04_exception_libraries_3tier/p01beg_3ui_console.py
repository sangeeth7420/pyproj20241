# Import required functions and objects from the `p01_2bl_salesmanager` module
from p01_sales.p01sc04_exception_libraries_3tier.p01beg_2bl_salesmanager import (
    view_sales, add_sales1, add_sales2, import_sales, save_all_sales, import_all_sales
)

def display_title():
    print("\nSALES DATA IMPORTER\n")

def display_menu():
    cmd_format = "6"  # ^ center, < is the default for str.
    print("COMMAND MENU",
          f"{'view':{cmd_format}} - View all sales",
          f"{'add1':{cmd_format}} - Add sales by typing sales, year, month, day, and region",
          f"{'add2':{cmd_format}} - Add sales by typing sales, date (YYYY-MM-DD), and region",
          f"{'import':{cmd_format}} - Import sales from file",
          f"{'menu':{cmd_format}} - Show menu",
          f"{'exit':{cmd_format}} - Exit program", sep='\n')

# Ask the user to enter a command and call corresponding functions
def execute_command(sales_list) -> None:
    while True:
        command = input("Enter command: ").strip().lower()
        if command == "view":
            view_sales(sales_list)
        elif command == "add1":
            add_sales1(sales_list)
        elif command == "add2":
            add_sales2(sales_list)
        elif command == "import":
            import_sales(sales_list)  # Only `sales_list` is passed here
        elif command == "menu":
            display_menu()
        elif command == "exit":
            save_all_sales(sales_list)
            print("Bye!")
            break
        else:
            print("Invalid command. Please try again.")
            display_menu()

def main():
    display_title()
    display_menu()

    # Get all original sales data from a CSV file
    sales_list = import_all_sales()

    execute_command(sales_list)

# If started as the main module, call the main function
if __name__ == "__main__":
    main()
