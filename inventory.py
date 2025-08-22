"""
This program provides a simple yet functional inventory management system for tracking shoes. 
It allows the user to view, search, add, restock, and evaluate stock items stored in 'inventory.txt'.

Features:
- View complete inventory in a clean tabular format
- Add new shoe entries to the file
- Identify and restock low inventory items
- Search shoes by product code
- Calculate and display total value of each shoe item
- Highlight the product with the highest stock available for sale

This program employs:
- Object-Oriented Programming using a custom Shoe class
- File I/O for reading and updating inventory
- Data validation, error handling, and friendly user prompts
- Reusable, modular functions for each task
"""

from tabulate import tabulate

class Shoe: 
    
    """Class representing a shoe item in the inventory"""

    def __init__(self, country, code, product, cost, quantity):
        """
        Initialise the following attributes:
            ● country,
            ● code,
            ● product,
            ● cost, and
            ● quantity.
        """
        self.country = country
        self.code = code
        self.product = product
        self.cost = float(cost)
        self.quantity = int(quantity)

    def get_cost(self):
        """Return the cost of the shoe."""
        print(f"Item cost: R {self.cost:.2f}")

    def get_quantity(self):
        """Return the available quantity of the shoe in inventory."""
        print(f"Inventory quantity: {self.quantity}")

    def __str__(self):
        """Return a string representation of the shoe object."""
        return f'''
Product:    {self.product}
Country:    {self.country}
Code:       {self.code}
Cost:       R {self.cost}
Quantity:   {self.quantity}'''

    def to_file_line(self):
        return f"{self.country},{self.code},{self.product},{self.cost},{self.quantity}"

#=============Shoe list===========
'''
The list will be used to store a list of objects of shoes.
'''
shoe_list = []


#==========Functions outside the class==============
def read_shoes_data():
    '''
    This function will open the file inventory.txt
    and read the data from this file, then create a shoes object with this data
    and append this object into the shoes list. One line in this file represents
    data to create one object of shoes.
    '''
    shoe_list.clear()
    try:
        with open('inventory.txt', 'r') as f:
            lines = f.readlines()
            for line in lines[1:]:
                temp = line.strip().split(',')
                if len(temp) == 5:
                    shoe = Shoe(*temp)
                    shoe_list.append(shoe)
    except FileNotFoundError:
        print("'inventory.txt' not found. Make sure the file exists.")
def capture_shoes():
    '''
    This function will allow a user to capture data
    about a shoe and use this data to create a shoe object
    and append this object inside the shoe list.
    '''
    try:
        country = input("Enter product country: ")
        code = input("Enter product code: ")
        product = input("Enter product name: ")
        cost = float(input("Enter cost (R): "))
        quantity = int(input("Enter quantity: "))

        shoe = Shoe(country, code, product, cost, quantity)
        shoe_list.append(shoe)

        with open('inventory.txt', 'a') as f:
            f.write('\n' + shoe.to_file_line())

        print("\n Product captured successfully!")
        print(shoe)

    except ValueError:
        print("Invalid input. Please enter correct numbers.")

def view_all():
    '''
    This function will iterate over the shoes list and
    print the details of the shoes returned from the __str__
    function. 
    '''
    if not shoe_list:
        print("Inventory is empty.")
        return

    table = [['Country', 'Code', 'Product', 'Cost (R)', 'Quantity']]
    for s in shoe_list:
        table.append([s.country, s.code, s.product, s.cost, s.quantity])
    print("\nInventory Overview")
    print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))

def re_stock():
    '''
    This function will find the shoe object with the lowest quantity,
    which is the shoes that need to be re-stocked. Ask the user if they
    want to add this quantity of shoes and then update it.
    This quantity should be updated on the file for this shoe.
    '''
    if not shoe_list:
        print("Inventory is empty.")
        return
   # Find the shoe with the lowest stock quantity
    stock_qty = [shoe.quantity for shoe in shoe_list]
    lowest_index = stock_qty.index(min(stock_qty))
    lowest_shoe = shoe_list[lowest_index]

    # Display product information
    print(f"\nLow Stock Item:\n\n{lowest_shoe}")

    # Ask user if they want to restock
    while True:
        choice = input("\nWould you like to restock this item? (Enter 'Y' for yes, 'N' for no, or 'e' to exit): ").strip().lower()

        if choice == 'y':
            # Ask for quantity to restock
            while True:
                try:
                    qty = int(input(f"Enter number of units to add to '{lowest_shoe.product}': "))
                    if qty < 0:
                        print("Please enter a non-negative number.")
                        continue
                    lowest_shoe.quantity += qty
                    break
                except ValueError:
                    print("Invalid input. Please enter a number only.")

            # Save changes to file
            try:
                with open("inventory.txt", "w") as f:
                    f.write("Country,code,product,cost,quantity")
                    for shoe in shoe_list:
                        f.write(f"{shoe.country},{shoe.code},{shoe.product},{shoe.cost},{shoe.quantity}\n")
                print(f"\n'{lowest_shoe.product}' has been restocked. New quantity: {lowest_shoe.quantity}")
            except Exception as e:
                print(f"Error saving to file: {e}")
            break

        elif choice == 'n':
            print(f"No changes made to '{lowest_shoe.product}'.")
            break

        elif choice == 'e':
            print("Exiting restock menu.")
            break

        else:
            print("Invalid option. Please type 'Y', 'N', or 'E'.")

def search_shoe():
    '''
     This function will search for a shoe from the list
     using the shoe code and return this object so that it will be printed.
   
    '''
    code = input("Enter product code to search: ").strip()
    for s in shoe_list:
        if s.code.lower() == code.lower():
            print("\nProduct Found:")
            print(s)
            return
    print("Product code not found.")

def value_per_item():
    '''
    This function will calculate the total value for each item.
    '''
    table = [['Product', 'Cost (R)', 'Quantity', 'Total Value (R)']]
    for s in shoe_list:
        total = s.cost * s.quantity
        table.append([s.product, f"{s.cost:.2f}", s.quantity, f"{total:.2f}"])
    print("\nProduct Values")
    print(tabulate(table, headers="firstrow", tablefmt="fancy_grid"))

def highest_qty():
    '''
    This function will determine the product with the highest quantity and
    print this shoe as being for sale.
    '''
    max_item = max(shoe_list, key=lambda s: s.quantity)
    print(f"\nOn Sale: {max_item.product.upper()}")
    print(max_item)

# ====================== Inventory Manager Main Menu ====================== #

read_shoes_data()

while True:
    print("\n********** INVENTORY MANAGER **********")
    print("\nPlease select an action below:")

    print("""
1. list  - Show full inventory
2. find  - Search for a product by code      
3. low   - Restock lowest stock product        
4. add   - Add a new product
5. value - Show value of each product
6. sale  - View item with most stock (on sale)
7. quit  - Exit the program
""")

    choice = input("Enter option number or keyword: ").strip().lower()

    if choice in ['1', 'list']:
        view_all() # Show full intentory

    elif choice in ['2', 'find']:
        search_shoe() # Search for a product by code

    elif choice in ['3', 'low']:
        re_stock() # Restock lowest stock product

    elif choice in ['4', 'add']:
        capture_shoes() # Add a new product

    elif choice in ['5', 'value']:
        value_per_item() # Show value of each product

    elif choice in ['6', 'sale']:
        highest_qty() # View Item with most stock

    elif choice in ['7', 'quit']:
        print("\nExiting Inventory Manager. Goodbye!")
        break

    else:
        print("Invalid option. Please enter a number 1–7 or a keyword.")


# REFERENCES

# HyperionDev Module M02T08 – Programming with User-defined Functions
# HyperionDev Module M03T02 – OOP Classes
# HyperionDev Module M02T05 – IO Operations and Code Files
# HyperionDev Module M02T06 – Data Structures – Lists and Dictionaries
# HyperionDev Module M02T07 – Programming with Built-in Functions
# HyperionDev Module M03T06 – Sorting and Searching
# https://docs.python.org/3/tutorial/errors.html
# https://docs.python.org/3/library/functions.html

# I have used:
# class Shoe(...) — to define a custom class to represent each shoe object
# def method_name(self): — to define instance methods such as mark_as_read and to_file_line
# open(filename, mode) — to read, write, and append data to inventory.txt
# with open(...) — for safe file handling and automatic closing
# list.append(...) — to add Shoe objects to the shoe_list
# list.clear() — to reset the list before repopulating from file
# str.split(',') — to split comma-separated values from the file into fields
# float(...) and int(...) — to convert input strings to numeric values
# try/except — to catch and handle invalid user inputs (ValueError)
# input(...) — to prompt user interaction for input values
# print(...) — to display formatted outputs for readability
# str formatting and f-strings — to build readable output messages and file lines
# tabulate(...) — from the tabulate library, to print lists in a tabular format (for better display)
# while True — to run the main menu loop until the user chooses to exit

# I also received support and discussion from my friends on how to restructure the `save_inventory()` 
# function after restocking, and how to apply list comprehensions when working with tabulate.
